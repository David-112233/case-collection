"""GT self-check for case-237-T3: viewports x states (default, after clicking power, after a volume notch, power off).

    python cases/case-237-T3/review_20261124/gt_check.py

Needs Playwright chromium and network access to fonts.googleapis.com (Bungee, Teko), public.codepenassets.com
(normalize.css) and cdnjs.cloudflare.com (Tone.js). Writes PNG screenshots and measurements.json next to this script.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
VIEWPORTS = [(1280, 800), (500, 800)]
PARTS = [".rplayer", ".record", ".record .label", ".tonebar", ".tonebar .bar", ".power", ".pbutton", ".knob", ".clickme", ".logo"]

PROBE = """(parts) => {
  const box = (sel) => { const el = document.querySelector(sel); if (!el) return null;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), transform: cs.transform, opacity: cs.opacity}; };
  const all = [...document.querySelectorAll('*')];
  return {
    running_animations: document.getAnimations().length,
    nonzero_transitions: all.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length,
    pwlight: getComputedStyle(document.documentElement).getPropertyValue('--pwlight'),
    spindiv: getComputedStyle(document.querySelector('.spindiv')).transform,
    tone: typeof window.Tone,
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
            page.screenshot(path=str(HERE / f"gt_{key}_default.png"))
            out[f"{key}_default"] = page.evaluate(PROBE, PARTS)
            page.click(".pbutton")
            page.wait_for_timeout(100)
            page.screenshot(path=str(HERE / f"gt_{key}_playing.png"))
            out[f"{key}_playing"] = page.evaluate(PROBE, PARTS)
            page.wait_for_timeout(2000)
            out[f"{key}_playing_after2s"] = page.evaluate(PROBE, PARTS)
            page.evaluate("document.querySelectorAll('.notch')[4].click()")
            page.screenshot(path=str(HERE / f"gt_{key}_volume5.png"))
            out[f"{key}_volume5"] = page.evaluate(PROBE, PARTS)
            page.click(".pbutton")
            page.wait_for_timeout(100)
            out[f"{key}_stopped"] = page.evaluate(PROBE, PARTS)
            out[f"{key}_failed_requests"] = failed
            page.close()
        browser.close()
    (HERE / "measurements.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
