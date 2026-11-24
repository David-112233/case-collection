r"""分段滚动实测：截图、对象位置，以及“跟随对象到描线末端”的距离。

注意：距离只在该图形自己的描绘阶段有意义（例如星形去画球时，到树线末端的距离自然很大）。

用于 input-sharpening 的第 2 步（实测被测输出）和第 9 步（GT 自检）。只读页面，不修改 HTML。

用法（仓库根目录）：
  $env:PYTHONUTF8='1'
  .\.venv\Scripts\python.exe -I .agents\skills\input-sharpening\scroll_trace_probe.py `
      --html cases\case-105-T6\ground_truth.html --out <暂存目录> `
      --path ".tree path" --follower ".star" --track ".tree" --track "h1"

--path 可重复，每条是一个“被逐步描出的”SVG 图形（按 stroke-dasharray/dashoffset 与 pathLength 计算已画长度）。
--follower 是应该停在描线末端的对象，取其包围盒中心。
--track 可重复，记录这些对象在每个滚动点的位置和透明度，用来发现对象移出视口、提前或延后出现。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HEAD_JS = """([sel, fsel]) => {
  const t = document.querySelector(sel);
  if (!t || !t.getTotalLength) return {error: 'path not found: ' + sel};
  const cs = getComputedStyle(t);
  const L = t.getTotalLength();
  const pl = parseFloat(t.getAttribute('pathLength') || L);
  const da = cs.strokeDasharray === 'none' ? pl : parseFloat(cs.strokeDasharray);
  const drawn = Math.max(0, Math.min(L, (da - parseFloat(cs.strokeDashoffset)) * L / pl));
  const p = t.getPointAtLength(drawn).matrixTransform(t.getScreenCTM());
  const out = {drawn_fraction: +(drawn / L).toFixed(3), head: [Math.round(p.x), Math.round(p.y)]};
  if (fsel) {
    const f = document.querySelector(fsel);
    if (f) {
      const r = f.getBoundingClientRect();
      const c = [r.x + r.width / 2, r.y + r.height / 2];
      out.follower = c.map(Math.round);
      out.distance_px = Math.round(Math.hypot(c[0] - p.x, c[1] - p.y));
      out.follower_opacity = +getComputedStyle(f).opacity;
    }
  }
  return out;
}"""

TRACK_JS = """(sel) => [...document.querySelectorAll(sel)].map(e => {
  const r = e.getBoundingClientRect();
  return {box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
          in_viewport: r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth,
          opacity: +getComputedStyle(e).opacity};
})"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--out", required=True, help="截图与 JSON 输出目录（建议放暂存目录或案例 review 目录）")
    ap.add_argument("--path", action="append", default=[])
    ap.add_argument("--follower")
    ap.add_argument("--track", action="append", default=[])
    ap.add_argument("--fractions", default="0,0.1,0.2,0.3,0.45,0.6,0.75,0.9,1")
    ap.add_argument("--viewport", default="1280x900")
    ap.add_argument("--browser", default="chromium", choices=["chromium", "firefox"])
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    w, h = (int(x) for x in args.viewport.split("x"))
    fractions = [float(x) for x in args.fractions.split(",")]
    url = Path(args.html).resolve().as_uri()
    stem = Path(args.html).stem
    rows = []
    with sync_playwright() as p:
        browser = getattr(p, args.browser).launch()
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto(url)
        page.wait_for_timeout(600)
        max_scroll = page.evaluate("document.documentElement.scrollHeight - innerHeight")
        shots = []
        for f in fractions:
            page.evaluate(f"window.scrollTo(0, {int(max_scroll * f)})")
            page.wait_for_timeout(400)
            row = {"fraction": f, "paths": {s: page.evaluate(HEAD_JS, [s, args.follower]) for s in args.path},
                   "track": {s: page.evaluate(TRACK_JS, s) for s in args.track}}
            rows.append(row)
            shot = out / f"{stem}_{args.browser}_{w}x{h}_{int(f * 100):03d}.png"
            page.screenshot(path=str(shot))
            shots.append(shot)
        browser.close()

    result = {"html": str(Path(args.html)), "browser": args.browser, "viewport": [w, h],
              "scrollable_px": max_scroll, "samples": rows}
    (out / f"{stem}_{args.browser}_{w}x{h}_probe.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    try:  # 九宫格总览，便于一次查看
        from PIL import Image
        thumbs = [Image.open(s).resize((427, int(427 * h / w))) for s in shots]
        cols = 3
        rows_n = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (427 * cols, thumbs[0].height * rows_n), "white")
        for i, im in enumerate(thumbs):
            sheet.paste(im, ((i % cols) * 427, (i // cols) * im.height))
        sheet.save(out / f"{stem}_{args.browser}_{w}x{h}_sheet.png")
    except ImportError:
        pass
    print(json.dumps({"scrollable_px": max_scroll, "samples": [
        {"fraction": r["fraction"], **{s: (v.get("drawn_fraction"), v.get("distance_px")) for s, v in r["paths"].items()}}
        for r in rows]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
