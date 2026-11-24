"""GT 自检：case-234-T1（拍立得）。1280×800 与 375×812 两个视口，GT 与 source 各截一张，并测量各部件。

用法（仓库根目录）：python cases/case-234-T1/review_20261124/gt_check.py
需要 playwright 和 chromium（python -m playwright install chromium）。
作品无动画、无交互，只截初始状态；另截一张鼠标悬停在快门上的图，确认悬停不改变画面。
输出：gt_<宽>.png、source_<宽>.png、gt_<宽>_hover_shutter.png 和 measurements.json，写在本脚本旁边。
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
SRC = HERE.parent / "source.html"
VIEWPORTS = [(1280, 800), (375, 812)]
PARTS = [
    ".camera", ".camera .top", ".camera .bottom",
    ".top .flash", ".top .timer", ".top .sensor", ".top .lens", ".top .lens .glass", ".top .shutter",
    ".top .viewfinder", ".top .viewfinder .glass", ".top .viewfinder .back",
    ".top .toggle-container", ".top .toggle-container .toggle", ".top .power",
    ".bottom .toggle-container", ".bottom .toggle", ".bottom .handle",
    ".bottom .printer", ".bottom .rainbow", ".bottom .logo",
]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            bg: cs.backgroundColor, color: cs.color, font: cs.fontFamily, cursor: cs.cursor}; };
  const all = [...document.querySelectorAll('*')];
  return {
    viewport: [innerWidth, innerHeight],
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    body_bg_image: getComputedStyle(document.body).backgroundImage,
    title: document.title,
    scripts: document.scripts.length,
    stylesheets: document.styleSheets.length,
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    logo_text: (document.querySelector('.logo') || {}).textContent,
    logo_font_ok: document.fonts.check('600 24px "Helvetica Neue"') || document.fonts.check('600 24px Helvetica'),
    parts: Object.fromEntries(parts.map(p => [p, box(p)])),
  };
}"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, path in (("gt", GT), ("source", SRC)):
            for w, h in VIEWPORTS:
                page = browser.new_page(viewport={"width": w, "height": h})
                failed = []
                page.on("requestfailed", lambda r: failed.append(r.url))
                page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
                page.goto(path.as_uri(), wait_until="networkidle")
                page.wait_for_timeout(500)
                page.screenshot(path=str(HERE / f"{name}_{w}.png"), full_page=True)
                key = f"{name}_{w}x{h}"
                out[key] = page.evaluate(PROBE, PARTS)
                if name == "gt":
                    page.hover(".top .shutter")
                    page.wait_for_timeout(200)
                    page.screenshot(path=str(HERE / f"gt_{w}_hover_shutter.png"), full_page=True)
                    out[f"{key}_hover_shutter"] = page.evaluate(PROBE, PARTS)
                out[f"{key}_failed_requests"] = failed
                page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in out.items():
        if isinstance(v, dict):
            print(k, "scroll:", v["scroll"], "animations:", v["running_animations"], "transitions:", v["nonzero_transitions"])
        else:
            print(k, v)


if __name__ == "__main__":
    main()
