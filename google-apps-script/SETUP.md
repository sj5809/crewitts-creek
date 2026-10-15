# Website Inbox Setup (about 10 minutes)

Each website form submission will be saved to a Google Sheet, emailed in full to
crewittscreek@gmail.com, and announced by a short text to the owner's Verizon phone.

Do these steps signed in to **crewittscreek@gmail.com**.

## 1. Create the sheet
1. Go to <https://sheets.new>.
2. Name it **Crewitts Creek – Website Inbox**.

## 2. Add the script
1. In the sheet, open **Extensions → Apps Script**.
2. Delete everything in `Code.gs` and paste in the contents of [`Code.gs`](Code.gs).
3. Near the top, set the owner's 10-digit Verizon cell number:
   `const OWNER_CELL = '8595551234';`
4. Click **Save** (the disk icon).

## 3. Run setup once
1. In the toolbar's function menu pick **setup**, then click **Run**.
2. Google asks for permission. Click **Review permissions**, choose
   crewittscreek@gmail.com, then **Advanced → Go to (project name) → Allow**.
   (The script only uses this sheet and sends email from this account.)
3. It creates the **Contact** and **Applications** tabs and sends a test email plus a
   test text. Confirm both arrive.

## 4. Publish it
1. Click **Deploy → New deployment**, click the gear icon, and pick **Web app**.
2. Set **Execute as: Me** and **Who has access: Anyone**, then click **Deploy**.
3. Copy the **Web app URL** (it ends in `/exec`).

## 5. Connect the website
In `index.html`, find `var FORM_ENDPOINT='';` and paste the URL between the quotes, then push.
Until this is set, the forms open the visitor's email app, as they did before.

## Day to day
- New rows arrive with Status **New**. Change it to Replied, Interview, Hired or Closed.
- Reply to the notification email to answer the person directly.
- To change the script later, edit it, then use **Deploy → Manage deployments → Edit →
  Version: New version** so the website URL stays the same.

## Good to know
- Verizon is shutting down email-to-text (`@vtext.com`), and it stops completely by
  **March 31, 2027**. When that happens, the sheet and emails keep working; only the text stops.
- If texts never arrive, check that email-to-text isn't blocked in the owner's Verizon
  settings, or set `SEND_TEXTS = false`.
- Gmail allows about 100 sends a day, and each submission uses 2, so roughly 50 submissions a day.
