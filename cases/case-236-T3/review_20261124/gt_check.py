"""GT self-check for case-236-T1: two viewports, default state only (the GT has no interaction).

    python cases/case-236-T1/review_20261124/gt_check.py

Needs Playwright chromium. The GT loads no external resource. Writes PNG screenshots and measurements.json
next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (500, 800), (375, 812)]
PARTS = [".main", ".shadows", ".a__top", ".b__top", ".c__top", ".screen", ".btn-b01", ".btn-b02", ".btn-09", ".at__top", ".bt__top"]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect();
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; };
  const all = [...document.querySelectorAll('*')];
  return {
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    main_transform: getComputedStyle(document.querySelector('.main')).transform,
    parts: Object.fromEntries(parts.map(p => [p, box(p)])),
  };
}"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            failed = []
            page.on("requestfailed", lambda r: failed.append(r.url))
            page.goto(GT.as_uri(), wait_until="networkidle")
            key = f"{w}x{h}"
            page.screenshot(path=str(HERE / f"gt_{key}.png"))
            out[key] = page.evaluate(PROBE, PARTS)
            # dragging and the wheel did change the view in the source; the GT must stay put
            page.mouse.move(w * 0.3, h * 0.3)
            page.mouse.down()
            page.mouse.move(w * 0.7, h * 0.6, steps=5)
            page.mouse.up()
            page.mouse.wheel(0, 300)
            page.wait_for_timeout(300)
            out[f"{key}_after_drag_and_wheel"] = page.evaluate(PROBE, PARTS)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
