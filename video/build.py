"""Generates project.json for the VRTX hero video (motion-studio engine).

Run:  python video/build.py   ->  video/project.json
The chart candles and UI rows are generated here so the layout stays consistent.
"""
import json
import random
from pathlib import Path

W, H = 1920, 1080
ACC = "$acc"
WHITE = "#f5f5f4"
MUTED = "#8b8b92"
DIM = "#5c5c63"
SURF = "#121316"
SURF2 = "#1a1b1f"
LINE = "#ffffff1c"
LOGO = "../public/vrtx-icon.png"


# ---------- helpers ----------

def rise(lid, layer, at, y, dy=18, dur=0.6, blur=10):
    """Fade + rise + un-blur entrance, the house style for UI pieces."""
    layer["id"] = lid
    layer["y"] = y
    k = layer.setdefault("keys", {})
    k["opacity"] = [[at, 0, "swift"], [at + dur, 1]]
    k["y"] = [[at, y + dy, "swift"], [at + dur, y]]
    if blur:
        k["blur"] = [[at, blur, "swift"], [at + dur * 0.8, 0]]
    return layer


def text(lid, s, x, y, size=24, fill=WHITE, font="medium", anchor="lm", **kw):
    return {"id": lid, "type": "text", "text": s, "x": x, "y": y, "size": size, "fill": fill,
            "font": font, "anchor": anchor, "align": "left" if anchor[0] == "l" else "center", **kw}


def rect(lid, x, y, w, h, fill=SURF2, radius=14, stroke=None, sw=1, **kw):
    L = {"id": lid, "type": "rect", "x": x, "y": y, "w": w, "h": h, "fill": fill, "radius": radius, **kw}
    if stroke:
        L["stroke"], L["stroke_width"] = stroke, sw
    return L


def window(prefix, w, h, url, at=0.0):
    """App window chrome under a null group so the whole window moves together."""
    grp = {"id": prefix, "type": "null", "x": 960, "y": 548,
           "keys": {"opacity": [[at, 0, "swift"], [at + 0.8, 1]],
                    "y": [[at, 600, "swift"], [at + 1.0, 548]],
                    "scale": [[at, 0.96, "swift"], [at + 1.0, 1]]}}
    top = -h / 2
    layers = [grp,
              rect(f"{prefix}.bg", 0, 0, w, h, fill={"type": "linear", "angle": 90, "stops": [[SURF, 0], ["#0d0e10", 1]]},
                   radius=26, stroke="#ffffff22", parent=prefix,
                   shadow={"color": "#000000cc", "blur": 60, "x": 0, "y": 30}),
              rect(f"{prefix}.bar", 0, top + 28, w - 2, 54, fill="#0f1012", radius=0, parent=prefix),
              {"id": f"{prefix}.barline", "type": "line", "points": [[0, 0], [w - 2, 0]], "x": 0, "y": top + 56,
               "stroke": LINE, "stroke_width": 1, "parent": prefix}]
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        layers.append({"id": f"{prefix}.dot{i}", "type": "circle", "r": 7, "x": -w / 2 + 34 + i * 24, "y": top + 28,
                       "fill": c + "cc", "parent": prefix})
    layers.append(rect(f"{prefix}.url", 0, top + 28, 360, 32, fill="#ffffff0d", radius=9, parent=prefix))
    layers.append(text(f"{prefix}.urltxt", url, 0, top + 28, 17, MUTED, "medium", "mm", parent=prefix))
    return layers


def cursor_path(lid, pts, click_at=None):
    """Mouse cursor following [(t, x, y), ...] with an optional click ripple."""
    xs = [[t, x, "glide"] for t, x, _ in pts]
    ys = [[t, y, "glide"] for t, _, y in pts]
    t0 = pts[0][0]
    layers = [{"id": lid, "type": "icon", "name": "cursor", "size": 34, "fill": "#ffffff", "anchor": "lt",
               "x": pts[0][1], "y": pts[0][2], "depth": 1.05,
               "shadow": {"color": "#000000aa", "blur": 10, "x": 0, "y": 4},
               "keys": {"x": xs, "y": ys, "opacity": [[t0, 0, "swift"], [t0 + 0.3, 1]]}}]
    if click_at is not None:
        t, x, y = click_at
        layers[0]["keys"]["scale"] = [[t - 0.08, 1, "out_quad"], [t, 0.86, "out_quad"], [t + 0.15, 1]]
        layers.append({"id": f"{lid}.ripple", "type": "ring", "r": 12, "x": x, "y": y, "stroke": ACC, "stroke_width": 3,
                       "sweep": 1, "in": t, "out": t + 0.7, "depth": 1.05,
                       "keys": {"r": [[t, 8, "out_cubic"], [t + 0.6, 46]], "opacity": [[t, 1, "out_cubic"], [t + 0.6, 0]]}})
    return layers


