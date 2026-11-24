"""GT self-check for case-235-T3 (fixed-view 3D office, WebGL canvas).

    python cases/case-235-T3/review_20261124/gt_check.py

Needs Playwright chromium with WebGL (headless chromium uses SwiftShader, which is fine) and network access to
cdnjs.cloudflare.com (three.js r124), unpkg.com (GLTFLoader 0.126), rawcdn.githack.com (11 .glb models,
baked.jpg, bg.jpg) and fonts.googleapis.com / fonts.gstatic.com (Montserrat).

For each viewport it waits until the loading overlay is hidden (room.glb loaded) and the network is idle,
takes a screenshot, takes a second one 1.5 s later and compares them (the page should be static), then clicks
the ceiling lamp and the chair positions and checks that nothing changes (all click interactions were removed).
Writes PNGs and measurements.json next to this script. 1836x1450 matches the target render the user supplied.
"""
import hashlib
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (1836, 1450), (375, 812)]
# Screen positions of the ceiling lamp and the chair seat at 1280x800, as fractions of the viewport,
# from projecting the model bounding boxes with the fixed camera (see static_check.md).
CLICKS = {"ceiling_lamp": (512 / 1280, 125 / 800), "chair": (567 / 1280, 523 / 800)}

PROBE = """() => {
  const loader = document.querySelector('#loader');
  const msg = document.querySelector('.message');
  const c = document.querySelector('canvas.webgl');
  const r = msg.getBoundingClientRect();
  return {
    loader_display: getComputedStyle(loader).display,
    body_bg: getComputedStyle(document.body).backgroundColor,
    bg_var: getComputedStyle(document.body).getPropertyValue('--bg').trim(),
    cursor: getComputedStyle(document.body).cursor,
    canvas_css: [c.clientWidth, c.clientHeight],
    canvas_px: [c.width, c.height],
    message_visible: msg.classList.contains('is-visible'),
    message_box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
    page_scroll: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    three: typeof window.THREE === 'object' ? window.THREE.REVISION : null,
    gltf_loader: typeof (window.THREE && window.THREE.GLTFLoader),
    orbit_controls: typeof (window.THREE && window.THREE.OrbitControls),
    camera_note: 'camera is a script-local const; position is (18,6,18) scaled to length 16',
  };
}"""


def digest(png: bytes) -> str:
    return hashlib.sha256(png).hexdigest()[:16]


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        for w, h in VIEWPORTS:
            key = f"{w}x{h}"
            page = browser.new_page(viewport={"width": w, "height": h})
            failed, errors = [], []
            page.on("requestfailed", lambda r: failed.append(r.url))
            page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(GT.as_uri(), wait_until="networkidle", timeout=120_000)
            try:
                page.wait_for_function("getComputedStyle(document.querySelector('#loader')).display === 'none'", timeout=60_000)
            except Exception as e:  # room.glb did not load: keep going so the failure is recorded
                errors.append(f"loader still visible: {e}")
            page.wait_for_timeout(3000)  # textures are loaded asynchronously after the models
            a = page.screenshot(path=str(HERE / f"gt_{key}.png"))
            page.wait_for_timeout(1500)
            b = page.screenshot(path=str(HERE / f"gt_{key}_after1500ms.png"))
            rec = {"probe": page.evaluate(PROBE), "static_over_1500ms": digest(a) == digest(b)}
            for name, (fx, fy) in CLICKS.items():
                page.mouse.click(fx * w, fy * h)
                page.wait_for_timeout(800)
                c = page.screenshot()
                rec[f"unchanged_after_click_{name}"] = digest(c) == digest(a)
            rec["probe_after_clicks"] = page.evaluate(PROBE)
            rec["failed_requests"] = failed
            rec["page_errors"] = errors
            out[key] = rec
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
