"""Numeric projection of the GT's CSS 3D faces (NOT a browser screenshot).

The cloud environment has no Chromium, so this script reproduces the CSS
transform chain of every face in ground_truth.html by hand (matrix by matrix,
using the GT's own transform / transform-origin / size values) and paints the
faces as flat polygons with a painter's sort. It is only a geometry aid for
reading the composition (which faces are visible, what sits where); colours
are the faces' background-color, gradients/borders/box-shadows are ignored.

Usage:  python3 css3d_projection.py <ground_truth.html> <out_dir>
Writes projection_<state>_<w>.png and projection_<state>_<w>.json.
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageColor, ImageDraw

# ---------------------------------------------------------------- CSS parsing
def parse_css(html):
    css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"@keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    rules = {}
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        decls = {}
        for d in body.split(";"):
            if ":" in d:
                k, v = d.split(":", 1)
                decls[k.strip()] = v.strip()
        for s in sel.split(","):
            rules.setdefault(s.strip(), {}).update(decls)
    return rules


class Ctx:
    def __init__(self, vw_px, vh_px):
        self.vw = vw_px / 100.0
        self.vh = vh_px / 100.0

    def length(self, v, ref=None):
        v = v.strip()
        if v in ("0", ""):
            return 0.0
        m = re.fullmatch(r"(-?[\d.]+)(vw|px|%|vh|deg)?", v)
        if not m:
            raise ValueError(v)
        n, u = float(m.group(1)), m.group(2)
        if u == "vw":
            return n * self.vw
        if u == "vh":
            return n * self.vh
        if u == "%":
            return n / 100.0 * ref
        return n


def T(x=0, y=0, z=0):
    m = np.eye(4)
    m[:3, 3] = (x, y, z)
    return m


def Rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])


def Ry(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])


def Rz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def transform_matrix(ctx, s, w, h):
    m = np.eye(4)
    if not s or s == "none":
        return m
    for fn, arg in re.findall(r"(\w+)\(([^)]*)\)", s):
        if fn == "perspective":
            p = np.eye(4)
            p[3, 2] = -1.0 / ctx.length(arg)
            f = p
        elif fn in ("rotateX", "rotateY", "rotateZ"):
            a = math.radians(float(arg.replace("deg", "")))
            f = {"rotateX": Rx, "rotateY": Ry, "rotateZ": Rz}[fn](a)
        elif fn == "translateX":
            f = T(x=ctx.length(arg, w))
        elif fn == "translateY":
            f = T(y=ctx.length(arg, h))
        elif fn == "translateZ":
            f = T(z=ctx.length(arg))
        elif fn == "skewX":
            f = np.eye(4)
            f[0, 1] = math.tan(math.radians(float(arg.replace("deg", ""))))
        else:
            raise ValueError(fn)
        m = m @ f
    return m


def origin(ctx, s, w, h):
    if not s:
        return (w / 2, h / 2)
    parts = s.split()
    kw = {"left": 0, "top": 0, "right": 1, "bottom": 1, "center": 0.5}
    if len(parts) == 2 and parts[0] in ("bottom", "top"):
        parts = parts[::-1]
    x = kw[parts[0]] * w if parts[0] in kw else ctx.length(parts[0], w)
    y = kw[parts[1]] * h if parts[1] in kw else ctx.length(parts[1], h)
    return (x, y)


# ----------------------------------------------------------- element tree
# (classes, children). Mirrors the GT DOM inside .shadows and .radio.
def cube(prefix, faces=("front", "back", "right", "left", "top", "bottom"), extra=None):
    kids = [([f"{prefix}__{f}", "face"], (extra or {}).get(f, [])) for f in faces]
    return kids


RADIO_TREE = [
    (["bf"], cube("bf")),
    (["ffa"], cube("ffa", ("front", "right", "left", "top", "bottom"),
                   extra={"front": [(["ffa__front-circles"], [])],
                          "right": [(["range"], cube("range"))]})),
    (["ffb"], cube("ffb", ("front", "right", "left", "top", "bottom"))),
    (["ffc"], cube("ffc", ("front", "right", "left", "top", "bottom"))),
    (["ffd"], cube("ffd", ("front", "right", "left", "top", "bottom"))),
    (["buttons"], [(["button"], cube("button")), (["button"], cube("button")),
                   (["button"], cube("button")), (["button", "button--cta"], cube("button"))]),
    (["cover"], [(["cover-b"], cube("cover-b", ("front", "right", "left", "top", "bottom")))]),
    (["cassete"], cube("cassete")),
]
SHADOW_TREE = [(["shadow-1"], []), (["shadow-2"], [])]


def style_of(rules, classes, nth=None, state=()):
    st = {}
    for c in classes:
        st.update(rules.get("." + c, {}))
    if nth is not None:
        st.update(rules.get(f".button:nth-of-type({nth})", {}))
    for sel, decls in rules.items():
        # descendant colour overrides such as ".button--cta .button__front"
        parts = sel.split()
        if len(parts) == 2 and parts[1].lstrip(".") in classes and ":" not in sel:
            if parts[0].lstrip(".") in state:
                st.update(decls)
    for s in state:
        if s.startswith("is-") and s in classes:
            pass
    return st


def walk(ctx, rules, tree, parent_m, pw, ph, out, state, ancestors=()):
    nth_counter = 0
    for classes, kids in tree:
        classes = list(classes)
        nth = None
        if "button" in classes:
            nth_counter += 1
            nth = nth_counter
        active = []
        if state == "playing":
            if "button--cta" in classes:
                active.append("is-button-active")
            if "cover" in classes:
                active.append("is-cover-active")
        st = style_of(rules, classes + active, nth, set(ancestors) | set(classes))
        for a in active:
            st.update(rules.get("." + a, {}))
        w = ctx.length(st.get("width", "0"), pw) if "width" in st else pw
        h = ctx.length(st.get("height", "0"), ph) if "height" in st else 0
        if "width" not in st and "face" in classes:
            w = pw
        # offsets
        x = y = 0.0
        if "left" in st:
            x = ctx.length(st["left"], pw)
        elif "right" in st:
            x = pw - w - ctx.length(st["right"], pw)
        if "top" in st:
            y = ctx.length(st["top"], ph)
        elif "bottom" in st:
            y = ph - h - ctx.length(st["bottom"], ph)
        if classes[0] == "range":  # abs child of flex face: centred, padding-top 3vw
            x = (pw - w) / 2
            y = ctx.length("3vw")
        if classes[0] == "ffa__front-circles":  # in-flow block, 100% x 80%
            x, y = 0, 0
        ox, oy = origin(ctx, st.get("transform-origin"), w, h)
        local = T(x, y) @ T(ox, oy) @ transform_matrix(ctx, st.get("transform"), w, h) @ T(-ox, -oy)
        m = parent_m @ local
        color = st.get("background-color")
        if "background-image" in st and not color:
            color = re.findall(r"#[0-9A-Fa-f]{6}", st["background-image"])[0]
        if classes[0] == "ffa__front-circles":
            color = "#383832"
        if color and w > 0 and h > 0:
            out.append({"cls": classes[0], "m": m, "w": w, "h": h, "color": color})
        walk(ctx, rules, kids, m, w, h, out, state, tuple(ancestors) + tuple(classes))


def project(m, pts):
    res = []
    for px, py in pts:
        v = m @ np.array([px, py, 0, 1.0])
        res.append((v[0] / v[3], v[1] / v[3], v[2] / v[3]))
    return res


def render(gt_path, out_dir, vw_px, vh_px, state):
    html = Path(gt_path).read_text(encoding="utf-8")
    rules = parse_css(html)
    ctx = Ctx(vw_px, vh_px)
    root_w, root_h = ctx.length("26vw"), ctx.length("6vw")
    # .radio / .shadows are absolutely positioned children of the centring flex body
    root_x = (vw_px - root_w) / 2
    root_y = (vh_px - root_h) / 2
    tr = rules[".radio"]["transform"]
    base = T(root_x, root_y) @ T(root_w / 2, root_h / 2) @ transform_matrix(ctx, tr, root_w, root_h) @ T(-root_w / 2, -root_h / 2)
    faces = []
    walk(ctx, rules, SHADOW_TREE, base, root_w, root_h, faces, state)
    walk(ctx, rules, RADIO_TREE, base, root_w, root_h, faces, state)
    polys = []
    for f in faces:
        q = project(f["m"], [(0, 0), (f["w"], 0), (f["w"], f["h"]), (0, f["h"])])
        polys.append((sum(p[2] for p in q) / 4, f, q))
    polys.sort(key=lambda t: t[0])
    # z-buffer rasterisation (painter's sort fails for the large overlapping faces)
    H, W = vh_px, vw_px
    zbuf = np.full((H, W), -np.inf)
    rgb = np.zeros((H, W, 3))
    rgb[:] = np.array(ImageColor.getrgb("#FCCD64"), float)
    owner = np.full((H, W), -1)
    boxes = {}
    yy, xx = np.mgrid[0:H, 0:W]
    for idx, (z, f, q) in enumerate(polys):
        col = f["color"]
        m = re.fullmatch(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", col)
        alpha = float(m.group(4)) if m else 1.0
        c = np.array([int(m.group(i)) for i in (1, 2, 3)], float) if m else np.array(ImageColor.getrgb(col), float)
        xs, ys = [p[0] for p in q], [p[1] for p in q]
        b = boxes.setdefault(f["cls"], [1e9, 1e9, -1e9, -1e9])
        boxes[f["cls"]] = [min(b[0], min(xs)), min(b[1], min(ys)), max(b[2], max(xs)), max(b[3], max(ys))]
        x0, x1 = max(0, int(min(xs))), min(W - 1, int(max(xs)) + 1)
        y0, y1 = max(0, int(min(ys))), min(H - 1, int(max(ys)) + 1)
        if x1 < x0 or y1 < y0:
            continue
        X = xx[y0:y1 + 1, x0:x1 + 1] + 0.5
        Y = yy[y0:y1 + 1, x0:x1 + 1] + 0.5
        for tri in ((q[0], q[1], q[2]), (q[0], q[2], q[3])):
            (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
            den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            if abs(den) < 1e-9:
                continue
            l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den
            l2 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den
            l3 = 1 - l1 - l2
            inside = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
            zz = l1 * az + l2 * bz + l3 * cz + 1e-3 * idx / len(polys)
            sub_z = zbuf[y0:y1 + 1, x0:x1 + 1]
            sub_rgb = rgb[y0:y1 + 1, x0:x1 + 1]
            if alpha >= 1:
                win = inside & (zz > sub_z)
                sub_z[win] = zz[win]
                sub_rgb[win] = c
                owner[y0:y1 + 1, x0:x1 + 1][win] = idx
            else:
                win = inside & (zz > sub_z)
                sub_rgb[win] = sub_rgb[win] * (1 - alpha) + c * alpha
    img = Image.fromarray(rgb.clip(0, 255).astype("uint8"))
    # translucent faces: draw their outline as the door frame
    d = ImageDraw.Draw(img)
    for z, f, q in polys:
        if f["color"].startswith("rgba"):
            d.polygon([(p[0], p[1]) for p in q], outline="#DEE0D3", width=max(1, vw_px // 400))
    out = Path(out_dir)
    img.save(out / f"projection_{state}_{vw_px}.png")
    (out / f"projection_{state}_{vw_px}.json").write_text(
        json.dumps({"note": "numeric CSS-3D projection, not a browser screenshot",
                    "viewport": [vw_px, vh_px], "state": state,
                    "bbox_px": {k: [round(v, 1) for v in b] for k, b in sorted(boxes.items())}},
                   ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    gt, out = sys.argv[1], sys.argv[2]
    for (w, h) in ((1280, 800), (375, 812)):
        for state in ("default", "playing"):
            render(gt, out, w, h, state)
