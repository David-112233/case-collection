"""GT self-check for case-242-T1 (static CSS 3D room, no interaction): screenshots and measurements.

    python cases/case-242-T1/review_20261124/gt_check.py [--headed]

Needs Playwright chromium and network access to codepen.io (the author's eYLjgaq.css / .js). Run it once headless
and once with --headed on a machine with a GPU: the cloud browser drew large white gaps in the walls and floor,
and the point of this script is to tell whether those gaps are real or a software-renderer artefact.
Writes PNG screenshots and measurements.json next to this script.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (375, 812)]
HEADED = "--headed" in sys.argv

PROBE = """() => {
  const all = [...document.querySelectorAll('*')];
  return {
    html_font_size: getComputedStyle(document.documentElement).fontSize,
    body_bg: getComputedStyle(document.body).backgroundColor,
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    stylesheets: [...document.styleSheets].map(s => { try { return [s.href, s.cssRules.length]; } catch (e) { return [s.href, 'unreadable']; } }),
    sig_element: !!document.querySelector('.sig'),
    fan_rotor_transform: getComputedStyle(document.querySelector('light > u:nth-of-type(5)')).transform,
  };
}"""


def main() -> None:
    out = {}
    tag = "headed" if HEADED else "headless"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED)
        for w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            failed = []
            page.on("requestfailed", lambda r: failed.append(r.url))
            page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(500)
            key = f"{tag}_{w}x{h}"
            page.screenshot(path=str(HERE / f"gt_{key}.png"))
            out[key] = page.evaluate(PROBE)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / f"measurements_{tag}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