def candles(count, seed):
    rnd = random.Random(seed)
    out, price = [], 100.0
    for i in range(count):
        ph = i / count
        if ph < .35: drift = (rnd.random() - .5) * 1.2
        elif ph < .45: drift = -1.6
        elif ph < .55: drift = 1.4
        elif ph < .65: drift = -.5
        else: drift = 1.5
        o = price
        c = o + drift + (rnd.random() - .5) * 2.0
        h = max(o, c) + rnd.random() * 1.3
        l = min(o, c) - rnd.random() * 1.3
        out.append((o, h, l, c))
        price = c
    return out


# ---------- scenes ----------

def scene_intro():
    return {
        "id": "intro", "duration": 2.8,
        "background": {"type": "radial", "cx": .5, "cy": .45, "r": .8, "stops": [["#0f1525", 0], ["#0a0a0b", 1]]},
        "camera": {"push": .04, "drift": 6},
        "layers": [
            {"id": "glow", "type": "circle", "r": 420, "x": 960, "y": 520, "fill": "#5f96ff22", "blur": 160, "depth": .4,
             "keys": {"opacity": [[0, 0, "swift"], [1.2, 1]]}},
            text("eyebrow", "V R T X", 960, 420, 22, MUTED, "semibold", "mm", tracking=6,
                 animate={"type": "blur_rise", "at": .15}),
            text("title", "In pursuit of price.", 960, 520, 104, WHITE, "display-semibold", "mm", tracking=-3,
                 animate={"type": "blur_rise", "at": .35, "split": "words", "stagger": .12},
                 exit={"type": "blur_out", "at": 2.35}),
            text("sub", "Guided by time.", 960, 630, 104, "#6f7079", "display-semibold", "mm", tracking=-3,
                 animate={"type": "blur_rise", "at": .85, "split": "words", "stagger": .12},
                 exit={"type": "blur_out", "at": 2.35}),
        ],
    }


