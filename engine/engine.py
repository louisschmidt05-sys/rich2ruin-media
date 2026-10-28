"""Rich 2 Ruin reel engine.
usage: python3 engine.py reels/<id>.json [voice|render|stills t1 t2 ...|all]
A reel JSON = list of lines, each with the narration text and the scene to draw while it plays."""
import json, math, os, subprocess, sys, random
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

import sfx as SFX

W, H, FPS = 1080, 1920, 30
BG = (14, 13, 16)
GOLD = (232, 178, 58)
RED = (215, 38, 61)
CREAM = (244, 237, 225)
GREY = (125, 118, 110)
GREEN = (88, 140, 92)
MONEY = (96, 178, 120)
COLORS = {"gold": GOLD, "red": RED, "cream": CREAM, "green": MONEY, "grey": GREY}
FORMAT_COL = {"THE CRASH": RED, "THE SCAM": MONEY, "RICH TO RUIN": GOLD}

_FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
F_BLACK = os.path.join(_FD, "InterDisplay-Black.otf")
F_BOLD = os.path.join(_FD, "Inter-Bold.otf")
F_SERIF_I = os.path.join(_FD, "Lora-Italic-Variable.ttf")
_fc = {}


def font(p, s):
    s = max(8, int(s))
    if (p, s) not in _fc:
        _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]


VOICE, SPEED, LEAD = "bm_george", 1.06, 0.12
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
CACHE = os.environ.get("R2R_CACHE", os.path.expanduser("~/.cache/rich2ruin"))
MODEL = os.path.join(CACHE, "kokoro-v1.0.onnx")
VOICES = os.path.join(CACHE, "voices-v1.0.bin")


# ---------- easing ----------
def clamp(x):
    return max(0.0, min(1.0, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x)
    return 3 * x * x - 2 * x ** 3


def prog(t, a, d):
    return clamp((t - a) / d)


def lerp(a, b, x):
    return a + (b - a) * x


def mix(c1, c2, x):
    x = clamp(x)
    return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))


def text_c(d, xy, s, f, fill, stroke=0, sfill=BG, anchor="mm"):
    if NO_DUST[0] and stroke == 0 and fill != BG:
        stroke, sfill = 6, (0, 0, 0)
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


def fit_font(d, s, path, size, maxw):
    f = font(path, size)
    while d.textlength(s, font=f) > maxw and size > 20:
        size -= 4
        f = font(path, size)
    return f


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------- shared visuals ----------
def make_vignette():
    yy, xx = np.mgrid[0:H // 4, 0:W // 4]
    r = np.sqrt(((xx - W / 8) / (W / 8)) ** 2 + ((yy - H / 8) / (H / 8)) ** 2)
    a = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6 * 200
    v = Image.fromarray(a.astype("uint8")).resize((W, H), Image.BILINEAR)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    layer.putalpha(v)
    return layer


VIG = make_vignette()
_r = random.Random(7)
DUST = [(_r.random() * W, _r.random() * H, _r.uniform(1.5, 4), _r.uniform(8, 30), _r.random() * 6.28) for _ in range(70)]


NO_DUST = [False]


def dust(d, t, col=GOLD, alpha=1.0):
    if NO_DUST[0]:
        return
    for x, y, r, sp, ph in DUST:
        yy = (y - t * sp) % H
        xx = x + math.sin(t * 0.6 + ph) * 14
        a = (0.35 + 0.35 * math.sin(t * 1.3 + ph)) * alpha
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=mix(BG, col, a))


# ---------- icons ----------
def ic_tulip(d, cx, cy, s, col=RED, flame=None):
    d.line([cx, cy + 40 * s, cx, cy + 190 * s], fill=GREEN, width=max(2, int(9 * s)))
    d.ellipse([cx - 60 * s, cy + 110 * s, cx, cy + 150 * s], fill=GREEN)
    d.ellipse([cx, cy + 90 * s, cx + 55 * s, cy + 128 * s], fill=GREEN)
    dark = mix(col, (0, 0, 0), 0.25)
    d.polygon([(cx - 52 * s, cy - 20 * s), (cx - 40 * s, cy - 75 * s), (cx - 10 * s, cy - 40 * s), (cx, cy + 45 * s), (cx - 45 * s, cy + 30 * s)], fill=dark)
    d.polygon([(cx + 52 * s, cy - 20 * s), (cx + 40 * s, cy - 75 * s), (cx + 10 * s, cy - 40 * s), (cx, cy + 45 * s), (cx + 45 * s, cy + 30 * s)], fill=dark)
    d.polygon([(cx - 30 * s, cy - 30 * s), (cx, cy - 92 * s), (cx + 30 * s, cy - 30 * s), (cx + 25 * s, cy + 40 * s), (cx - 25 * s, cy + 40 * s)], fill=col)
    if flame:
        for k in (-18, 0, 18):
            d.line([(cx + k * s, cy + 35 * s), (cx + k * 1.4 * s, cy - 10 * s), (cx + k * 0.6 * s, cy - 70 * s)], fill=flame, width=max(2, int(7 * s)))


def ic_coin(d, cx, cy, s, sym="$", col=GOLD):
    r = 70 * s
    d.ellipse([cx - r, cy - r + 8 * s, cx + r, cy + r + 8 * s], fill=mix(col, BG, 0.45))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.ellipse([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78], outline=mix(col, BG, 0.3), width=max(2, int(6 * s)))
    text_c(d, (cx, cy + 2 * s), sym, font(F_BLACK, 80 * s), mix(col, BG, 0.45))


