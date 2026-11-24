"""GT self-check for case-244-T1: screenshots at 1280x800 and 500x800 plus ring boxes.

    python cases/case-244-T1/review_20261124/shot_gt.py

Needs Playwright chromium. Writes PNGs and measurements.json next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
PROBE = """() => ({
  scroll_w: document.documentElement.scrollWidth,
  running_animations: document.getAnimations().length,
  rings: [...document.querySelectorAll('.ring')].map(e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return {cls: e.className, x: r.x, y: r.y, w: r.width, h: r.height, z: cs.zIndex,
            colors: [cs.borderTopColor, cs.borderRightColor, cs.borderBottomColor, cs.borderLeftColor]}; }),
})"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in [(1280, 800), (500, 800)]:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.screenshot(path=str(HERE / f"gt_{w}x{h}.png"))
            out[f"{w}x{h}"] = page.evaluate(PROBE)
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
