"""GT self-check for case-239-T2: viewports x states (default, hovering the cassette, after leaving).

    python cases/case-239-T2/review_20261124/gt_check.py

Needs Playwright chromium and network access to cdnjs.cloudflare.com (jQuery) and public.codepenassets.com
(prefixfree). Writes PNG screenshots and measurements.json next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (500, 800)]
PARTS = [".cassette-scene", ".case-scene .ft", ".case-scene .tp", ".full-mask", "#reel-scene1", "#reel-scene2", ".cover-scene", ".shadow-shape1", ".shadow-shape2"]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            opacity: cs.opacity, boxShadow: cs.boxShadow, transform: cs.transform}; };
  const all = [...document.querySelectorAll('*')];
  return {
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    jquery: typeof window.jQuery,
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
            page.mouse.move(2, 2)
            page.screenshot(path=str(HERE / f"gt_{key}_default.png"))
            out[f"{key}_default"] = page.evaluate(PROBE, PARTS)
            page.hover(".full-mask")
            page.wait_for_timeout(100)  # no transition left, the end state should be immediate
            page.screenshot(path=str(HERE / f"gt_{key}_hover.png"))
            out[f"{key}_hover"] = page.evaluate(PROBE, PARTS)
            page.mouse.move(2, 2)
            page.wait_for_timeout(100)
            out[f"{key}_after_leave"] = page.evaluate(PROBE, PARTS)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