def ic_note(d, cx, cy, s, col=MONEY, sym="$"):
    w, h = 190 * s, 95 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=10 * s, fill=col)
    d.rounded_rectangle([cx - w / 2 + 10 * s, cy - h / 2 + 10 * s, cx + w / 2 - 10 * s, cy + h / 2 - 10 * s], radius=6 * s, outline=mix(col, BG, 0.35), width=max(2, int(4 * s)))
    d.ellipse([cx - 28 * s, cy - 28 * s, cx + 28 * s, cy + 28 * s], fill=mix(col, BG, 0.25))
    text_c(d, (cx, cy), sym, font(F_BLACK, 40 * s), mix(col, CREAM, 0.6))


def ic_bank(d, cx, cy, s, col=CREAM):
    d.polygon([(cx - 150 * s, cy - 60 * s), (cx, cy - 140 * s), (cx + 150 * s, cy - 60 * s)], fill=col)
    for i in range(5):
        x = cx - 120 * s + i * 60 * s
        d.rectangle([x - 14 * s, cy - 50 * s, x + 14 * s, cy + 90 * s], fill=col)
    d.rectangle([cx - 160 * s, cy + 95 * s, cx + 160 * s, cy + 120 * s], fill=col)


def ic_ship(d, cx, cy, s, col=CREAM):
    d.polygon([(cx - 150 * s, cy + 30 * s), (cx + 150 * s, cy + 30 * s), (cx + 110 * s, cy + 90 * s), (cx - 110 * s, cy + 90 * s)], fill=mix(col, (120, 80, 50), 0.6))
    d.line([cx, cy + 30 * s, cx, cy - 170 * s], fill=col, width=max(2, int(8 * s)))
    d.polygon([(cx + 6 * s, cy - 160 * s), (cx + 110 * s, cy - 10 * s), (cx + 6 * s, cy - 10 * s)], fill=col)
    d.polygon([(cx - 6 * s, cy - 130 * s), (cx - 90 * s, cy - 10 * s), (cx - 6 * s, cy - 10 * s)], fill=mix(col, BG, 0.2))


def ic_coupon(d, cx, cy, s, col=CREAM):
    w, h = 220 * s, 140 * s
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=col)
    for k in range(12):
        x = cx - w / 2 + k * w / 11
        d.ellipse([x - 6 * s, cy - h / 2 - 6 * s, x + 6 * s, cy - h / 2 + 6 * s], fill=BG)
        d.ellipse([x - 6 * s, cy + h / 2 - 6 * s, x + 6 * s, cy + h / 2 + 6 * s], fill=BG)
    d.rectangle([cx - w / 2 + 16 * s, cy - h / 2 + 18 * s, cx - w / 2 + 80 * s, cy + h / 2 - 18 * s], outline=RED, width=max(2, int(4 * s)))
    for k in range(3):
        y = cy - 30 * s + k * 30 * s
        d.line([cx - 10 * s, y, cx + w / 2 - 20 * s, y], fill=GREY, width=max(2, int(5 * s)))


def ic_bars(d, cx, cy, s, col=GREY):
    d.rectangle([cx - 160 * s, cy - 180 * s, cx + 160 * s, cy + 180 * s], outline=col, width=max(3, int(12 * s)))
    for i in range(1, 6):
        x = cx - 160 * s + i * 320 * s / 6
        d.line([x, cy - 180 * s, x, cy + 180 * s], fill=col, width=max(3, int(12 * s)))


def ic_person(d, cx, cy, s, col=CREAM):
    d.ellipse([cx - 70 * s, cy - 190 * s, cx + 70 * s, cy - 50 * s], fill=col)
    d.pieslice([cx - 150 * s, cy - 30 * s, cx + 150 * s, cy + 270 * s], 180, 360, fill=col)


ICONS = {"tulip": ic_tulip, "coin": ic_coin, "note": ic_note, "bank": ic_bank, "ship": ic_ship,
         "coupon": ic_coupon, "bars": ic_bars, "person": ic_person}


def icon(d, name, cx, cy, s, **kw):
    ICONS[name](d, cx, cy, s, **kw)


# ---------- scenes: fn(img, d, lt, ld, p, ctx) ----------
def sc_year(img, d, lt, ld, p, ctx):
    """Big slam headline + serif subtitle. p: big, sub, color"""
    dust(d, ctx["t"])
    col = COLORS.get(p.get("color", "gold"))
    a = ease(prog(lt, 0.05, 0.3))
    f = fit_font(d, p["big"], F_BLACK, lerp(360, 260, a), W - 120)
    shake = (1 - prog(lt, 0.1, 0.35)) * 10 if lt > 0.1 else 0
    yb = p.get("y", 760)
    text_c(d, (W / 2 + math.sin(lt * 80) * shake, yb), p["big"], f, mix(BG, col, a), stroke=p.get("stroke", 0))
    if p.get("sub"):
        b = ease(prog(lt, 0.45, 0.4))
        fs = fit_font(d, p["sub"], F_SERIF_I, 64, W - 140)
        text_c(d, (W / 2, yb + 200 + (1 - b) * 25), p["sub"], fs, mix(BG, CREAM, b))
    if p.get("icon"):
        c = ease(prog(lt, 0.3, 0.5))
        if c > 0:
            icon(d, p["icon"], W / 2, 470 + (1 - c) * 40, 0.9 * c, **p.get("icon_kw", {}))


