"""Builds favicons, app icons and the social share (Open Graph) image from the VRTX logo.

Run:  python tools/make_brand_assets.py
Writes into public/. Fonts: Inter (pass a folder with --fonts, defaults to Windows fonts / bundled fallbacks).
"""
import argparse
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
BG = (10, 10, 11)
ACCENT = (95, 150, 255)
WHITE = (245, 245, 244)
MUTED = (139, 139, 146)


def clean_mark(src: Path, size: int = 2048) -> Image.Image:
    """The source logo is a small raster; rebuild the white mark as a crisp, smooth alpha mask."""
    im = Image.open(src).convert("L")
    box = im.point(lambda v: 255 if v > 60 else 0).getbbox()
    pad = 4
    crop = im.crop((box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad))
    scale = size / crop.width
    big = crop.resize((size, round(crop.height * scale)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale * .35))
    mask = big.point(lambda v: 255 if v > 128 else 0)
    # supersampled edge: blur a touch, then the final downscale antialiases it
    return mask.filter(ImageFilter.GaussianBlur(1.2))


def place_mark(mask: Image.Image, canvas: int, width_frac: float, bg, radius_frac=0.0, y_shift=0.0) -> Image.Image:
    """Mark centred on a square tile, rendered 4x then downscaled for clean edges."""
    S = canvas * 4
    tile = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    if bg is not None:
        d.rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * radius_frac), fill=bg + (255,))
    mw = int(S * width_frac)
    m = mask.resize((mw, round(mask.height * mw / mask.width)), Image.LANCZOS)
    white = Image.new("RGBA", m.size, WHITE + (255,))
    tile.paste(white, ((S - m.width) // 2, int((S - m.height) / 2 + S * y_shift)), m)
    return tile.resize((canvas, canvas), Image.LANCZOS)


def font(folder: Path, names, size):
    for n in names:
        p = folder / n
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise SystemExit(f"font not found in {folder}: {names}")


def og_image(mask: Image.Image, fonts: Path) -> Image.Image:
    W, H, K = 1200, 630, 2           # drawn at 2x, downscaled at the end
    w, h = W * K, H * K
    img = Image.new("RGB", (w, h), BG)

    # soft blue glow, top right
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse((w * .52, -h * .55, w * 1.25, h * .75), fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    img.paste(Image.new("RGB", (w, h), (30, 52, 105)), (0, 0), glow)

    d = ImageDraw.Draw(img, "RGBA")
    # faint grid
    for x in range(0, w, 120):
        d.line((x, 0, x, h), fill=(255, 255, 255, 7), width=2)
    for y in range(0, h, 120):
        d.line((0, y, w, y), fill=(255, 255, 255, 7), width=2)

    # candles rising on the right, echoing the site's chart
    rnd = random.Random(21)
    price, cs = 100.0, []
    for i in range(26):
        ph = i / 26
        drift = (rnd.random() - .5) * 1.2 if ph < .3 else (-1.4 if ph < .42 else 1.6)
        o = price
        c = o + drift + (rnd.random() - .5) * 1.6
        cs.append((o, max(o, c) + rnd.random(), min(o, c) - rnd.random(), c))
        price = c
    lo, hi = min(c[2] for c in cs), max(c[1] for c in cs)
    x0, x1, y0, y1 = w * .56, w * .94, h * .22, h * .82
    step = (x1 - x0) / len(cs)
    py = lambda v: y0 + (hi - v) / (hi - lo) * (y1 - y0)
    for i, (o, hh, ll, c) in enumerate(cs):
        cx = x0 + step * (i + .5)
        up = c >= o
        a = int(70 + 150 * i / len(cs))
        col = (233, 233, 234, a) if up else (90, 90, 98, a)
        d.line((cx, py(hh), cx, py(ll)), fill=col, width=3)
        d.rounded_rectangle((cx - step * .3, py(max(o, c)), cx + step * .3, max(py(min(o, c)), py(max(o, c)) + 6)), radius=3, fill=col)
    # +2R tag
    tf = font(fonts, ["InterDisplay-SemiBold.otf", "Inter-SemiBold.otf"], 40)
    tx, ty = x1 - 150, py(cs[-1][1]) - 90
    d.rounded_rectangle((tx - 80, ty - 34, tx + 80, ty + 34), radius=34, fill=ACCENT + (255,))
    d.text((tx, ty), "+2R", font=tf, fill=(255, 255, 255), anchor="mm")

    # logo tile + wordmark
    tile = place_mark(mask, 132, .62, (18, 19, 22), radius_frac=.24)
    img.paste(tile, (120, 110), tile)
    d.rounded_rectangle((120, 110, 252, 242), radius=32, outline=(255, 255, 255, 40), width=2)
    wf = font(fonts, ["InterDisplay-SemiBold.otf", "Inter-SemiBold.otf"], 54)
    d.text((290, 176), "V R T X", font=wf, fill=WHITE, anchor="lm")

    # headline
    hf = font(fonts, ["InterDisplay-SemiBold.otf", "Inter-SemiBold.otf"], 132)
    d.text((116, 470), "In pursuit of price.", font=hf, fill=WHITE, anchor="ls")
    d.text((116, 620), "Guided by time.", font=hf, fill=(112, 113, 122), anchor="ls")

    # footer line
    sf = font(fonts, ["Inter-Medium.otf"], 38)
    d.ellipse((120, 1078, 140, 1098), fill=ACCENT + (255,))
    d.text((160, 1088), "Gold trading community  ·  Daily analysis  ·  1-on-1 mentorship", font=sf, fill=MUTED, anchor="lm")

    return img.resize((W, H), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", type=Path, required=True, help="folder with Inter / Inter Display .otf files")
    args = ap.parse_args()

    mask = clean_mark(PUBLIC / "vrtx-icon.png")

    # browser tab icons: dark rounded tile, mark large so it reads at 16px
    ico_sizes = [16, 32, 48]
    tiles = [place_mark(mask, s, .78, BG, radius_frac=.22) for s in ico_sizes]
    tiles[-1].save(PUBLIC / "favicon.ico", sizes=[(s, s) for s in ico_sizes], append_images=tiles[:-1])
    place_mark(mask, 32, .78, BG, radius_frac=.22).save(PUBLIC / "favicon-32x32.png")
    place_mark(mask, 16, .80, BG, radius_frac=.22).save(PUBLIC / "favicon-16x16.png")
    # iOS rounds the corners itself, so a full square
    place_mark(mask, 180, .62, BG).convert("RGB").save(PUBLIC / "apple-touch-icon.png")
    # PWA / Android
    place_mark(mask, 192, .62, BG, radius_frac=.22).save(PUBLIC / "icon-192.png")
    place_mark(mask, 512, .62, BG, radius_frac=.22).save(PUBLIC / "icon-512.png")
    place_mark(mask, 512, .5, BG).convert("RGB").save(PUBLIC / "icon-maskable-512.png")   # mark inside the safe zone

    og_image(mask, args.fonts).save(PUBLIC / "og-image.jpg", quality=90, optimize=True, progressive=True)
    print("wrote favicons, app icons and og-image.jpg to", PUBLIC)


if __name__ == "__main__":
    main()
