"""GT 自检：1280 与 375 两个视口截图并测量 GLENN 五个字母及其伪元素的位置。

用法（仓库根目录）：python cases/case-230-T1/review_20261124/shot_gt.py
需要 playwright 和 chromium（python -m playwright install chromium）。
本作品无动画、无交互，只截初始状态。
"""
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"
SRC = HERE.parent / "source.html"

MEASURE = """() => {
  const spans = [...document.querySelectorAll('#logo span')];
  const out = spans.map(s => {
    const r = s.getBoundingClientRect();
    const cs = getComputedStyle(s), b = getComputedStyle(s, '::before'), a = getComputedStyle(s, '::after');
    return {letter: s.textContent, x: r.x, y: r.y, w: r.width, h: r.height,
            color: cs.color, fontSize: cs.fontSize, fontFamily: cs.fontFamily, fontWeight: cs.fontWeight,
            beforeTransform: b.transform, beforeShadow: b.textShadow,
            afterTransform: a.transform, afterFill: a.webkitTextFillColor, afterBg: a.backgroundImage};
  });
  const lines = new Set(out.map(o => Math.round(o.y))).size;
  return {viewport: [innerWidth, innerHeight], bodyBg: getComputedStyle(document.body).backgroundColor,
          scrollWidth: document.documentElement.scrollWidth, lines, letters: out,
          fontsCheck: document.fonts.check('bold 128px Helvetica')};
}"""

def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, path in (("gt", GT), ("source", SRC)):
            for w, h in ((1280, 800), (375, 812)):
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto(path.as_uri())
                page.wait_for_timeout(500)
                page.screenshot(path=str(HERE / f"{name}_{w}.png"), full_page=True)
                result[f"{name}_{w}"] = page.evaluate(MEASURE)
                page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in result.items():
        print(k, "lines:", v["lines"], "scrollWidth:", v["scrollWidth"])

if __name__ == "__main__":
    main()