def sc_text(img, d, lt, ld, p, ctx):
    """Kinetic headline lines. p: lines [[text, color]], sub, icon"""
    dust(d, ctx["t"], alpha=0.7)
    y = p.get("y", 640)
    if p.get("icon"):
        c = ease(prog(lt, 0.0, 0.45))
        icon(d, p["icon"], W / 2, y - 200 + (1 - c) * 50, p.get("icon_scale", 1.0) * c)
        y += 120
    for i, (txt, col) in enumerate(p["lines"]):
        a = ease(prog(lt, 0.1 + i * 0.35, 0.3))
        f = fit_font(d, txt, F_BLACK, p.get("size", 110), W - 120)
        text_c(d, (W / 2 + (1 - a) * 60, y + i * (f.size + 30)), txt, f, mix(BG, COLORS[col], a))
    if p.get("sub"):
        b = ease(prog(lt, 0.2 + len(p["lines"]) * 0.35, 0.4))
        fs = fit_font(d, p["sub"], F_SERIF_I, 56, W - 140)
        text_c(d, (W / 2, y + len(p["lines"]) * (p.get("size", 110) + 30) + 30), p["sub"], fs, mix(BG, CREAM, b))


def fmt_num(v, dec):
    return f"{v:,.{dec}f}"


def sc_stat(img, d, lt, ld, p, ctx):
    """Counter. p: label, value, from, prefix, suffix, dec, color, sub, icon"""
    dust(d, ctx["t"], alpha=0.8)
    col = COLORS.get(p.get("color", "gold"))
    a = ease(prog(lt, 0, 0.3))
    if p.get("label"):
        fl = fit_font(d, p["label"], F_BLACK, 66, W - 140)
        text_c(d, (W / 2, p.get("label_y", 300 if p.get("icon") else 600)), p["label"], fl, mix(BG, CREAM, a))
    if p.get("icon"):
        g = ease(prog(lt, 0, 0.5))
        for r in range(300, 100, -40):
            d.ellipse([W / 2 - r, 690 - r, W / 2 + r, 690 + r], fill=mix(BG, mix(BG, col, 0.35), g * (1 - r / 380) * 1.2))
        kw = {"flame": RED, "col": (236, 232, 226)} if p["icon"] == "tulip_flamed" else {}
        name = "tulip" if p["icon"] == "tulip_flamed" else p["icon"]
        icon(d, name, W / 2, 650 if name == "tulip" else 690, lerp(1.5, 1.8, ease_io(prog(lt, 0, ld))) * g, **kw)
    dur = min(1.6, ld * 0.55)
    c = ease_io(prog(lt, 0.25, dur))
    v0, v1 = p.get("from", 0), p["value"]
    v = lerp(v0, v1, c)
    pulse = 1 + 0.07 * math.sin(clamp((lt - 0.25 - dur) / 0.3) * math.pi)
    s = f'{p.get("prefix", "")}{fmt_num(v, p.get("dec", 0))}{p.get("suffix", "")}'
    f = fit_font(d, s, F_BLACK, 170 * pulse, W - 100)
    y = p.get("y", 1150 if p.get("icon") else 790)
    text_c(d, (W / 2, y), s, f, col if c >= 1 else CREAM, stroke=4)
    if p.get("sub"):
        b = ease(prog(lt, 0.4, 0.4))
        fs = fit_font(d, p["sub"], F_BOLD, 40, W - 140)
        text_c(d, (W / 2, y + 115), p["sub"], fs, mix(BG, GREY, b))


def sc_compare(img, d, lt, ld, p, ctx):
    """1 small thing vs long bar. p: a, b1, b2, icon"""
    dust(d, ctx["t"])
    fl = font(F_BOLD, 46)
    y1, y2 = 650, 900
    q = ease(prog(lt, 0, 0.4))
    icon(d, p.get("icon", "coin"), 190, y1 + 10, 0.55 * q)
    d.text((300, y1), p["a"], font=fl, fill=mix(BG, CREAM, q), anchor="lm")
    r = ease(prog(lt, 0.6, ld * 0.6))
    e = ease(prog(lt, 0.4, 0.4))
    d.text((140, y2 - 60), p["b1"], font=fl, fill=mix(BG, CREAM, e), anchor="lm")
    d.text((140, y2 - 10), p["b2"], font=fl, fill=mix(BG, CREAM, e), anchor="lm")
    d.rounded_rectangle([140, y2 + 30, max(150, 140 + 800 * r), y2 + 100], radius=14, fill=GOLD)
    for i in range(int(12 * r)):
        cx = 175 + i * 66
        d.ellipse([cx - 18, y2 + 47, cx + 18, y2 + 83], outline=BG, width=4)


def sc_icons(img, d, lt, ld, p, ctx):
    """Grid of icons popping. p: icon, rows, cols, title, colors, badge"""
    dust(d, ctx["t"], alpha=0.6)
    if p.get("title"):
        a = ease(prog(lt, 0, 0.4))
        f = fit_font(d, p["title"], F_SERIF_I, 64, W - 140)
        text_c(d, (W / 2, 330 + (1 - a) * 25), p["title"], f, mix(BG, GOLD, a))
    rows, cols = p.get("rows", 3), p.get("cols", 4)
    cl = [COLORS.get(c, c) if isinstance(c, str) else tuple(c) for c in p.get("colors", ["red"])]
    sc = p.get("scale", 0.6)
    for r_ in range(rows):
        for c_ in range(cols):
            k = r_ * cols + c_
            pp = ease(prog(lt, 0.1 + k * 0.06, 0.4))
            if pp <= 0:
                continue
            cx = W / (cols + 1) * (c_ + 1) + (W / (cols + 1) / 2 if r_ % 2 and p["icon"] == "tulip" else 0)
            cx = min(cx, W - 90)
            cy = p.get("y0", 560) + r_ * p.get("dy", 220) + (1 - pp) * 100
            sway = math.sin(ctx["t"] * 2 + k) * 6
            kw = {"col": cl[k % len(cl)]} if p["icon"] in ("tulip", "coin", "note") else {}
            if p["icon"] in ("coin", "note") and p.get("sym"):
                kw["sym"] = p["sym"]
            icon(d, p["icon"], cx + sway, cy, sc * pp, **kw)
    if p.get("badge"):
        q = ease(prog(lt, ld * 0.35, 0.35))
        if q > 0:
            fb = font(F_BLACK, 70)
            bw = (d.textlength(p["badge"], font=fb) + 90) * q
            d.rounded_rectangle([W / 2 - bw / 2, 1180, W / 2 + bw / 2, 1290], radius=20, fill=GOLD)
            if q > 0.7:
                text_c(d, (W / 2, 1235), p["badge"], fb, BG)


