from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random, math, os

os.makedirs('/home/claude/crewitts-creek/images', exist_ok=True)

def make_hero(path, w=1200, h=600):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    # Deep navy to dark blue gradient
    for y in range(h):
        t = y / h
        r = int(7 + (13 - 7) * t)
        g = int(17 + (31 - 17) * t)
        b = int(35 + (60 - 35) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Radial glow left
    for i in range(120, 0, -1):
        alpha = int(35 * (i / 120) ** 2)
        x0, y0 = int(w * 0.28) - i * 3, int(h * 0.55) - i * 2
        x1, y1 = int(w * 0.28) + i * 3, int(h * 0.55) + i * 2
        draw.ellipse([x0, y0, x1, y1], fill=(43, 127, 212, alpha))
    # Subtle dots / stars
    random.seed(42)
    for _ in range(180):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(1, 3)
        br = random.randint(60, 160)
        draw.ellipse([x, y, x+s, y+s], fill=(br, br+20, br+40))
    # Creek wave shape at bottom
    pts = []
    for x in range(0, w+1, 4):
        wave = int(30 * math.sin(x / 80) + 20 * math.sin(x / 40 + 1))
        pts.append((x, h - 80 + wave))
    pts.extend([(w, h), (0, h)])
    draw.polygon(pts, fill=(43, 100, 180, 60))
    img.save(path, quality=90)

def make_food(path, w=800, h=500):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    # Warm dark background
    for y in range(h):
        t = y / h
        r = int(20 + 15 * t)
        g = int(12 + 8 * t)
        b = int(8 + 5 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Table surface
    for y in range(int(h*0.45), h):
        t = (y - h*0.45) / (h * 0.55)
        r = int(45 + 30 * t)
        g = int(28 + 18 * t)
        b = int(15 + 10 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Plate
    cx, cy = w//2, int(h*0.52)
    draw.ellipse([cx-160, cy-30, cx+160, cy+30], fill=(220, 215, 205))
    draw.ellipse([cx-155, cy-25, cx+155, cy+25], fill=(235, 230, 220))
    # Burger bun top
    draw.ellipse([cx-90, cy-120, cx+90, cy-20], fill=(180, 110, 40))
    draw.ellipse([cx-85, cy-115, cx+85, cy-25], fill=(200, 130, 55))
    # Sesame seeds
    random.seed(7)
    for _ in range(12):
        sx = cx + random.randint(-60, 60)
        sy = cy - 80 + random.randint(-20, 20)
        draw.ellipse([sx-3, sy-2, sx+3, sy+2], fill=(230, 200, 140))
    # Patty
    draw.ellipse([cx-80, cy-42, cx+80, cy-18], fill=(100, 55, 20))
    # Cheese
    pts = [(cx-82, cy-38), (cx+82, cy-38), (cx+88, cy-28), (cx-88, cy-28)]
    draw.polygon(pts, fill=(210, 160, 40))
    # Lettuce peek
    draw.arc([cx-85, cy-32, cx+85, cy-8], 0, 180, fill=(60, 140, 60), width=8)
    # Tomato
    draw.arc([cx-70, cy-28, cx+70, cy-10], 0, 180, fill=(180, 50, 40), width=6)
    # Bun bottom
    draw.ellipse([cx-85, cy-22, cx+85, cy+8], fill=(190, 120, 45))
    # Fries
    for i in range(7):
        fx = cx - 130 + i * 18
        fh = random.randint(50, 80)
        draw.rectangle([fx, cy-fh, fx+9, cy-5], fill=(210, 165, 55))
        draw.rectangle([fx+1, cy-fh-2, fx+8, cy-fh+4], fill=(220, 180, 70))
    # Warm glow
    for r in range(80, 0, -4):
        a = int(15 * (r/80)**2)
        draw.ellipse([cx-r*2, cy-r, cx+r*2, cy+r], fill=(255, 160, 60, a))
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    img.save(path, quality=90)

def make_bar(path, w=800, h=500):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    # Dark bar atmosphere
    for y in range(h):
        t = y / h
        r = int(8 + 10 * t)
        g = int(14 + 12 * t)
        b = int(28 + 20 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Bar counter
    for y in range(int(h*0.62), h):
        t = (y - h*0.62) / (h*0.38)
        r = int(35 + 20*t); g = int(22 + 12*t); b = int(12 + 8*t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Counter top edge shine
    draw.rectangle([0, int(h*0.62), w, int(h*0.62)+6], fill=(80, 55, 30))
    draw.rectangle([0, int(h*0.62)+6, w, int(h*0.62)+10], fill=(55, 35, 15))
    # Beer taps
    tap_positions = [w//2 - 120, w//2 - 40, w//2 + 40, w//2 + 120]
    for tx in tap_positions:
        ty = int(h * 0.35)
        # Tap base
        draw.rectangle([tx-8, ty+40, tx+8, ty+100], fill=(120, 120, 130))
        # Tap handle
        draw.rectangle([tx-5, ty, tx+5, ty+45], fill=(160, 160, 170))
        draw.ellipse([tx-10, ty-8, tx+10, ty+8], fill=(180, 180, 190))
        draw.ellipse([tx-7, ty-5, tx+7, ty+5], fill=(200, 200, 210))
    # Beer glasses
    glass_x = [w//2 - 170, w//2 + 110]
    for gx in glass_x:
        gy = int(h * 0.5)
        # Glass
        pts = [(gx-22, gy), (gx+22, gy), (gx+18, gy+90), (gx-18, gy+90)]
        draw.polygon(pts, fill=(43, 90, 160, 120))
        # Beer fill
        pts2 = [(gx-19, gy+15), (gx+19, gy+15), (gx+17, gy+88), (gx-17, gy+88)]
        draw.polygon(pts2, fill=(180, 140, 50))
        # Foam
        draw.ellipse([gx-20, gy+6, gx+20, gy+22], fill=(240, 235, 225))
        # Highlight
        draw.rectangle([gx-18, gy+18, gx-13, gy+75], fill=(200, 165, 70))
    # Warm amber bottle glow lights
    for i, lx in enumerate([w*0.15, w*0.5, w*0.82]):
        for r in range(60, 0, -6):
            a = int(12 * (r/60)**1.5)
            ly = h * 0.18
            draw.ellipse([lx-r*1.5, ly-r*0.6, lx+r*1.5, ly+r*0.6], fill=(200, 130, 40, a))
    # Shelves with bottles (background)
    for shelf_y in [int(h*0.12), int(h*0.25)]:
        draw.rectangle([int(w*0.1), shelf_y+35, int(w*0.9), shelf_y+40], fill=(60, 40, 20))
        for bx in range(int(w*0.12), int(w*0.88), 28):
            bh = random.randint(28, 42)
            col = random.choice([(80,120,60),(60,40,20),(100,80,30),(40,60,100)])
            draw.rectangle([bx, shelf_y+35-bh, bx+14, shelf_y+35], fill=col)
            draw.rectangle([bx+4, shelf_y+35-bh-8, bx+10, shelf_y+35-bh], fill=(col[0]//2, col[1]//2, col[2]//2))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img.save(path, quality=90)

def make_interior(path, w=800, h=500):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    # Warm wood-toned walls
    for y in range(h):
        t = y / h
        r = int(28 + 22*t); g = int(18 + 14*t); b = int(10 + 8*t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # Wood plank wall texture
    random.seed(99)
    for i in range(14):
        py = i * 38 - 10
        br = random.randint(-8, 8)
        draw.rectangle([0, py, w, py+2], fill=(20+br, 12+br//2, 6))
        for _ in range(6):
            gx = random.randint(0, w)
            draw.line([(gx, py+2), (gx+random.randint(20,80), py+36)], fill=(22+br, 13, 7), width=1)
    # Floor
    for y in range(int(h*0.7), h):
        t = (y-h*0.7)/(h*0.3)
        r = int(50+20*t); g = int(32+12*t); b = int(18+6*t)
        draw.line([(0,y),(w,y)], fill=(r,g,b))
    # Log slab table
    tx, ty, tw, th2 = w//2-180, int(h*0.62), 360, 55
    draw.ellipse([tx, ty, tx+tw, ty+th2], fill=(75, 48, 22))
    draw.ellipse([tx+5, ty+4, tx+tw-5, ty+th2-4], fill=(90, 58, 28))
    # Wood grain lines on table
    for i in range(8):
        gx = tx + 20 + i * 40
        draw.arc([tx, ty, tx+tw, ty+th2], -10+i*3, 190-i*3, fill=(70, 44, 20), width=1)
    # Chairs (silhouette)
    for cx2 in [tx-60, tx+tw+20]:
        draw.rectangle([cx2, int(h*0.55), cx2+40, int(h*0.72)], fill=(45, 28, 12))
        draw.rectangle([cx2-5, int(h*0.38), cx2+45, int(h*0.56)], fill=(50, 32, 14))
    # Glasses on table
    for gx in [w//2 - 60, w//2 + 30]:
        gy = int(h*0.56)
        pts = [(gx-12, gy), (gx+12, gy), (gx+10, gy+40), (gx-10, gy+40)]
        draw.polygon(pts, fill=(60, 100, 150, 140))
        pts2 = [(gx-10, gy+8), (gx+10, gy+8), (gx+9, gy+38), (gx-9, gy+38)]
        draw.polygon(pts2, fill=(180, 140, 50))
    # Warm Edison bulb glow lights
    light_positions = [w*0.2, w*0.5, w*0.8]
    for lx in light_positions:
        ly = h * 0.08
        # Cord
        draw.line([(int(lx), 0), (int(lx), int(ly+10))], fill=(40, 28, 12), width=2)
        # Bulb glow
        for r in range(70, 0, -5):
            a = int(18 * (r/70)**1.8)
            draw.ellipse([lx-r, ly-r*0.7, lx+r, ly+r*0.7], fill=(220, 160, 60, a))
        draw.ellipse([lx-10, ly-8, lx+10, ly+8], fill=(255, 220, 140))
    # TV screens on wall
    for svx in [int(w*0.15), int(w*0.82)]:
        svy = int(h*0.22)
        draw.rectangle([svx-50, svy-30, svx+50, svy+30], fill=(10,10,18))
        draw.rectangle([svx-46, svy-26, svx+46, svy+26], fill=(15,25,60))
        # Game on screen
        draw.rectangle([svx-40, svy-20, svx+40, svy+20], fill=(20,80,30))
        draw.ellipse([svx-8, svy-8, svx+8, svy+8], fill=(200, 200, 200))
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    img.save(path, quality=90)

make_hero('/home/claude/crewitts-creek/images/hero.jpg')
make_food('/home/claude/crewitts-creek/images/food.jpg')
make_bar('/home/claude/crewitts-creek/images/bar.jpg')
make_interior('/home/claude/crewitts-creek/images/interior.jpg')

print("Images generated:")
import os
for f in os.listdir('/home/claude/crewitts-creek/images'):
    size = os.path.getsize(f'/home/claude/crewitts-creek/images/{f}')
    print(f"  {f}: {size:,} bytes")
