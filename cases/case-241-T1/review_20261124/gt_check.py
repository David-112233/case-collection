"""GT self-check for case-241-T1 (static page, no interaction): full-page screenshots and measurements.

    python cases/case-241-T1/review_20261124/gt_check.py

Needs Playwright chromium; the page has no external resources. Writes PNG screenshots and measurements.json
next to this script. 375 wide is below the source's 992px breakpoint (circles switch to one horizontal row).
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (375, 812)]

PROBE = """() => {
  const box = (el) => { const r = el.getBoundingClientRect(); return [Math.round(r.x + scrollX), Math.round(r.y + scrollY), Math.round(r.width), Math.round(r.height)]; };
  const all = [...document.querySelectorAll('*')];
  const names = ['one', 'two', 'three', 'four', 'five', 'six'];
  return {
    body_bg: getComputedStyle(document.body).backgroundColor,
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    circles: Object.fromEntries(names.map(n => { const c = document.querySelector('.circle.' + n);
      return [n, {circle: box(c), number: c.querySelector('i').textContent, heading: box(c.querySelector('h2')),
                  text_block: box(c.querySelector('.content-container')), line: box(c.querySelector('.line')),
                  dot: c.querySelector('.dot') ? box(c.querySelector('.dot')) : null}]; })),
  };
}"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(300)
            key = f"{w}x{h}"
            page.screenshot(path=str(HERE / f"gt_{key}.png"), full_page=True)
            out[key] = page.evaluate(PROBE)
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