def sc_chart(img, d, lt, ld, p, ctx):
    """Line chart. p: points [[label, value]], show_from, show_to (indices, reveal animates),
    red_from (index where line turns red), title, unit, illustrative, big (overlay text), big_color"""
    pts = p["points"]
    x0, x1, y0, y1 = 130, 950, 1150, 420
    vmax = max(v for _, v in pts) * 1.08
    vmin = 0
    n = len(pts) - 1
    a_, b_ = p.get("show_from", 0), p.get("show_to", n)
    rev = lerp(a_, b_, ease_io(prog(lt, 0.15, max(0.6, ld * 0.7))))
    red_from = p.get("red_from", 99)
    plunge = rev > red_from
    flash = 0
    if plunge and p.get("flash", True):
        tcross = 0.15 + (red_from - a_) / max(1e-6, b_ - a_) * max(0.6, ld * 0.7)
        flash = max(0.0, 1 - abs(lt - tcross - 0.15) / 0.35)
        if flash > 0:
            img.paste(mix(BG, (90, 10, 20), flash * 0.7), [0, 0, W, H])
            d = ImageDraw.Draw(img)
    sh = flash * 16
    ox, oy = math.sin(lt * 70) * sh, math.cos(lt * 53) * sh
    dust(d, ctx["t"], col=RED if plunge else GOLD, alpha=0.5)
    axis = mix(BG, GREY, 0.7)
    d.line([x0 + ox, y0 + oy, x1 + ox, y0 + oy], fill=axis, width=4)
    d.line([x0 + ox, y0 + oy, x0 + ox, y1 - 30 + oy], fill=axis, width=4)
    for k in range(1, 4):
        yy = lerp(y0, y1, k / 4)
        d.line([x0 + ox, yy + oy, x1 + ox, yy + oy], fill=mix(BG, GREY, 0.18), width=2)
    fs = font(F_BOLD, 28)
    X = lambda i: lerp(x0 + 30, x1 - 30, i / max(1, n)) + ox
    Y = lambda v: lerp(y0, y1, (v - vmin) / (vmax - vmin)) + oy
    for i, (lab, v) in enumerate(pts):
        if lab and (i == 0 or i == n or p.get("all_labels")):
            d.text((X(i), y0 + 40 + oy), lab, font=fs, fill=GREY, anchor="mm")
    if p.get("title"):
        text_c(d, (W / 2 + ox, 270), p["title"], fit_font(d, p["title"], F_BLACK, 64, W - 140), CREAM)
    if p.get("sub"):
        text_c(d, (W / 2, 345), p["sub"], fit_font(d, p["sub"], F_SERIF_I, 46, W - 140), GOLD)
    if p.get("illustrative"):
        d.text((x1 + ox, y1 - 22 + oy), "ILLUSTRATIVE CURVE", font=font(F_BOLD, 24), fill=GREY, anchor="rm")
    elif p.get("source"):
        d.text((x1 + ox, y1 - 22 + oy), p["source"], font=font(F_BOLD, 24), fill=GREY, anchor="rm")
    # build polyline with smooth subdivision
    line_pts = []
    steps = 24
    for i in range(n):
        if i > rev:
            break
        for s_ in range(steps):
            u = i + s_ / steps
            if u > rev:
                break
            v0, v1v = pts[i][1], pts[i + 1][1]
            if p.get("curve") == "exp":
                v = v0 + (v1v - v0) * ((s_ / steps) ** 3 if v1v > v0 else ease(s_ / steps))
            else:
                v = lerp(v0, v1v, ease_io(s_ / steps))
            line_pts.append((u, X(u), Y(v)))
    if rev >= n:
        line_pts.append((n, X(n), Y(pts[n][1])))
    else:
        i = int(rev)
        if i < n:
            fr = rev - i
            v0, v1v = pts[i][1], pts[i + 1][1]
            v = v0 + (v1v - v0) * (fr ** 3 if (p.get("curve") == "exp" and v1v > v0) else ease_io(fr))
            line_pts.append((rev, X(rev), Y(v)))
    if len(line_pts) > 1:
        gold = [(x, y) for u, x, y in line_pts if u <= red_from + 1e-6]
        red = [(x, y) for u, x, y in line_pts if u >= red_from - 1e-6]
        for seg, col in ((gold, GOLD), (red, RED)):
            if len(seg) > 1:
                d.line(seg, fill=mix(col, (0, 0, 0), 0.5), width=22, joint="curve")
                d.line(seg, fill=col, width=12, joint="curve")
        u, hx, hy = line_pts[-1]
        col = RED if u > red_from else GOLD
        d.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], fill=col)
        if p.get("value_tags", True):
            idx = min(n, int(round(u))) if abs(u - round(u)) < 0.04 else None
            for i in range(0, int(u) + 1):
                if i in p.get("tag", []):
                    vt = pts[i][1]
                    lab = f'{p.get("prefix", "")}{fmt_num(vt, p.get("dec", 0))}{p.get("suffix", "")}'
                    tc = RED if i > red_from else GOLD
                    d.text((X(i), Y(vt) - 45), lab, font=font(F_BLACK, 44), fill=tc, anchor="mm", stroke_width=4, stroke_fill=BG)
    if p.get("big"):
        q = ease(prog(lt, p.get("big_at", ld * 0.6), 0.25))
        if q > 0:
            fb = fit_font(d, p["big"], F_BLACK, lerp(190, 130, q), W - 100)
            text_c(d, (W / 2 + ox, 1270 + oy), p["big"], fb, mix(BG, COLORS[p.get("big_color", "red")], q), stroke=5)


