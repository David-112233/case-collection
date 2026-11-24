"""GT self-check for case-228-T3: two viewports x two states (default, after clicking the wheel).

    python cases/case-228-T3/review_20261124/gt_check.py

Needs Playwright chromium and network access to cdnjs.cloudflare.com (jQuery), use.fontawesome.com (icons),
pro.fontawesome.com and public.codepenassets.com (prefixfree). Writes PNG screenshots and measurements.json
next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (375, 812)]
PARTS = [".shadow-shape", ".case-scene", ".cub-1 .tp", ".cub-1 .ft", ".cub-1 .rt", ".screen-scene", ".wheel-scene", ".light-scene"]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            display: cs.display, opacity: cs.opacity, bg: cs.backgroundColor}; };
  const all = [...document.querySelectorAll('*')];
  return {
    body_bg: getComputedStyle(document.body).backgroundColor,
    body_class: document.body.className,
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    nonzero_animation_names: all.filter(e => getComputedStyle(e).animationName !== 'none').length,
    icons_as_svg: document.querySelectorAll('.wheel-scene svg').length,
    icons_left_as_i: document.querySelectorAll('.wheel-scene i').length,
    icon_boxes: [...document.querySelectorAll('.wheel-scene svg')].map(s => { const r = s.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; }),
    jquery: typeof window.jQuery,
    fontawesome: typeof window.FontAwesome,
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
            page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(500)
            key = f"{w}x{h}"
            page.screenshot(path=str(HERE / f"gt_{key}_default.png"))
            out[f"{key}_default"] = page.evaluate(PROBE, PARTS)
            page.click(".wheel-scene")
            page.wait_for_timeout(100)  # no transition left, the end state should be immediate
            page.screenshot(path=str(HERE / f"gt_{key}_glow.png"))
            out[f"{key}_glow"] = page.evaluate(PROBE, PARTS)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(HERE / f"gt_{key}_glow_after1500ms.png"))
            page.click(".wheel-scene")
            page.wait_for_timeout(100)
            out[f"{key}_back_to_default"] = page.evaluate(PROBE, PARTS)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
