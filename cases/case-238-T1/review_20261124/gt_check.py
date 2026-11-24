"""GT self-check for case-238-T1: two viewports, default state only (the GT has no dynamics).

    python cases/case-238-T1/review_20261124/gt_check.py

Needs Playwright chromium and network access to fonts.googleapis.com (Gochi Hand). Writes PNG screenshots
(viewport and full page) and measurements.json next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (500, 800)]
PARTS = [".wrap", ".cassette", ".cassette .label", "#mix", ".reels", ".window", ".head", ".cassetteCase"]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect();
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}; };
  return {
    running_animations: document.getAnimations().length,
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family),
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
            page.screenshot(path=str(HERE / f"gt_{key}_full.png"), full_page=True)
            out[key] = page.evaluate(PROBE, PARTS)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
