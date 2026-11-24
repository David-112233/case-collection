"""case-250 GT 自检脚本：多视口截图 + 测量。

用法（仓库根目录）：
    python cases/case-250-T1/review_20261124/gt_selfcheck.py

需要 requirements.txt 里的 playwright 和 chromium 浏览器。
来源有三个断点（625、480、225px），所以在 1280、600、450、375 四个宽度下各截整页，并测量
四条横幅的位置尺寸、左右错开方向、编号圆片的位置与文字、标题图标、运行中的动画数、是否横向溢出。
结果写到本目录：gt_<宽度>.png、measure.json（截图不入库）。
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

MEASURE_JS = """
() => {
  const r = (b) => ({x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1)});
  return {
    articles: [...document.querySelectorAll('article')].map(a => {
      const cs = getComputedStyle(a), bf = getComputedStyle(a, '::before');
      return {box: r(a.getBoundingClientRect()), transform: cs.transform, display: cs.display,
              radius: cs.borderRadius, bg: cs.backgroundImage.slice(0, 80),
              number: bf.content, number_font: bf.fontSize, number_w: bf.width, number_h: bf.height,
              number_bg: bf.backgroundImage.slice(0, 60), number_color: bf.color,
              title: a.querySelector('h3').textContent, icon: a.querySelector('h3').dataset.icon,
              title_box: r(a.querySelector('h3').getBoundingClientRect()),
              text_box: r(a.querySelector('p').getBoundingClientRect())};
    }),
    running_animations: document.getAnimations().length,
    scroll: {w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight,
             vw: innerWidth, vh: innerHeight},
  };
}
"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in (1280, 600, 450, 375):
            page = browser.new_page(viewport={"width": w, "height": 900})
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(300)
            page.screenshot(path=str(HERE / f"gt_{w}.png"), full_page=True)
            result[str(w)] = page.evaluate(MEASURE_JS)
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in result.items():
        print(k, v["running_animations"], v["scroll"], [a["box"]["x"] for a in v["articles"]])


if __name__ == "__main__":
    main()
