"""Redraw assets/logo.svg as a transparent PNG.

No SVG renderer is available on this machine (no cairo/rsvg/inkscape), so the
geometry from the SVG is reproduced directly with Pillow at 4x and downsampled.
Coordinates below mirror the SVG's viewBox (600x96) one-for-one.
"""
from PIL import Image, ImageDraw, ImageFont

S = 4                      # supersample factor
W, H = 600, 96
FONT = '/System/Library/Fonts/Menlo.ttc'


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient(size, p0, p1, c0, c1):
    """Linear gradient image, projected along the p0->p1 axis (SVG userSpace)."""
    w, h = size
    img = Image.new('RGB', (w, h))
    px = img.load()
    x0, y0 = p0[0] * S, p0[1] * S
    x1, y1 = p1[0] * S, p1[1] * S
    dx, dy = x1 - x0, y1 - y0
    denom = dx * dx + dy * dy
    for y in range(h):
        for x in range(w):
            t = ((x - x0) * dx + (y - y0) * dy) / denom
            px[x, y] = lerp(c0, c1, min(1.0, max(0.0, t)))
    return img


def rr(d, x, y, w, h, r):
    d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], radius=r * S, fill=255)


def thick_line(d, x0, y0, x1, y1, width):
    d.line([x0 * S, y0 * S, x1 * S, y1 * S], fill=255, width=round(width * S))
    r = width * S / 2
    for cx, cy in ((x0 * S, y0 * S), (x1 * S, y1 * S)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)


def circle(d, cx, cy, r):
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=255)


canvas = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))

# ---- mark (translate(8 16) in the SVG) -------------------------------------
mask = Image.new('L', (W * S, H * S), 0)
d = ImageDraw.Draw(mask)
OX, OY = 8, 16
rr(d, OX + 4, OY + 18, 20, 5, 2.5)
rr(d, OX + 4, OY + 30, 26, 5, 2.5)
rr(d, OX + 4, OY + 42, 16, 5, 2.5)
circle(d, OX + 39, OY + 20.5, 5)
circle(d, OX + 39, OY + 44.5, 5)
circle(d, OX + 54, OY + 32.5, 6)
for a, b in (((43.5, 23.5), (50.5, 29.5)), ((43.5, 41.5), (50.5, 35.5))):
    thick_line(d, OX + a[0], OY + a[1], OX + b[0], OY + b[1], 3)

faint = Image.new('L', (W * S, H * S), 0)
df = ImageDraw.Draw(faint)
for a, b in (((26, 20.5), (34, 20.5)), ((32, 32.5), (47, 32.5)), ((22, 44.5), (34, 44.5))):
    thick_line(df, OX + a[0], OY + a[1], OX + b[0], OY + b[1], 3)
faint = faint.point(lambda v: round(v * 0.7))
mask = Image.eval(Image.merge('L', [mask]), lambda v: v)
mask.paste(faint, (0, 0), Image.eval(faint, lambda v: 255 if v else 0))
d = ImageDraw.Draw(mask)  # re-draw solids over the faint strokes
rr(d, OX + 4, OY + 18, 20, 5, 2.5)
rr(d, OX + 4, OY + 30, 26, 5, 2.5)
rr(d, OX + 4, OY + 42, 16, 5, 2.5)
circle(d, OX + 39, OY + 20.5, 5)
circle(d, OX + 39, OY + 44.5, 5)
circle(d, OX + 54, OY + 32.5, 6)
for a, b in (((43.5, 23.5), (50.5, 29.5)), ((43.5, 41.5), (50.5, 35.5))):
    thick_line(d, OX + a[0], OY + a[1], OX + b[0], OY + b[1], 3)

grad_mark = gradient((W * S, H * S), (12, 16), (68, 80), (0x2D, 0xD4, 0xBF), (0x63, 0x66, 0xF1))
canvas.paste(grad_mark, (0, 0), mask)

# ---- wordmark --------------------------------------------------------------
font = ImageFont.truetype(FONT, 38 * S, index=1)   # Menlo Bold
tmask = Image.new('L', (W * S, H * S), 0)
dt = ImageDraw.Draw(tmask)

x = 90 * S
baseline = 62 * S
tracking = -1 * S
spans = []           # (start_x, end_x) per run, for colouring
for run in ('langgraph', '-declarative'):
    start = x
    for ch in run:
        dt.text((x, baseline), ch, font=font, fill=255, anchor='ls')
        x += round(font.getlength(ch)) + tracking
    spans.append((start, x))

neutral = Image.new('RGB', (W * S, H * S), (0x7C, 0x8A, 0xA0))
grad_text = gradient((W * S, H * S), (300, 30), (580, 70), (0x14, 0xB8, 0xA6), (0x63, 0x66, 0xF1))

for (x0, x1), fill in zip(spans, (neutral, grad_text)):
    sub = Image.new('L', (W * S, H * S), 0)
    sub.paste(tmask.crop((x0, 0, x1, H * S)), (x0, 0))
    canvas.paste(fill, (0, 0), sub)

out = canvas.resize((W * 2, H * 2), Image.LANCZOS)   # 1200x192
out.save('logo.png')
print('wrote logo.png', out.size, 'bbox', out.getbbox())