def scene_analysis():
    w, h = 1440, 800
    L = window("win", w, h, "vrtx  ·  XAUUSD  ·  15m")
    top = -h / 2
    # header row
    L.append(rect("pill", -w / 2 + 110, top + 106, 160, 40, fill="#5f96ff22", radius=20, stroke="#5f96ff55", parent="win"))
    L.append(text("pilltxt", "XAUUSD · 15m", -w / 2 + 110, top + 106, 18, ACC, "semibold", "mm", parent="win"))
    L.append(text("plan", "Pre-session plan", w / 2 - 40, top + 106, 20, MUTED, "medium", "rm", parent="win"))
    # chart panel
    cx0, cx1, cy0, cy1 = -w / 2 + 40, w / 2 - 40, top + 150, top + 610
    L.append(rect("panel", 0, (cy0 + cy1) / 2, cx1 - cx0, cy1 - cy0, fill="#0b0c0e", radius=16, stroke="#ffffff12", parent="win"))
    for i, f in enumerate([.25, .5, .75]):
        y = cy0 + (cy1 - cy0) * f
        L.append({"id": f"grid{i}", "type": "line", "points": [[0, 0], [cx1 - cx0 - 2, 0]], "x": 0, "y": y,
                  "stroke": "#ffffff0a", "stroke_width": 1, "parent": "win"})
    cs = candles(46, 21)
    lo, hi = min(c[2] for c in cs), max(c[1] for c in cs)
    pad = 36
    py = lambda v: cy0 + pad + (hi - v) / (hi - lo) * (cy1 - cy0 - 2 * pad)
    step = (cx1 - cx0 - 2 * pad) / len(cs)
    px = lambda i: cx0 + pad + step * (i + .5)
    t0 = 0.7
    for i, (o, hh, ll, c) in enumerate(cs):
        at = t0 + i * 0.03
        up = c >= o
        col = "#e9e9ea" if up else "#4a4a52"
        L.append({"id": f"wick{i}", "type": "line", "points": [[0, py(hh)], [0, py(ll)]], "x": px(i),
                  "y": (py(hh) + py(ll)) / 2, "stroke": "#e9e9ea" if up else "#5f5f68", "stroke_width": 2,
                  "parent": "win", "keys": {"opacity": [[at, 0, "swift"], [at + .3, 1]]}})
        bt, bb = py(max(o, c)), py(min(o, c))
        L.append(rect(f"body{i}", px(i), (bt + bb) / 2, step * .6, max(4, bb - bt), fill=col, radius=2,
                      stroke=None if up else "#6a6a73", parent="win",
                      keys={"opacity": [[at, 0, "swift"], [at + .3, 1]],
                            "scale_y": [[at, .2, "swift"], [at + .35, 1]]}))
    # levels
    rh = max(c[1] for c in cs[:int(len(cs) * .35)])
    sweep = min(range(len(cs)), key=lambda i: cs[i][2])
    entry_i = sweep + 3
    la = t0 + len(cs) * .03 + .1
    L.append({"id": "rangehigh", "type": "line", "points": [[0, 0], [cx1 - cx0 - 2 * pad, 0]], "x": 0, "y": py(rh),
              "stroke": "#ffffff55", "stroke_width": 2, "parent": "win",
              "keys": {"draw": [[la, 0, "swift"], [la + .8, 1]]}})
    L.append(text("rhl", "Range high", cx0 + pad + 6, py(rh) - 20, 18, MUTED, "medium", parent="win",
                  keys={"opacity": [[la + .2, 0, "swift"], [la + .6, 1]]}))
    ex = px(entry_i)
    L.append({"id": "entry", "type": "line", "points": [[0, 0], [cx1 - pad - ex, 0]], "x": (ex + cx1 - pad) / 2,
              "y": py(cs[entry_i][3]), "stroke": ACC, "stroke_width": 2, "parent": "win",
              "keys": {"draw": [[la + .3, 0, "swift"], [la + 1.0, 1]], "opacity": [[la + .3, 0], [la + .4, .8]]}})
    L.append(text("swl", "Sweep", px(sweep) - 18, py(cs[sweep][2]) + 4, 18, MUTED, "medium", "rm", parent="win",
                  keys={"opacity": [[la + .4, 0, "swift"], [la + .8, 1]]}))
    last = cs[-1]
    L.append(text("cont", "Continuation +2R", px(len(cs) - 1) + 6, py(last[1]) - 26, 20, ACC, "semibold", "rm", parent="win",
                  glow={"color": "#5f96ff", "radius": 14, "strength": .5},
                  keys={"opacity": [[la + .6, 0, "swift"], [la + 1.0, 1]]}))
    # stat boxes
    bw = (w - 80 - 32) / 3
    for i, (lab, val, accent) in enumerate([("Bias", "Bullish", True), ("Window", "NY open", False), ("Model", "Continuation", False)]):
        bx = -w / 2 + 40 + bw / 2 + i * (bw + 16)
        at = la + .2 + i * .12
        L.append(rise(f"box{i}", rect("", bx, 0, bw, 104, fill="#ffffff07", radius=14, stroke="#ffffff14", parent="win"), at, top + 690, blur=0))
        L.append(rise(f"boxl{i}", text("", lab, bx - bw / 2 + 24, 0, 18, MUTED, "medium", parent="win"), at + .05, top + 668, blur=0))
        L.append(rise(f"boxv{i}", text("", val, bx - bw / 2 + 24, 0, 26, ACC if accent else WHITE, "semibold", parent="win"), at + .08, top + 706, blur=0))
    # cursor travels to the continuation and clicks; +2R tag pops
    cxs, cys = 960 + px(len(cs) - 3), 548 + py(cs[-3][1]) + 10
    L += cursor_path("cur", [(2.6, 1500, 900), (3.6, cxs, cys), (4.6, cxs + 4, cys + 2)], click_at=(3.75, cxs, cys))
    tag_x, tag_y = cxs - 330, cys - 40
    L.append(rect("tag", tag_x, tag_y, 124, 48, fill=ACC, radius=24, glow={"color": "#5f96ff", "radius": 26, "strength": .6},
                  keys={"opacity": [[3.85, 0, "punch"], [4.1, 1]], "scale": [[3.85, .6, "punch"], [4.25, 1]]}))
    L.append(text("tagtxt", "+2R", tag_x, tag_y, 24, "#ffffff", "bold", "mm",
                  keys={"opacity": [[3.85, 0, "punch"], [4.1, 1]], "scale": [[3.85, .6, "punch"], [4.25, 1]]}))
    return {
        "id": "analysis", "duration": 5.6,
        "background": "#0a0a0b",
        "transition": {"type": "blur", "duration": .6},
        "camera": {"drift": 8, "keys": {
            "zoom": [[0, 1.0, "ae"], [2.4, 1.0, "ae"], [4.6, 1.18]],
            "pan_x": [[0, 0, "ae"], [2.4, 0, "ae"], [4.6, 230]],
            "pan_y": [[0, 0, "ae"], [2.4, 0, "ae"], [4.6, -90]]}},
        "layers": L,
    }


