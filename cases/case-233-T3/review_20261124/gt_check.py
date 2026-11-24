"""GT self-check for case-233: two viewports x three states (default, How to? panel open, panel closed again),
plus a drag test that should change nothing now that camera.js is gone.

    python cases/case-233-T2/review_20261124/gt_check.py

Needs Playwright chromium and network access to fonts.googleapis.com and shadowshahriar.github.io (starter.css,
3d.css, howto.css and the cake textures). Writes PNG screenshots and measurements.json next to this script.
(If the case directory is renamed by `registry.py retier`, the script still works: it finds the GT by relative path.)
"""
import hashlib
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
SRC = HERE.parent / "source.html"
VIEWPORTS = [(1280, 800), (375, 812)]
PARTS = ["[data-camera]", "[data-scene]", ".plate", ".cake-base", ".spheres", ".cake-base-shadow", "#howto",
         "#howto [data-desc]", "#howto [data-close]", "#howto [data-desktop]", "#howto [data-mobile]", "[data-howto]"]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            display: cs.display, visibility: cs.visibility, opacity: cs.opacity, bg: cs.backgroundColor,
            color: cs.color, font: cs.fontFamily, transform: cs.transform}; };
  const all = [...document.querySelectorAll('*')];
  const root = getComputedStyle(document.documentElement);
  const cam = document.querySelector('[data-camera]'), camcs = cam ? getComputedStyle(cam) : null;
  return {
    hash: location.hash,
    running_animations: document.getAnimations().length,
    animation_names: [...new Set(all.map(e => getComputedStyle(e).animationName).filter(n => n !== 'none'))],
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0))
                            .map(e => e.tagName + (e.id ? '#' + e.id : '') + (e.className ? '.' + e.className : '')),
    autorotate_attr: cam ? cam.hasAttribute('data-autorotate') : null,
    px_var: root.getPropertyValue('--px'),
    camera_vars: camcs ? ['--perspective', '--cameraZ', '--cameraY', '--translateZ'].map(v => [v, camcs.getPropertyValue(v)]) : null,
    camera_perspective: camcs ? camcs.perspective : null,
    scene_transform: document.querySelector('[data-scene]') ? getComputedStyle(document.querySelector('[data-scene]')).transform : null,
    scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    parts: Object.fromEntries(parts.map(p => [p, box(p)])),
  };
}"""


def digest(png: bytes) -> str:
    return hashlib.sha256(png).hexdigest()[:16]


def run(browser, path: Path, tag: str, out: dict) -> None:
    for w, h in VIEWPORTS:
        page = browser.new_page(viewport={"width": w, "height": h})
        failed = []
        page.on("requestfailed", lambda r: failed.append(r.url))
        page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        page.goto(path.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(800)
        key = f"{tag}_{w}x{h}"
        a = page.screenshot(path=str(HERE / f"{key}_default.png"))
        out[f"{key}_default"] = page.evaluate(PROBE, PARTS)
        page.wait_for_timeout(1500)
        b = page.screenshot(path=str(HERE / f"{key}_default_after1500ms.png"))
        out[f"{key}_static_over_time"] = digest(a) == digest(b)
        if tag == "gt":
            # drag across the cake: with camera.js removed the picture should not change
            page.mouse.move(w / 2, h / 2)
            page.mouse.down()
            page.mouse.move(w / 2 + 150, h / 2 + 60, steps=10)
            page.mouse.up()
            page.wait_for_timeout(300)
            c = page.screenshot(path=str(HERE / f"{key}_after_drag.png"))
            out[f"{key}_unchanged_by_drag"] = digest(a) == digest(c)
            page.dblclick("[data-scene]")
            page.wait_for_timeout(1000)
            d = page.screenshot(path=str(HERE / f"{key}_after_dblclick.png"))
            out[f"{key}_unchanged_by_dblclick"] = digest(a) == digest(d)
            page.click("[data-howto]")
            page.wait_for_timeout(100)
            page.screenshot(path=str(HERE / f"{key}_howto_open.png"))
            out[f"{key}_howto_open"] = page.evaluate(PROBE, PARTS)
            page.wait_for_timeout(1000)
            page.screenshot(path=str(HERE / f"{key}_howto_open_after1000ms.png"))
            page.click("#howto [data-close]", force=True)
            page.wait_for_timeout(100)
            page.screenshot(path=str(HERE / f"{key}_howto_closed.png"))
            out[f"{key}_howto_closed"] = page.evaluate(PROBE, PARTS)
        out[f"{key}_failed_requests"] = failed
        page.close()


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        run(browser, GT, "gt", out)
        run(browser, SRC, "source", out)  # for side-by-side comparison of the default view
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