def sc_myth(img, d, lt, ld, p, ctx):
    """p: kicker, myth, reality, sub, source"""
    dust(d, ctx["t"], alpha=0.6)
    a = ease(prog(lt, 0, 0.3))
    text_c(d, (W / 2, 330), p.get("kicker", "THE TWIST"), font(F_BLACK, 76), mix(BG, GOLD, a))
    fm = fit_font(d, p["myth"], F_BLACK, 64, W - 200)
    q = ease(prog(lt, 0.4, 0.3))
    text_c(d, (W / 2, 620), p["myth"], fm, mix(BG, CREAM, q))
    s = ease(prog(lt, 1.0, 0.3))
    if s > 0:
        w = d.textlength(p["myth"], font=fm) / 2 + 30
        d.line([W / 2 - w, 620, W / 2 - w + 2 * w * s, 620], fill=RED, width=14)
        text_c(d, (W / 2, 535), "MYTH", font(F_BOLD, 40), mix(BG, RED, s))
    r = ease(prog(lt, 1.6, 0.35))
    if r > 0:
        fr = fit_font(d, p["reality"], F_BLACK, 120, W - 120)
        text_c(d, (W / 2, 880 + (1 - r) * 30), p["reality"], fr, mix(BG, GOLD, r))
        if p.get("sub"):
            text_c(d, (W / 2, 1010 + (1 - r) * 30), p["sub"], fit_font(d, p["sub"], F_SERIF_I, 58, W - 140), mix(BG, CREAM, r))
        if p.get("source"):
            text_c(d, (W / 2, 1100), p["source"], font(F_BOLD, 32), mix(BG, GREY, r))


def sc_name(img, d, lt, ld, p, ctx):
    """Name card with generic silhouette (no real likeness). p: name, sub, years, tag"""
    dust(d, ctx["t"], alpha=0.6)
    a = ease(prog(lt, 0, 0.45))
    for r in range(330, 110, -40):
        d.ellipse([W / 2 - r, 640 - r, W / 2 + r, 640 + r], fill=mix(BG, (55, 40, 25), a * (1 - r / 360) * 1.3))
    icon(d, "person", W / 2, 700 + (1 - a) * 40, 1.25 * a, col=mix(BG, (60, 56, 52), a))
    text_c(d, (W / 2, 640), "?", font(F_BLACK, 130), mix(BG, mix(BG, GOLD, 0.35), a)) if p.get("mystery") else None
    b = ease(prog(lt, 0.25, 0.35))
    fn = fit_font(d, p["name"], F_BLACK, 120, W - 100)
    text_c(d, (W / 2 + (1 - b) * 50, 1040), p["name"], fn, mix(BG, CREAM, b))
    if p.get("sub"):
        c = ease(prog(lt, 0.55, 0.35))
        text_c(d, (W / 2, 1150), p["sub"], fit_font(d, p["sub"], F_SERIF_I, 56, W - 140), mix(BG, GOLD, c))
    if p.get("tag"):
        e = ease(prog(lt, 0.8, 0.3))
        fb = font(F_BOLD, 38)
        bw = d.textlength(p["tag"], font=fb) + 60
        d.rounded_rectangle([W / 2 - bw / 2, 1225, W / 2 + bw / 2, 1290], radius=30, fill=mix(BG, RED, e))
        text_c(d, (W / 2, 1258), p["tag"], fb, mix(RED, CREAM, e))


def sc_news(img, d, lt, ld, p, ctx):
    """Newspaper card (our own wording). p: masthead, headline, date"""
    dust(d, ctx["t"], alpha=0.4)
    a = ease(prog(lt, 0, 0.35))
    rot_y = (1 - a) * 300
    paper = (232, 224, 205)
    x0, x1, y0 = 110, 970, 380 + rot_y
    d.rectangle([x0 + 14, y0 + 14, x1 + 14, y0 + 780], fill=(5, 5, 6))
    d.rectangle([x0, y0, x1, y0 + 780], fill=mix(BG, paper, a))
    ink = (25, 22, 20)
    text_c(d, (W / 2, y0 + 70), p.get("masthead", "THE DAILY LEDGER"), font(F_SERIF_I, 64), mix(BG, ink, a))
    d.line([x0 + 30, y0 + 120, x1 - 30, y0 + 120], fill=ink, width=4)
    d.text((x0 + 30, y0 + 145), p.get("date", ""), font=font(F_BOLD, 28), fill=ink, anchor="lm")
    d.line([x0 + 30, y0 + 170, x1 - 30, y0 + 170], fill=ink, width=2)
    fh = font(F_BLACK, 104)
    lines = wrap(d, p["headline"], fh, x1 - x0 - 80)
    while len(lines) > 3:
        fh = font(F_BLACK, fh.size - 10)
        lines = wrap(d, p["headline"], fh, x1 - x0 - 80)
    for i, ln in enumerate(lines):
        text_c(d, (W / 2, y0 + 270 + i * (fh.size + 14)), ln, fh, ink)
    for k in range(6):
        yy = y0 + 560 + k * 32
        d.line([x0 + 40, yy, x0 + 40 + (x1 - x0 - 80) * (0.95 if k % 3 else 0.7), yy], fill=mix(paper, ink, 0.35), width=10)


