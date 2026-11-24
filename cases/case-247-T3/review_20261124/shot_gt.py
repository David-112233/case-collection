"""GT self-check for case-247-T3: screenshots at 1280x800 and 500x800 in four states (default, night, zoom, night+zoom).

    python cases/case-247-T3/review_20261124/shot_gt.py

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
  nonzero_transitions: [...document.querySelectorAll('*')].filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
  dark: document.querySelector('#dark').checked, zoom: document.querySelector('#zoom').checked,
  bg: getComputedStyle(document.querySelector('.scene__wrapper')).backgroundColor,
  chair_opacity: getComputedStyle(document.querySelector('.chair__base')).opacity,
  labels_visible: [...document.querySelectorAll('label')].map(l => [l.htmlFor, getComputedStyle(l).display]),
})"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in [(1280, 800), (500, 800)]:
            page = browser.new_page(viewport={"width": w, "height": h})
            failed = []
            page.on("requestfailed", lambda r: failed.append(r.url))
            page.goto(GT.as_uri(), wait_until="networkidle")
            for state, clicks in [("default", []), ("night", ["dark"]), ("night_zoom", ["zoom"]), ("zoom", ["dark"])]:
                for c in clicks:
                    # the light label is hidden while zoomed, so toggle the checkbox itself
                    page.evaluate("(id) => document.getElementById(id).click()", c)
                page.wait_for_timeout(300)
                page.screenshot(path=str(HERE / f"gt_{w}x{h}_{state}.png"))
                out[f"{w}x{h}_{state}"] = page.evaluate(PROBE)
            out[f"{w}x{h}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
