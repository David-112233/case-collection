"""GT 自检：宽屏 1280、窄屏 500 与 375 三个视口截图，并测量四条横幅及其编号圆标、斜切标签。

用法（仓库根目录）：python cases/case-252-T1/review_20261124/shot_gt.py
需要 playwright 和 chromium（python -m playwright install chromium）。
本作品无动画、无交互，只截初始状态；另截一次 1 秒后的画面确认静止。
"""
import json
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

MEASURE = """() => {
  const arts = [...document.querySelectorAll('article')].map(a => {
    const r = a.getBoundingClientRect(), cs = getComputedStyle(a);
    const b = getComputedStyle(a, '::before'), af = getComputedStyle(a, '::after');
    const h = a.querySelector('h3').getBoundingClientRect(), p = a.querySelector('p').getBoundingClientRect();
    return {x: r.x, y: r.y, w: r.width, h: r.height, radius: cs.borderRadius, clip: cs.clipPath,
            before: {content: b.content, transform: b.transform, w: b.width, h: b.height},
            after: {content: af.content, w: af.width, h: af.height, color: af.color},
            h3: [h.x, h.y, h.width, h.height], p: [p.x, p.y, p.width, p.height]};
  });
  return {viewport: [innerWidth, innerHeight], scrollWidth: document.documentElement.scrollWidth,
          font: getComputedStyle(document.querySelector('article')).fontFamily, articles: arts};
}"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in ((1280, 800), (500, 800), (375, 812)):
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(GT.as_uri())
            page.wait_for_timeout(800)
            a = page.screenshot(path=str(HERE / f"gt_{w}.png"), full_page=True)
            page.wait_for_timeout(1000)
            b = page.screenshot(full_page=True)
            result[f"gt_{w}"] = page.evaluate(MEASURE) | {"static_over_1s": a == b}
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in result.items():
        print(k, "scrollWidth:", v["scrollWidth"], "static:", v["static_over_1s"])


if __name__ == "__main__":
    main()