def sc_outro(img, d, lt, ld, p, ctx):
    dust(d, ctx["t"])
    a = ease(prog(lt, 0, 0.5))
    r = lerp(40, 190, a)
    cx, cy = W / 2, 640
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=12)
    d.arc([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], 200, 250, fill=CREAM, width=12)
    if a > 0.6:
        d.line([(cx + 20, cy - r + 10), (cx - 10, cy - 30), (cx + 30, cy + 10), (cx - 5, cy + r - 10)], fill=RED, width=10)
    text_c(d, (W / 2, 960), "RICH 2 RUIN", font(F_BLACK, 120), mix(BG, CREAM, a))
    q = ease(prog(lt, 0.5, 0.4))
    text_c(d, (W / 2, 1075), "History's greatest crashes, in 60 seconds", font(F_SERIF_I, 44), mix(BG, GOLD, q))
    b = ease(prog(lt, 0.9, 0.3))
    if b > 0:
        d.rounded_rectangle([W / 2 - 200, 1190, W / 2 + 200, 1290], radius=50, fill=mix(BG, RED, b))
        text_c(d, (W / 2, 1240), "FOLLOW", font(F_BLACK, 56), mix(RED, CREAM, b))



# ---------- archive photo scene ----------
MEDIA = BASE
_imgcache = {}


def load_src(path, mode):
    key = (path, mode)
    if key not in _imgcache:
        im = Image.open(os.path.join(MEDIA, path)).convert("RGB")
        if mode == "fit":
            from PIL import ImageFilter, ImageEnhance
            bg = im.copy()
            s = max(W / bg.width, H / bg.height)
            bg = bg.resize((int(bg.width * s) + 2, int(bg.height * s) + 2), Image.BILINEAR)
            bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
            bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(0.45)
            _imgcache[key] = (im, bg)
        else:
            _imgcache[key] = (im, None)
    return _imgcache[key]


def _shade():
    yy = np.linspace(0, 1, H)[:, None]
    a = np.clip(0.30 + 0.55 * np.clip((yy - 0.55) / 0.35, 0, 1) + 0.35 * np.clip((0.22 - yy) / 0.22, 0, 1), 0, 0.92)
    a = np.repeat((a * 255).astype("uint8"), W, axis=1)
    lay = Image.new("RGBA", (W, H), (8, 7, 9, 255))
    lay.putalpha(Image.fromarray(a))
    return lay


SHADE = _shade()


