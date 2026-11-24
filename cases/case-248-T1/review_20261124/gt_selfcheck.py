"""case-248 GT 自检脚本：双视口截图 + 测量。

用法（仓库根目录）：
    python cases/case-248-T1/review_20261124/gt_selfcheck.py

需要 requirements.txt 里的 playwright 和 chromium 浏览器。
本作品没有交互和动画，只截静止状态；同时检查外部重置样式表和三张图片是否加载、
页面上有没有正在运行的动画、六块折面的折痕位置。
结果写到本目录：gt_1280.png、gt_375.png、measure.json（截图不入库）。
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

MEASURE_JS = """
() => {
  const r = (el) => { const b = el.getBoundingClientRect();
    return {x: +b.x.toFixed(1), y: +b.y.toFixed(1), w: +b.width.toFixed(1), h: +b.height.toFixed(1)}; };
  const out = {};
  out.container = r(document.querySelector('.container'));
  out.plain = [...document.querySelectorAll('.container > img')].map(r);
  out.posters = [...document.querySelectorAll('.poster')].map(el => {
    const cs = getComputedStyle(el), b = getComputedStyle(el, '::before'), a = getComputedStyle(el, '::after');
    return {box: r(el), img: r(el.querySelector('img')), padding: cs.paddingLeft, filter: cs.filter,
            shadow: cs.boxShadow, before_h: b.height, before_bottom: b.bottom, after_h: a.height};
  });
  out.images = [...document.images].map(i => ({src: i.src.split('/').pop(), complete: i.complete,
                                              natural: [i.naturalWidth, i.naturalHeight]}));
  out.reset_loaded = [...document.styleSheets].some(s => (s.href || '').includes('reset-2.0'))
                     && getComputedStyle(document.body).marginTop === '0px';
  out.body_bg = getComputedStyle(document.body).backgroundColor;
  out.running_animations = document.getAnimations().length;
  out.scroll = {w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight,
                vw: innerWidth, vh: innerHeight};
  return out;
}
"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, vp in (("1280", {"width": 1280, "height": 900}), ("375", {"width": 375, "height": 812})):
            page = browser.new_page(viewport=vp)
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=str(HERE / f"gt_{name}.png"), full_page=True)
            result[name] = page.evaluate(MEASURE_JS)
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: {"animations": v["running_animations"], "reset": v["reset_loaded"],
                          "images": [i["complete"] for i in v["images"]], "scroll": v["scroll"]}
                      for k, v in result.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
