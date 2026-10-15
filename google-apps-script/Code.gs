/**
 * Crewitts Creek – Website Inbox
 * ------------------------------------------------------------------
 * Receives the website's Contact and Job Application forms, then:
 *   1. saves each submission as a row in this Google Sheet,
 *   2. emails the full details to the restaurant's Gmail,
 *   3. texts the owner's Verizon phone a short "check your email" alert.
 *
 * SETUP (one time, signed in as crewittscreek@gmail.com):
 *   1. Paste this whole file into Extensions > Apps Script (replace everything).
 *   2. Fill in OWNER_CELL below with the owner's 10-digit Verizon number.
 *      (Only stored here, never on the public website.)
 *   3. Pick the function "setup" in the toolbar and click Run. Approve Google's
 *      permission screen. This creates the two tabs and sends a test text + email.
 *   4. Deploy > New deployment > type "Web app":
 *        Execute as: Me    |    Who has access: Anyone
 *      Copy the Web app URL (ends in /exec) and put it in index.html (FORM_ENDPOINT).
 *
 * NOTE: Verizon is shutting down email-to-text (@vtext.com) by March 31, 2027.
 * When that happens the sheet and email keep working; only the text stops.
 */

// ===== SETTINGS ====================================================
const OWNER_EMAIL = 'crewittscreek@gmail.com';
const OWNER_CELL = '';            // e.g. '8595551234' (10 digits, Verizon)
const SMS_GATEWAY = '@vtext.com'; // Verizon email-to-text
const SEND_TEXTS = true;          // set false to turn texts off
// ===================================================================

const TABS = {
  contact: {
    name: 'Contact',
    headers: ['Received', 'Name', 'Email', 'Phone', 'Subject', 'Message', 'Status'],
  },
  application: {
    name: 'Applications',
    headers: ['Received', 'Name', 'Email', 'Phone', 'Position', 'Status'],
  },
};

/** Run once from the editor: creates tabs/headers and sends a test alert. */
function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  Object.keys(TABS).forEach(function (key) {
    const t = TABS[key];
    let sh = ss.getSheetByName(t.name);
    if (!sh) sh = ss.insertSheet(t.name);
    sh.getRange(1, 1, 1, t.headers.length).setValues([t.headers])
      .setFontWeight('bold').setBackground('#0D1F3C').setFontColor('#ffffff');
    sh.setFrozenRows(1);
    const statusCol = t.headers.indexOf('Status') + 1;
    const rule = SpreadsheetApp.newDataValidation()
      .requireValueInList(['New', 'Replied', 'Interview', 'Hired', 'Closed'], true)
      .setAllowInvalid(true).build();
    sh.getRange(2, statusCol, sh.getMaxRows() - 1, 1).setDataValidation(rule);
    sh.autoResizeColumns(1, t.headers.length);
  });
  const blank = ss.getSheetByName('Sheet1');
  if (blank && blank.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(blank);
  sendTest();
}

/** Sends a test email + text so you can confirm alerts arrive. */
function sendTest() {
  notifyOwner_('contact', {
    name: 'Test Submission', email: OWNER_EMAIL, phone: '', subject: 'Setup test',
    message: 'If you got this email and a text on your phone, the website inbox is working.',
  });
  Logger.log('Test sent. Texts enabled: ' + textsReady_() + '. Emails left today: ' + MailApp.getRemainingDailyQuota());
}

