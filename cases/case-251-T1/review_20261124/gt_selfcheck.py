"""case-251 GT 自检脚本：多视口截图 + 测量。

用法（仓库根目录）：
    python cases/case-251-T1/review_20261124/gt_selfcheck.py

需要 requirements.txt 里的 playwright 和 chromium 浏览器。
来源有两个断点（39em≈624px、15em≈240px），所以在 1280、600、375 三个宽度下各截整页，并测量
四张卡片的位置尺寸与圆角、编号色块与图标块的位置和斜切变换、KoHo 字体与背景图是否加载、运行中的动画数。
结果写到本目录：gt_<宽度>.png、measure.json（截图不入库）。
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

MEASURE_JS = """
async () => {
  const r = (b) => ({x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1)});
  await document.fonts.ready;
  const bgUrl = 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/2017/kreator_rockharz_july_2018.jpg';
  const bgLoaded = await new Promise(res => { const i = new Image(); i.onload = () => res([i.naturalWidth, i.naturalHeight]);
                                              i.onerror = () => res(false); i.src = bgUrl; });
  return {
    koho_900: document.fonts.check('900 28px KoHo'),
    koho_400: document.fonts.check('400 16px KoHo'),
    background_image: bgLoaded,
    articles: [...document.querySelectorAll('article')].map(a => {
      const cs = getComputedStyle(a), b = getComputedStyle(a, '::before'), af = getComputedStyle(a, '::after');
      const h3 = a.querySelector('h3'), h3a = getComputedStyle(h3, '::after'), h3b = getComputedStyle(h3, '::before');
      return {box: r(a.getBoundingClientRect()), radius: cs.borderRadius, columns: cs.gridTemplateColumns,
              rows: cs.gridTemplateRows, before_transform: b.transform, after_transform: af.transform,
              icon: a.dataset.icon, number: h3b.content, h3_box: r(h3.getBoundingClientRect()),
              h3_after_transform: h3a.transform, title: a.querySelector('h4').textContent,
              title_color: getComputedStyle(a.querySelector('h4')).color,
              text: a.querySelector('p').textContent, text_box: r(a.querySelector('p').getBoundingClientRect())};
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
        for w in (1280, 600, 375):
            page = browser.new_page(viewport={"width": w, "height": 900})
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=str(HERE / f"gt_{w}.png"), full_page=True)
            result[str(w)] = page.evaluate(MEASURE_JS)
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in result.items():
        print(k, v["koho_900"], bool(v["background_image"]), v["running_animations"], v["scroll"])


if __name__ == "__main__":
    main()