def sc_photo(img, d, lt, ld, p, ctx):
    """Archive image with slow camera move. p: img, mode (cover|fit), from [cx,cy,z], to [cx,cy,z],
    bw, tint, credit, overlay (another scene spec drawn on top, without dust)"""
    src, bg = load_src(p["img"], p.get("mode", "cover"))
    k = ease_io(prog(lt, 0, ld + 0.4))
    f0, f1 = p.get("from", [0.5, 0.5, 1.0]), p.get("to", [0.5, 0.5, 1.15])
    cx, cy, z = (lerp(a, b, k) for a, b in zip(f0, f1))
    if p.get("mode") == "fit":
        base = bg.copy()
        sw = W * 0.96 * z
        sh = sw * src.height / src.width
        fg = src.resize((int(sw), int(sh)), Image.BILINEAR)
        x = int(W / 2 - sw * cx)
        y = int(p.get("y", 760) - sh * (cy - 0.5) - sh / 2)
        base.paste(fg, (x, y))
        frame = base
    else:
        vh = src.height / z
        vw = vh * W / H
        if vw > src.width:
            vw = src.width
            vh = vw * H / W
        x0 = min(max(cx * src.width - vw / 2, 0), src.width - vw)
        y0 = min(max(cy * src.height - vh / 2, 0), src.height - vh)
        frame = src.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + vw, y0 + vh))
    if p.get("bw"):
        frame = frame.convert("L").convert("RGB")
    if p.get("tint"):
        frame = Image.blend(frame, Image.new("RGB", (W, H), COLORS[p["tint"]]), 0.22)
    dim = p.get("dim", 0.15)
    if dim:
        frame = Image.blend(frame, Image.new("RGB", (W, H), (0, 0, 0)), dim)
    fl = p.get("flash")
    if fl:
        a = max(0.0, 1 - abs(lt - fl) / 0.3)
        if a > 0:
            frame = Image.blend(frame, Image.new("RGB", (W, H), (120, 10, 25)), a * 0.6)
    fi = ease(prog(lt, 0, 0.35)) if p.get("fade_in", True) else 1
    if fi < 1:
        frame = Image.blend(Image.new("RGB", (W, H), BG), frame, fi)
    fr = frame.convert("RGBA")
    fr.alpha_composite(SHADE)
    img.paste(fr.convert("RGB"))
    d = ImageDraw.Draw(img)
    if p.get("credit"):
        d.text((W / 2, 240), p["credit"], font=font(F_BOLD, 22), fill=(190, 180, 170), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
    ov = p.get("overlay")
    if ov:
        NO_DUST[0] = True
        try:
            SCENES[ov["type"]](img, d, lt, ld, ov, ctx)
        finally:
            NO_DUST[0] = False


SCENES = {"photo": sc_photo, "year": sc_year, "text": sc_text, "stat": sc_stat, "compare": sc_compare, "icons": sc_icons,
          "chart": sc_chart, "myth": sc_myth, "name": sc_name, "news": sc_news, "outro": sc_outro}

# default sound per scene type (played at scene start + offset)
AUTO_SFX = {"photo": [("whoosh", 0.0)], "year": [("slam", 0.05)], "text": [("whoosh", 0.0)], "stat": [("whoosh", 0.0)],
            "compare": [("whoosh", 0.0)], "icons": [("whoosh", 0.0)], "chart": [("whoosh", 0.0)],
            "myth": [("whoosh", 0.0), ("paper", 1.0)], "name": [("whoosh_down", 0.0), ("impact", 0.3)],
            "news": [("paper", 0.0), ("impact", 0.3)], "outro": [("whoosh", 0.0), ("ding", 0.9)]}
GAIN = {"whoosh": 0.22, "whoosh_down": 0.22, "slam": 0.5, "impact": 0.45, "boom": 0.6, "crash": 0.58,
        "riser": 0.28, "ding": 0.55, "cash": 0.6, "paper": 0.3}


# ---------- pipeline ----------
class Reel:
    def __init__(self, path):
        self.path = path
        self.spec = json.load(open(path))
        self.id = self.spec["id"]
        self.dir = os.path.join(BASE, "build", self.id)
        os.makedirs(self.dir, exist_ok=True)
        tp = os.path.join(self.dir, "timing.json")
        self.timing = json.load(open(tp)) if os.path.exists(tp) else None

    # 1. voice
    def voice(self):
        from kokoro_onnx import Kokoro
        k = Kokoro(MODEL, VOICES)
        sr_ = 24000
        gap = np.zeros(int(0.2 * sr_), np.float32)
        out = [np.zeros(int(0.3 * sr_), np.float32)]
        t, timing = 0.3, []
        for i, ln in enumerate(self.spec["lines"]):
            a, sr = k.create(ln["say"] if "say" in ln else ln["text"], voice=VOICE, speed=SPEED, lang="en-gb")
            a = np.asarray(a, np.float32)
            idx = np.where(np.abs(a) > 0.01)[0]
            a = a[max(idx[0] - 600, 0): idx[-1] + 1200]
            dur = len(a) / sr_
            timing.append({"i": i, "start": t, "end": t + dur})
            pause = ln.get("pause", 0.2)
            out += [a, np.zeros(int(pause * sr_), np.float32)]
            t += dur + pause
        out.append(np.zeros(int(1.4 * sr_), np.float32))
        full = np.concatenate(out)
        full = full / (np.abs(full).max() + 1e-9) * 0.9
        raw = os.path.join(self.dir, "voice_raw.wav")
        sf.write(raw, full, sr_)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                        "bass=g=3:f=140,treble=g=-2:f=6500,aecho=0.8:0.6:35:0.12,acompressor=threshold=0.1:ratio=3:attack=10:release=150",
                        "-ar", "44100", "-ac", "1", os.path.join(self.dir, "voice.wav")], check=True)
        self.timing = {"lines": timing, "total": len(full) / sr_}
        json.dump(self.timing, open(os.path.join(self.dir, "timing.json"), "w"), indent=1)
        self._words()

    # scene windows
    def windows(self):
        L = self.timing["lines"]
        tot = self.timing["total"]
        wins = []
        for i, ln in enumerate(L):
            a = 0.0 if i == 0 else L[i]["start"] - LEAD
            b = tot if i == len(L) - 1 else L[i + 1]["start"] - LEAD
            wins.append((a, b))
        return wins

    def _words(self):
        groups = []
        for ln, tm in zip(self.spec["lines"], self.timing["lines"]):
            ws = ln["text"].split()
            tc = sum(len(w) + 2 for w in ws)
            t0, dur = tm["start"], tm["end"] - tm["start"]
            acc, cur, gs = 0, [], []
            for w in ws:
                cur.append(w)
                if len(cur) == 3 or w.endswith((".", ",", "?", ":", "!")):
                    gs.append(cur)
                    cur = []
            if cur:
                gs.append(cur)
            for g in gs:
                gw = []
                for w in g:
                    s0 = t0 + dur * acc / tc
                    acc += len(w) + 2
                    gw.append((w, s0, t0 + dur * acc / tc))
                groups.append(gw)
        self.words = groups

    def caption(self, img, t):
        grp = None
        for g in self.words:
            if g[0][1] - 0.05 <= t < g[-1][2] + 0.12:
                grp = g
        if not grp:
            return
        d = ImageDraw.Draw(img)
        words = [w.upper() for w, _, _ in grp]
        f = font(F_BLACK, 76)
        while sum(d.textlength(w + " ", font=f) for w in words) > W - 80 and f.size > 40:
            f = font(F_BLACK, f.size - 4)
        widths = [d.textlength(w + " ", font=f) for w in words]
        x = W / 2 - (sum(widths) - d.textlength(" ", font=f)) / 2
        pop = ease(prog(t, grp[0][1] - 0.05, 0.12))
        for (w, s0, s1), word, wd in zip(grp, words, widths):
            act = s0 <= t < s1 + 0.05
            d.text((x, 1400 + (-6 if act else 0) + (1 - pop) * 20), word, font=f, fill=GOLD if act else CREAM,
                   anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
            x += wd

    def chrome(self, d, t):
        d.text((W / 2, 140), "RICH  2  RUIN", font=font(F_BOLD, 30), fill=mix(BG, CREAM, 0.55), anchor="mm")
        fmt = self.spec.get("format")
        if fmt:
            col = FORMAT_COL.get(fmt, GOLD)
            fb = font(F_BOLD, 24)
            w = d.textlength(fmt, font=fb) + 36
            d.rounded_rectangle([W / 2 - w / 2, 172, W / 2 + w / 2, 210], radius=19, outline=mix(BG, col, 0.8), width=2)
            d.text((W / 2, 191), fmt, font=fb, fill=mix(BG, col, 0.9), anchor="mm")

    def frame(self, t, wins=None):
        wins = wins or self.windows()
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        for i, (a, b) in enumerate(wins):
            if a <= t < b or (i == len(wins) - 1 and t >= a):
                ln = self.spec["lines"][i]
                sc = ln["scene"]
                ld = self.timing["lines"][i]["end"] - a
                SCENES[sc["type"]](img, d, t - a, ld, sc, {"t": t, "i": i})
                break
        img = img.convert("RGBA")
        img.alpha_composite(VIG)
        img = img.convert("RGB")
        d = ImageDraw.Draw(img)
        self.chrome(d, t)
        self.caption(img, t)
        return img

    # 2. audio: music + sfx + voice
    def audio(self):
        wins = self.windows()
        tot = self.timing["total"]
        n = int(tot * SFX.SR)
        fx = np.zeros(n)
        accents = []
        drop = twist = None

        def put(name, at):
            s = SFX.LIB[name]()
            s = s / (np.abs(s).max() + 1e-9) * GAIN[name]
            i = int(at * SFX.SR)
            if 0 <= i < n:
                j = min(n, i + len(s))
                fx[i:j] += s[: j - i]

        for i, ln in enumerate(self.spec["lines"]):
            a, _ = wins[i]
            sc = ln["scene"]
            events = ln.get("sfx")
            if events is None:
                events = AUTO_SFX.get(sc["type"], [])
            for name, off in events:
                put(name, a + off)
            if ln.get("big"):
                at = a + ln.get("big_at", 0.0)
                put("riser", max(0, at - 1.3))
                put(ln.get("big_sfx", "boom"), at)
                accents.append(at)
            if ln.get("drop"):
                drop = a + ln.get("big_at", 0.0)
            if ln.get("twist"):
                twist = a
            if sc["type"] == "stat":
                dur = min(1.6, (self.timing["lines"][i]["end"] - a) * 0.55)
                tk = SFX.ticks(dur)
                tk = tk / (np.abs(tk).max() + 1e-9) * 0.12
                s0 = int((a + 0.25) * SFX.SR)
                fx[s0:s0 + len(tk)] += tk[: max(0, n - s0)]
                if not ln.get("big"):
                    put(sc.get("end_sfx", "ding"), a + 0.25 + dur)
        m = SFX.music(tot, drop, twist, accents)
        fx_st = np.stack([fx, fx], 1)
        sf.write(os.path.join(self.dir, "music.wav"), np.stack([m, m], 1).astype(np.float32), SFX.SR)
        sf.write(os.path.join(self.dir, "fx.wav"), fx_st.astype(np.float32), SFX.SR)
        D = self.dir
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/voice.wav", "-i", f"{D}/music.wav", "-i", f"{D}/fx.wav",
                        "-filter_complex",
                        "[0:a]aresample=44100,aformat=channel_layouts=stereo,asplit=2[v1][v2];"
                        "[1:a]volume=0.30[m];[m][v2]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[md];"
                        "[2:a]volume=0.65[f];"
                        "[v1][md][f]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                        "-map", "[a]", "-ar", "44100", f"{D}/mix.wav"], check=True)

    # 3. video
    def render(self, only=None):
        wins = self.windows()
        sdir = os.path.join(self.dir, "scenes")
        os.makedirs(sdir, exist_ok=True)
        files = []
        for i, (a, b) in enumerate(wins):
            out = os.path.join(sdir, f"{i:02d}.mp4")
            files.append(out)
            if only is not None and i not in only and os.path.exists(out):
                continue
            tmp = out.replace(".mp4", ".tmp.mp4")
            n0, n1 = round(a * FPS), round(b * FPS)
            p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                  "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                                  "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
            for k in range(n0, n1):
                p.stdin.write(self.frame(k / FPS, wins).tobytes())
            p.stdin.close()
            if p.wait() == 0:
                os.replace(tmp, out)
        lst = os.path.join(self.dir, "list.txt")
        open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
        vid = os.path.join(self.dir, "video.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
        final = os.path.join(BASE, "reels", f"{self.id}.mp4")
        os.makedirs(os.path.dirname(final), exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", os.path.join(self.dir, "mix.wav"),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
        return final

    def stills(self, ts):
        if not hasattr(self, "words"):
            self._words()
        os.makedirs(os.path.join(self.dir, "stills"), exist_ok=True)
        ims = [self.frame(float(t)).resize((270, 480)) for t in ts]
        sheet = Image.new("RGB", (270 * min(5, len(ims)), 480 * ((len(ims) + 4) // 5)))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % 5) * 270, (i // 5) * 480))
        p = os.path.join(self.dir, "sheet.png")
        sheet.save(p)
        return p


if __name__ == "__main__":
    r = Reel(sys.argv[1])
    cmd = sys.argv[2] if len(sys.argv) > 2 else "all"
    if cmd in ("voice", "all"):
        r.voice()
        print(r.id, "voice", round(r.timing["total"], 1), "s", flush=True)
    else:
        r._words()
    if cmd in ("render", "all"):
        r.audio()
        print(r.id, "->", r.render(), flush=True)
    if cmd == "stills":
        # one still per line, 70% into it
        wins = r.windows()
        ts = [a + (b - a) * 0.75 for a, b in wins] if len(sys.argv) == 3 else sys.argv[3:]
        print(r.stills(ts))
