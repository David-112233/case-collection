"""GT self-check for case-245-T1: screenshots at 1280x800, 1280x992 and 500x800.

    python cases/case-245-T1/review_20261124/shot_gt.py

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
  scroll_h: document.documentElement.scrollHeight,
  frame: (() => { const r = document.querySelector('.frame').getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height}; })(),
  rows: document.querySelectorAll('.row').length,
  cubes: document.querySelectorAll('.inverse-cube').length,
})"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in [(1280, 800), (1280, 992), (500, 800)]:
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
