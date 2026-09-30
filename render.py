"""Render today's Vestra signature quote to quote.png (repo root).

Usage:
  python render.py              # today's quote (Pacific time) -> quote.png
  python render.py --all DIR    # render every quote to DIR (for proofing)
"""
import sys, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT                    # fonts live in the repo root

# --- Design (display size in the signature is 520 x 80) -------------------
SCALE = 2                       # render at 2x for retina screens
W, H = 520, 80
TEAL, TEAL_DARK, RULE = "#5FDEE3", "#2BC4C9", "#D6F4F5"
INK, BG = "#111114", "#FFFFFF"
SIGNOFF = "\u2014 Vestra, on the state of lending"
TEXT_X = 64                     # left edge of the quote text
SIZES = (15, 14, 13, 12, 11)    # shrink until the quote fits on two lines

# Day 0 of the rotation. Changing this shifts which quote shows on which day.
START = datetime.date(2026, 9, 30)


def font(name, size):
    return ImageFont.truetype(str(FONTS / f"LiberationSans-{name}.ttf"), int(size * SCALE))


def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def render(quote):
    s = SCALE
    img = Image.new("RGB", (W * s, H * s), BG)
    d = ImageDraw.Draw(img)
    d.text((2 * s, -8 * s), "\u201C", font=font("Bold", 72), fill=TEAL)          # big quote mark
    d.line([(52 * s, 12 * s), (52 * s, (H - 12) * s)], fill=RULE, width=s)     # divider
    max_w = (W - TEXT_X - 6) * s
    for size in SIZES:
        f = font("Italic", size)
        lines = wrap(d, quote, f, max_w)
        if len(lines) <= 2:
            break
    fits = len(lines) <= 2
    lh = int(size * 1.35) * s
    top = 4 * s + ((H - 22) * s - lh * len(lines)) // 2
    for i, line in enumerate(lines):
        d.text((TEXT_X * s, top + i * lh), line, font=f, fill=INK)
    d.text((TEXT_X * s, (H - 17) * s), SIGNOFF, font=font("Regular", 9), fill=TEAL_DARK)
    return img, fits


def load_quotes():
    lines = (ROOT / "quotes.txt").read_text(encoding="utf-8").splitlines()
    return [q.strip() for q in lines if q.strip() and not q.strip().startswith("#")]


def todays_quote(quotes):
    today = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).date()
    idx = (today - START).days % len(quotes)
    return idx, quotes[idx], today


if __name__ == "__main__":
    quotes = load_quotes()
    if len(sys.argv) > 2 and sys.argv[1] == "--all":
        out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
        bad = []
        for i, q in enumerate(quotes):
            img, fits = render(q)
            img.save(out / f"{i:03d}.png", optimize=True)
            if not fits:
                bad.append(q)
        print(f"Rendered {len(quotes)} quotes.")
        for q in bad:
            print("TOO LONG (3+ lines):", q)
        sys.exit(1 if bad else 0)

    idx, q, today = todays_quote(quotes)
    img, fits = render(q)
    img.save(ROOT / "quote.png", optimize=True)
    print(f"{today}: quote #{idx + 1} of {len(quotes)}: {q}" + ("" if fits else "  [WARNING: too long]"))