/** Website form posts arrive here. */
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    const p = (e && e.parameter) || {};

    // Spam trap: real people never fill the hidden "website" field.
    if (p.website) return json_({ ok: true });

    const type = p.formType === 'application' ? 'application' : 'contact';
    const data = {
      name: clean_(p.name, 100),
      email: clean_(p.email, 150),
      phone: clean_(p.phone, 30),
      subject: clean_(p.subject, 150),
      message: clean_(p.message, 3000),
      position: clean_(p.position, 60),
    };

    if (!data.name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
      return json_({ ok: false, error: 'Please include your name and a valid email.' });
    }
    if (type === 'contact' && !data.message) return json_({ ok: false, error: 'Please include a message.' });
    if (type === 'application' && (!data.phone || !data.position)) {
      return json_({ ok: false, error: 'Please include your phone and the position.' });
    }

    // Simple flood limit: max 3 submissions per email address per 10 minutes.
    const cache = CacheService.getScriptCache();
    const key = 'n_' + data.email.toLowerCase();
    const count = Number(cache.get(key) || 0);
    if (count >= 3) return json_({ ok: false, error: 'Too many submissions. Please call us instead.' });
    cache.put(key, String(count + 1), 600);

    lock.waitLock(15000);
    const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(TABS[type].name);
    if (!sh) throw new Error('Missing tab ' + TABS[type].name + ' — run setup() first.');
    const row = type === 'contact'
      ? [new Date(), data.name, data.email, data.phone, data.subject, data.message, 'New']
      : [new Date(), data.name, data.email, data.phone, data.position, 'New'];
    sh.appendRow(row.map(safeCell_));
    lock.releaseLock();

    try { notifyOwner_(type, data); } catch (mailErr) { console.error('Notify failed', mailErr); }
    return json_({ ok: true });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'Something went wrong. Please call us at (859) 359-5121.' });
  } finally {
    try { lock.releaseLock(); } catch (_) {}
  }
}

/** Lets you open the /exec URL in a browser to check it is live. */
function doGet() {
  return json_({ ok: true, service: 'Crewitts Creek website inbox' });
}

// ----- helpers -----------------------------------------------------

function notifyOwner_(type, d) {
  const isApp = type === 'application';
  const sheetUrl = SpreadsheetApp.getActiveSpreadsheet().getUrl();
  const subject = isApp
    ? 'New job application: ' + d.name + ' (' + d.position + ')'
    : 'New website message: ' + d.name + (d.subject ? ' – ' + d.subject : '');

  const rows = isApp
    ? [['Name', d.name], ['Email', d.email], ['Phone', d.phone], ['Position', d.position]]
    : [['Name', d.name], ['Email', d.email], ['Phone', d.phone || '—'], ['Subject', d.subject || '—'], ['Message', d.message]];

  const html =
    '<div style="font-family:Arial,sans-serif;font-size:14px;color:#1c1c1c">' +
    '<h2 style="color:#0D1F3C;margin:0 0 12px">' + esc_(subject) + '</h2>' +
    '<table cellpadding="6" style="border-collapse:collapse">' +
    rows.map(function (r) {
      return '<tr><td style="font-weight:bold;vertical-align:top;color:#506d88">' + esc_(r[0]) +
        '</td><td style="white-space:pre-wrap">' + esc_(r[1]) + '</td></tr>';
    }).join('') +
    '</table><p style="margin-top:16px">Reply to this email to respond directly to ' + esc_(d.name) + '.<br>' +
    '<a href="' + sheetUrl + '">Open the website inbox sheet</a></p></div>';

  MailApp.sendEmail({
    to: OWNER_EMAIL,
    replyTo: d.email,
    subject: subject,
    htmlBody: html,
    body: rows.map(function (r) { return r[0] + ': ' + r[1]; }).join('\n') + '\n\nSheet: ' + sheetUrl,
    name: 'Crewitts Creek Website',
  });

  if (textsReady_()) {
    const first = d.name.split(' ')[0];
    const lastInitial = (d.name.split(' ')[1] || '').charAt(0);
    const who = first + (lastInitial ? ' ' + lastInitial + '.' : '');
    const text = isApp
      ? 'New job application from ' + who + ' (' + d.position + '). Check your email.'
      : 'New website message from ' + who + (/\.$/.test(who) ? '' : '.') + ' Check your email.';
    MailApp.sendEmail(OWNER_CELL + SMS_GATEWAY, 'Crewitts Creek', text.slice(0, 140));
  }
}

function textsReady_() {
  return SEND_TEXTS && /^\d{10}$/.test(OWNER_CELL);
}

function clean_(v, max) {
  return String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
}

/** Stops values like "=HYPERLINK(...)" from running as spreadsheet formulas. */
function safeCell_(v) {
  return typeof v === 'string' && /^[=+\-@]/.test(v) ? "'" + v : v;
}

function esc_(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