def scene_community():
    w, h = 1440, 800
    L = window("dwin", w, h, "discord.gg  ·  V R T X")
    top = -h / 2
    side_w = 300
    sx = -w / 2 + side_w / 2
    L.append(rect("side", sx, 28, side_w - 2, h - 58, fill="#0c0d0f", radius=0, parent="dwin"))
    L.append({"id": "logo", "type": "image", "src": LOGO, "w": 40, "h": 40, "radius": 10, "x": -w / 2 + 44, "y": top + 100, "parent": "dwin"})
    L.append(text("srv", "V R T X", -w / 2 + 78, top + 100, 22, WHITE, "semibold", parent="dwin", tracking=2))
    chans = ["announcements", "analysis", "trade-talk", "trade-recaps", "wins", "education"]
    for i, c in enumerate(chans):
        y = top + 168 + i * 50
        if c == "trade-talk":
            L.append(rect("chact", sx, y, side_w - 36, 40, fill="#ffffff10", radius=8, parent="dwin"))
        L.append(rise(f"ch{i}", text("", f"#  {c}", -w / 2 + 36, 0, 19, WHITE if c == "trade-talk" else MUTED, "medium", parent="dwin"),
                      .6 + i * .07, y, dy=10, dur=.45, blur=0))
    mx0 = -w / 2 + side_w + 40
    L.append(text("chan", "#  trade-talk", mx0, top + 100, 22, WHITE, "semibold", parent="dwin"))
    L.append({"id": "chline", "type": "line", "points": [[0, 0], [w - side_w - 2, 0]], "x": side_w / 2, "y": top + 136,
              "stroke": LINE, "stroke_width": 1, "parent": "dwin"})
    msgs = [
        (True, "M I R Z A", "Gold swept the Asia low into the NY window. Watching for the continuation sequence above the range."),
        (False, "member", "Is the displacement candle enough confirmation here?"),
        (True, "M I R Z A", "Wait for the time. Price can go anywhere, timing tells you when it matters."),
    ]
    y = top + 200
    for i, (mentor, name, msg) in enumerate(msgs):
        at = 1.0 + i * 1.05
        g = f"m{i}"
        L.append({"id": g, "type": "null", "x": 0, "y": 0, "parent": "dwin",
                  "keys": {"opacity": [[at, 0, "swift"], [at + .5, 1]], "y": [[at, 22, "swift"], [at + .6, 0]]}})
        L.append({"id": f"{g}.av", "type": "circle", "r": 24, "x": mx0 + 24, "y": y + 20, "fill": ACC if mentor else "#2a2a30", "parent": g})
        L.append(text(f"{g}.ini", name[0], mx0 + 24, y + 20, 20, "#ffffff" if mentor else MUTED, "bold", "mm", parent=g))
        L.append(text(f"{g}.name", name, mx0 + 66, y + 4, 21, WHITE, "semibold", parent=g, tracking=2 if mentor else 0))
        if mentor:
            L.append(rect(f"{g}.tagbg", mx0 + 66 + 170, y + 4, 58, 24, fill="#2a2a30", radius=6, parent=g))
            L.append(text(f"{g}.tag", "VRTX", mx0 + 66 + 170, y + 4, 13, MUTED, "bold", "mm", parent=g, tracking=1))
        L.append(text(f"{g}.txt", msg, mx0 + 66, y + 30, 21, "#c9c9ce", "regular", "lt", parent=g,
                      max_width=w - side_w - 160, line_height=1.35))
        y += 150 if len(msg) > 90 else 110
    ty = top + h - 120
    L.append({"id": "typing", "type": "null", "x": 0, "y": 0, "parent": "dwin",
              "keys": {"opacity": [[4.2, 0, "swift"], [4.5, 1]]}})
    for i in range(3):
        L.append({"id": f"td{i}", "type": "circle", "r": 4, "x": mx0 + 8 + i * 14, "y": ty, "fill": MUTED, "parent": "typing",
                  "wiggle": {"y": [3, 2.2 + i * .1]}})
    L.append(text("tdt", "member is typing…", mx0 + 52, ty, 17, MUTED, "medium", parent="typing"))
    L.append(rect("input", (mx0 + w / 2 - 40) / 2, top + h - 64, w / 2 - 40 - mx0, 52, fill="#ffffff0a", radius=12, parent="dwin"))
    L.append(text("inputt", "Message #trade-talk", mx0 + 20, top + h - 64, 18, DIM, "medium", parent="dwin"))
    return {
        "id": "community", "duration": 5.6,
        "background": "#0a0a0b",
        "transition": {"type": "blur", "duration": .6},
        "camera": {"drift": 8, "keys": {
            "zoom": [[0, 1.0, "ae"], [1.2, 1.0, "ae"], [5.6, 1.14]],
            "pan_x": [[0, 0, "ae"], [1.2, 0, "ae"], [5.6, 150]],
            "pan_y": [[0, 0, "ae"], [1.2, 0, "ae"], [5.6, -30]]}},
        "layers": L,
    }


