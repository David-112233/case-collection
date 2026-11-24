"""GT self-check for case-231-T3: two viewports x states (default, hover, playing, back to default).

    python cases/case-231-T3/review_20261124/gt_check.py

Needs Playwright chromium. The only external resource left in the GT is the song
(raw.githubusercontent.com/ricardoolivaalonso/recursos/master/asiatic-a/song.mp3); headless
Chromium is started with autoplay allowed so that play() after the click is not refused.
Writes PNG screenshots and measurements.json next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (375, 812)]
PARTS = [".shadows", ".shadow-1", ".radio", ".bf__front", ".bf__top", ".ffa__front", ".ffa__front-circles",
         ".ffa__right", ".range", ".ffc__front", ".ffd__front", ".cassete__front", ".cover-b__front",
         ".button--cta .button__front", ".button:nth-of-type(1) .button__front", "#soff", "#son"]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
            display: cs.display, bg: cs.backgroundColor, transform: cs.transform}; };
  const all = [...document.querySelectorAll('*')];
  const a = document.querySelector('#audio');
  return {
    body_bg: getComputedStyle(document.body).backgroundColor,
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    nonzero_animation_names: all.filter(e => getComputedStyle(e).animationName !== 'none').length,
    classes: {radio: document.querySelector('#radio').className, cover: document.querySelector('#cover').className,
              cta: document.querySelector('#button-cta').className},
    audio: {paused: a.paused, loop: a.loop, currentTime: a.currentTime, readyState: a.readyState,
            networkState: a.networkState, error: a.error && a.error.code},
    parts: Object.fromEntries(parts.map(p => [p, box(p)])),
  };
}"""


def main() -> None:
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
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
            # hover the orange key: its front face should darken, nothing else changes
            page.hover(".button--cta .button__front", force=True)
            page.wait_for_timeout(100)
            page.screenshot(path=str(HERE / f"gt_{key}_hover_cta.png"))
            out[f"{key}_hover_cta"] = page.evaluate(PROBE, PARTS)
            page.hover("#soff")
            page.wait_for_timeout(100)
            out[f"{key}_hover_icon"] = page.evaluate(PROBE, PARTS)
            # play: click the orange key (the radio has no transitions left, the end state is immediate)
            page.click(".button--cta .button__front", force=True)
            page.mouse.move(0, h - 1)
            page.wait_for_timeout(100)
            page.screenshot(path=str(HERE / f"gt_{key}_playing.png"))
            out[f"{key}_playing"] = page.evaluate(PROBE, PARTS)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(HERE / f"gt_{key}_playing_after1500ms.png"))
            out[f"{key}_playing_after1500ms"] = page.evaluate(PROBE, PARTS)
            # stop via the speaker icon
            page.click("#son")
            page.mouse.move(0, h - 1)
            page.wait_for_timeout(100)
            page.screenshot(path=str(HERE / f"gt_{key}_back_to_default.png"))
            out[f"{key}_back_to_default"] = page.evaluate(PROBE, PARTS)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
