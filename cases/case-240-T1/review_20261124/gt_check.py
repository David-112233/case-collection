"""GT self-check for case-240-T1 (static page, no interaction): full-page screenshots and measurements.

    python cases/case-240-T1/review_20261124/gt_check.py

Needs Playwright chromium and network access to fonts.googleapis.com / fonts.gstatic.com.
Writes PNG screenshots and measurements.json next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (375, 812)]
PARTS = [".op", ".keyboard", ".speaker", ".sw2", ".display", ".sw4__1", ".sw4__2", ".sw4__3", ".sw4__4",
         ".r1c17", ".r2c17", ".name", ".fourDots", ".fiveDots"]

PROBE = """(parts) => {
  const box = (el) => { const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
  const all = [...document.querySelectorAll('*')];
  return {
    body_bg: getComputedStyle(document.body).backgroundColor,
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    fonts_loaded: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight),
    row3_buttons: document.querySelectorAll('[class*="btn__base r3c"]').length,
    black_keys: [...document.querySelectorAll('.btn__base__left, .btn__base__mid, .btn__base__right')].map(e => box(e)),
    white_keys: [...document.querySelectorAll('.keys__white')].map(e => box(e)),
    parts: Object.fromEntries(parts.map(p => { const el = document.querySelector(p); return [p, el ? box(el) : null]; })),
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
            page.screenshot(path=str(HERE / f"gt_{key}.png"), full_page=True)
            out[key] = page.evaluate(PROBE, PARTS)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