def scene_results():
    L = [
        {"id": "rglow", "type": "circle", "r": 380, "x": 960, "y": 620, "fill": "#5f96ff18", "blur": 160, "depth": .4},
        text("head", "Results, shared in public.", 960, 210, 64, WHITE, "display-semibold", "mm", tracking=-2,
             animate={"type": "blur_rise", "at": .2, "split": "words", "stagger": .1}),
    ]
    cards = [("+2R", 2, "Continuation sequence", "XAUUSD · Oct 30"), ("+3R", 3, "Session expansion", "XAUUSD · Oct 23")]
    cw, ch = 500, 370
    xs = [960 - cw - 40 - 30, 960 - 30 + 0]
    xs = [400, 940]
    for i, (lab, n, note, meta) in enumerate(cards):
        g, x, at = f"c{i}", xs[i] , .5 + i * .18
        L.append({"id": g, "type": "null", "x": x, "y": 600, "depth": 1.1,
                  "keys": {"opacity": [[at, 0, "swift"], [at + .6, 1]], "y": [[at, 660, "swift"], [at + .9, 600]]}})
        L.append(rect(f"{g}.bg", 0, 0, cw, ch, fill={"type": "linear", "angle": 90, "stops": [[SURF2, 0], ["#0f1013", 1]]},
                      radius=22, stroke="#ffffff1f", parent=g, shadow={"color": "#000000aa", "blur": 40, "x": 0, "y": 20}))
        L.append(rect(f"{g}.pill", -cw / 2 + 78, -ch / 2 + 46, 116, 34, fill="#5f96ff22", radius=17, stroke="#5f96ff55", parent=g))
        L.append(text(f"{g}.pt", "XAUUSD", -cw / 2 + 78, -ch / 2 + 46, 16, ACC, "semibold", "mm", parent=g))
        L.append(text(f"{g}.meta", meta.split(" · ")[1], cw / 2 - 30, -ch / 2 + 46, 17, MUTED, "medium", "rm", parent=g))
        L.append(text(f"{g}.num", lab, -cw / 2 + 30, -6, 110, ACC, "display-semibold", parent=g, tracking=-3,
                      number=0, format="+{:.0f}R", keys={"number": [[at + .3, 0, "swift"], [at + 1.2, n]]},
                      glow={"color": "#5f96ff", "radius": 24, "strength": .4}))
        L.append(text(f"{g}.note", note, -cw / 2 + 32, 74, 24, MUTED, "medium", parent=g))
        L.append({"id": f"{g}.line", "type": "polyline", "smooth": True, "parent": g, "x": 0, "y": 140,
                  "points": [[-180, 20], [-120, 14], [-60, 22], [0, 6], [60, 0], [120, -14], [180, -26]],
                  "stroke": ACC, "stroke_width": 3, "keys": {"draw": [[at + .5, 0, "swift"], [at + 1.4, 1]]}})
    # testimonial
    g, at = "q", .9
    qx = 1490
    L.append({"id": g, "type": "null", "x": qx, "y": 600, "depth": 1.2,
              "keys": {"opacity": [[at, 0, "swift"], [at + .6, 1]], "y": [[at, 660, "swift"], [at + .9, 600]]}})
    L.append(rect(f"{g}.bg", 0, 0, 520, 370, fill="#5f96ff12", radius=22, stroke="#5f96ff44", parent=g,
                  shadow={"color": "#000000aa", "blur": 40, "x": 0, "y": 20}))
    L.append(text(f"{g}.t", "Phase 1 & 2 in 5 days", -225, -125, 28, WHITE, "semibold", parent=g))
    L.append(text(f"{g}.b", "“I passed my phase 1 in 3 days and phase 2 in 2 days. Thank you so much.”",
                  -225, -85, 23, "#c9c9ce", "regular", "lt", parent=g, max_width=450, line_height=1.4))
    L.append({"id": f"{g}.av", "type": "circle", "r": 20, "x": -205, "y": 130, "fill": "#2a2a30", "parent": g})
    L.append(text(f"{g}.ai", "S", -205, 130, 16, WHITE, "bold", "mm", parent=g))
    L.append(text(f"{g}.n", "Shahid · VRTX member", -172, 130, 18, MUTED, "medium", parent=g))
    return {
        "id": "results", "duration": 4.4,
        "background": "#0a0a0b",
        "transition": {"type": "blur", "duration": .6},
        "camera": {"push": .05, "drift": 10},
        "layers": L,
    }


