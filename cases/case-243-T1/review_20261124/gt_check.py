"""GT self-check for case-243-T1 (static CSS 3D scene, no interaction): screenshots and measurements.

    python cases/case-243-T1/review_20261124/gt_check.py

Needs Playwright chromium; the page has no external resources. Also screenshots source.html at the same viewports,
so the GT can be compared with the source's default (unchecked "Animate") view, which it should match.
Writes PNG screenshots and measurements.json next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PAGES = {"gt": HERE.parent / "ground_truth.html", "source": HERE.parent / "source.html"}
VIEWPORTS = [(1280, 800), (375, 812)]

PROBE = """() => {
  const box = (el) => { const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
  const all = [...document.querySelectorAll('*')];
  return {
    article_transform: getComputedStyle(document.querySelector('article')).transform,
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    running_or_paused_animations: document.getAnimations().length,
    inputs: document.querySelectorAll('input').length,
    cubicles: document.querySelectorAll('.cubicle').length,
    boxes: {
      article: box(document.querySelector('article')),
      tower: box(document.querySelector('.tower')),
      panels: [...document.querySelectorAll('.panel')].map(box),
      computers: [...document.querySelectorAll('.computer')].map(box),
      kleenex: box(document.querySelector('.kleenex')),
      pencil_box: box(document.querySelector('.pencil-box')),
    },
  };
}"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, path in PAGES.items():
            for w, h in VIEWPORTS:
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto(path.as_uri(), wait_until="networkidle")
                page.wait_for_timeout(300)
                key = f"{name}_{w}x{h}"
                page.screenshot(path=str(HERE / f"{key}.png"))
                out[key] = page.evaluate(PROBE)
                page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
