"""GT 自检：1280、500、375 三个视口截图；按下数字键 5 不放时再截一次，松开后再截一次，并测量键帽位置。

用法（仓库根目录）：python cases/case-253-T2/review_20261124/shot_gt.py
需要 playwright 和 chromium（python -m playwright install chromium）。
GT 依赖 esm.sh 上的 React 19 与 Google Fonts，需联网。按键会触发来源的点击音效，无头浏览器下可能被拦截，不影响画面。
"""
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

MEASURE = """() => {
  const keys = [...document.querySelectorAll('.key')].map(k => {
    const r = k.querySelector('.top').getBoundingClientRect();
    return {char: k.textContent, cls: k.className, transform: getComputedStyle(k).transform,
            transition: getComputedStyle(k).transitionDuration, x: Math.round(r.x), y: Math.round(r.y)};
  });
  return {viewport: [innerWidth, innerHeight], keys,
          font: getComputedStyle(document.querySelector('.char') || document.body).fontFamily,
          bioRhyme: document.fonts.check('700 64px BioRhyme')};
}"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in ((1280, 800), (500, 800), (375, 812)):
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(GT.as_uri())
            page.wait_for_selector(".key")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(HERE / f"gt_{w}_idle.png"))
            idle = page.evaluate(MEASURE)
            page.keyboard.down("5")
            page.wait_for_timeout(50)
            page.screenshot(path=str(HERE / f"gt_{w}_press5.png"))
            pressed = page.evaluate(MEASURE)
            page.keyboard.up("5")
            page.wait_for_timeout(50)
            page.screenshot(path=str(HERE / f"gt_{w}_release.png"))
            released = page.evaluate(MEASURE)
            result[f"gt_{w}"] = {"idle": idle, "pressed_5": pressed, "released": released}
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in result.items():
        moved = [a["char"] for a, b in zip(v["idle"]["keys"], v["pressed_5"]["keys"]) if (a["x"], a["y"]) != (b["x"], b["y"])]
        print(k, "keys moved while 5 held:", moved)


if __name__ == "__main__":
    main()
