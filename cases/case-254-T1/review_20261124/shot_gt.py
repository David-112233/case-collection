"""GT 自检：1280、500、375 三个视口截图，隔 2 秒再截一次确认静止，并测量灯塔、光束、帆船、月亮的位置。

用法（仓库根目录）：python cases/case-254-T2/review_20261124/shot_gt.py
需要 playwright 和 chromium（python -m playwright install chromium）。GT 不加载外部资源。
"""
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

MEASURE = """() => {
  const box = sel => { const e = document.querySelector(sel); if (!e) return null;
    const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
  const anims = document.getAnimations().length;
  return {viewport: [innerWidth, innerHeight], running_animations: anims,
          lighthouse: box('.lighthouse'), light: box('.light'), boat: box('.boat'), moon: box('.moon'),
          mountains: [...document.querySelectorAll('.mountain')].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width)]; }),
          glow_opacity: getComputedStyle(document.querySelector('.glow')).opacity};
}"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in ((1280, 800), (500, 800), (375, 812)):
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(GT.as_uri())
            page.wait_for_timeout(500)
            a = page.screenshot(path=str(HERE / f"gt_{w}.png"))
            page.wait_for_timeout(2000)
            b = page.screenshot()
            result[f"gt_{w}"] = page.evaluate(MEASURE) | {"static_over_2s": a == b}
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in result.items():
        print(k, "animations:", v["running_animations"], "static:", v["static_over_2s"])


if __name__ == "__main__":
    main()