def scene_mentorship():
    w, h = 1180, 760
    L = window("mwin", w, h, "1-on-1  ·  Mentorship")
    top = -h / 2
    L.append(rect("mpill", -w / 2 + 90, top + 106, 110, 40, fill="#5f96ff22", radius=20, stroke="#5f96ff55", parent="mwin"))
    L.append(text("pt", "1-on-1", -w / 2 + 90, top + 106, 18, ACC, "semibold", "mm", parent="mwin"))
    L.append(text("wk", "This week · 2/3", w / 2 - 40, top + 106, 20, MUTED, "medium", "rm", parent="mwin"))
    L.append(rect("track", 0, top + 152, w - 80, 5, fill="#ffffff14", radius=3, parent="mwin"))
    L.append(rect("fill", -w / 2 + 40, top + 152, w - 80, 5, fill=ACC, radius=3, anchor="lm", parent="mwin",
                  glow={"color": "#5f96ff", "radius": 10, "strength": .5},
                  keys={"scale_x": [[.9, .001, "swift"], [2.0, .667]]}))
    rows = [("Mon", "Model review", True), ("Wed", "Live execution", True), ("Fri", "Journal and risk", False)]
    for i, (d, topic, done) in enumerate(rows):
        y = top + 230 + i * 92
        at = .8 + i * .14
        g = f"r{i}"
        L.append({"id": g, "type": "null", "x": 0, "y": 0, "parent": "mwin",
                  "keys": {"opacity": [[at, 0, "swift"], [at + .5, 1]], "y": [[at, 16, "swift"], [at + .6, 0]]}})
        L.append(rect(f"{g}.bg", 0, y, w - 80, 76, fill="#ffffff06", radius=14, stroke="#ffffff14", parent=g))
        L.append(text(f"{g}.d", d, -w / 2 + 66, y, 22, MUTED, "medium", parent=g))
        L.append(text(f"{g}.t", topic, -w / 2 + 170, y, 24, WHITE, "semibold", parent=g))
        if done:
            L.append({"id": f"{g}.ck", "type": "icon", "name": "check", "size": 22, "fill": ACC, "x": w / 2 - 140, "y": y, "parent": g,
                      "keys": {"scale": [[1.3 + i * .15, 0, "punch"], [1.6 + i * .15, 1]]}})
            L.append(text(f"{g}.s", "Done", w / 2 - 66, y, 19, MUTED, "medium", "rm", parent=g))
        else:
            L.append(text(f"{g}.s", "Next", w / 2 - 66, y, 19, ACC, "semibold", "rm", parent=g))
    ny = top + 560
    L.append({"id": "note", "type": "null", "x": 0, "y": 0, "parent": "mwin",
              "keys": {"opacity": [[1.5, 0, "swift"], [2.1, 1]], "y": [[1.5, 16, "swift"], [2.1, 0]]}})
    L.append(rect("note.bg", 0, ny + 40, w - 80, 150, fill="#5f96ff14", radius=16, stroke="#5f96ff33", parent="note"))
    L.append(text("note.l", "Mentor note", -w / 2 + 70, ny + 0, 18, MUTED, "medium", parent="note"))
    L.append(text("note.t", "Entries are clean. Stop moving the stop to breakeven before the sequence completes. Let the trade breathe.",
                  -w / 2 + 70, ny + 26, 24, WHITE, "medium", "lt", parent="note", max_width=w - 160, line_height=1.4))
    return {
        "id": "mentorship", "duration": 4.4,
        "background": "#0a0a0b",
        "transition": {"type": "blur", "duration": .6},
        "camera": {"drift": 8, "keys": {"zoom": [[0, 1.0, "ae"], [4.4, 1.09]], "pan_y": [[0, 0, "ae"], [4.4, 40]]}},
        "layers": L,
    }


