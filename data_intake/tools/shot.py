"""Headless screenshots for case authoring checks (Playwright Chromium, same stack as evaluation).

shot.py FILE OUT_PREFIX [--widths=1280,768,375] [--height=900] [--full] [--offline] [--eval=JS] [--wait=ms]
--offline aborts every non-file request and prints them (GT must report none).
--eval runs JS before each screenshot (e.g. scroll or click) and prints its JSON result.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) if "=" in a else (a[2:], "1") for a in sys.argv[1:] if a.startswith("--"))
page_file = Path(args[0]).resolve()
prefix = Path(args[1])
prefix.parent.mkdir(parents=True, exist_ok=True)
if "evalfile" in opts:
    opts["eval"] = Path(opts["evalfile"]).read_text(encoding="utf-8")
widths = [int(w) for w in opts.get("widths", "1280,768,375").split(",")]
height = int(opts.get("height", 900))

with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in widths:
        ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        page = ctx.new_page()
        blocked = []
        if "offline" in opts:
            def guard(route):
                if route.request.url.startswith("file:") or route.request.url.startswith("data:"):
                    route.continue_()
                else:
                    blocked.append(route.request.url)
                    route.abort()
            page.route("**/*", guard)
        page.goto(page_file.as_uri(), wait_until="load", timeout=30000)
        page.wait_for_timeout(int(opts.get("wait", 800)))
        for xy in filter(None, opts.get("click", "").split(";")):
            x, y = (float(v) for v in xy.split(","))
            page.mouse.click(x, y)
            page.wait_for_timeout(int(opts.get("clickwait", 1200)))
        if "eval" in opts:
            print(width, "eval:", json.dumps(page.evaluate(opts["eval"]), ensure_ascii=False))
            page.wait_for_timeout(400)
        out = prefix.with_name(f"{prefix.name}_{width}.png")
        page.screenshot(path=str(out), full_page="full" in opts)
        print(width, "->", out, "blocked:" if blocked else "", blocked[:5] if blocked else "")
        ctx.close()
    browser.close()
