"""Cut a subject out of a photo and turn it into a paper sticker (free, local: rembg + Pillow).
  python3 cutout.py in.jpg out.png [--outline 14] [--no-shadow] [--max 1400]
out.png = subject only, transparent background, white sticker outline, trimmed to the subject.
First run downloads the u2net model (~170 MB) into ~/.u2net."""
import argparse
from PIL import Image, ImageFilter, ImageOps

def sticker(src, dst, outline=14, max_side=1400, model="u2net"):
    from rembg import remove, new_session
    im = Image.open(src).convert("RGB"); im.thumbnail((max_side, max_side))
    cut = remove(im, session=new_session(model))
    a = cut.split()[-1].point(lambda v: 255 if v > 40 else 0)
    bbox = a.getbbox()
    if not bbox: raise SystemExit("nothing found to cut out")
    pad = outline * 2 + 6
    cut = cut.crop(bbox); a = a.crop(bbox)
    W, H = cut.size[0] + 2 * pad, cut.size[1] + 2 * pad
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    big = Image.new("L", (W, H), 0); big.paste(a, (pad, pad))
    ring = big.filter(ImageFilter.MaxFilter(outline * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("RGBA", (W, H), (250, 248, 240, 255)); base.paste(white, (0, 0), ring)
    base.alpha_composite(cut, (pad, pad))
    base.save(dst)
    return base.size

def card(src, dst, max_side=1400, vintage=False):
    """photo prepared for a torn paper card (resized; optional faded vintage look)."""
    im = Image.open(src).convert("RGB"); im.thumbnail((max_side, max_side))
    if vintage:
        g = ImageOps.grayscale(im); im = ImageOps.colorize(ImageOps.autocontrast(g, 2), "#2a2018", "#f2e6cc")
    im.save(dst, quality=90)
    return im.size

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("src"); p.add_argument("dst"); p.add_argument("--outline", type=int, default=14); p.add_argument("--max", type=int, default=1400)
    a = p.parse_args(); print(sticker(a.src, a.dst, a.outline, a.max))