def scene_end():
    return {
        "id": "end", "duration": 3.6,
        "background": {"type": "radial", "cx": .5, "cy": .55, "r": .7, "stops": [["#0e1322", 0], ["#0a0a0b", 1]]},
        "transition": {"type": "blur", "duration": .7},
        "camera": {"push": .03, "drift": 4},
        "layers": [
            {"id": "eglow", "type": "circle", "r": 300, "x": 960, "y": 640, "fill": "#5f96ff30", "blur": 140, "depth": .5,
             "keys": {"opacity": [[.8, 0, "swift"], [1.8, 1]]}},
            {"id": "etitle", "type": "text", "spans": [{"text": "Time "}, {"text": ">", "fill": ACC}, {"text": " Price."}],
             "x": 960, "y": 400, "size": 120, "font": "display-semibold", "fill": WHITE, "anchor": "mm", "align": "center",
             "tracking": -4, "animate": {"type": "blur_rise", "at": .25, "split": "words", "stagger": .14}},
            {"id": "elogo", "type": "image", "src": LOGO, "w": 150, "h": 150, "radius": 36, "x": 960, "y": 650,
             "border": "#ffffff33", "border_width": 2,
             "glow": {"color": "#5f96ff", "radius": 46, "strength": .55},
             "keys": {"opacity": [[1.0, 0, "swift"], [1.6, 1]], "scale": [[1.0, .7, "spring"], [1.9, 1]],
                      "blur": [[1.0, 14, "swift"], [1.5, 0]]}},
            text("brand", "V R T X", 960, 790, 24, MUTED, "semibold", "mm", tracking=8,
                 animate={"type": "blur_rise", "at": 1.6}),
        ],
    }


project = {
    "output": {"width": W, "height": H, "fps": 30},
    "design": [W, H],
    "palette": {"acc": "#5f96ff"},
    "motion_blur": 1.0,
    "sfx": {"auto": False},
    "post": [{"type": "bloom", "strength": .25, "threshold": .75}, {"type": "vignette", "strength": .25},
             {"type": "grain", "amount": .012}],
    "scenes": [scene_intro(), scene_analysis(), scene_community(), scene_results(), scene_mentorship(), scene_end()],
}

out = Path(__file__).with_name("project.json")
out.write_text(json.dumps(project, indent=1))
print("wrote", out, "layers:", sum(len(s["layers"]) for s in project["scenes"]))
