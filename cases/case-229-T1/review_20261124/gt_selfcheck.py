"""case-229 GT 自检脚本：双视口截图 + 测量。

用法（仓库根目录）：
    python cases/case-229-T1/review_20261124/gt_selfcheck.py

需要 requirements.txt 里的 playwright 和 chromium 浏览器。
本作品没有任何交互和动画，所以只截静止状态；同时检查页面上没有正在运行的动画或过渡。
结果写到本目录：gt_1280.png、gt_375.png、measure.json。
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

SELECTORS = [
    ".casio", ".speaker", ".logo", ".logo h1", ".controls", ".controls-labels p",
    ".controls-bar", ".mode-container", ".mode-handle", ".volume-container",
    ".volume-handle", ".tone-container", ".tone-handle", ".btn", ".bigbtn",
    ".keys-container", ".white", ".white .key", ".black .key",
]

MEASURE_JS = """
(sels) => {
  const r = (el) => { const b = el.getBoundingClientRect();
    return {x: +b.x.toFixed(2), y: +b.y.toFixed(2), w: +b.width.toFixed(2), h: +b.height.toFixed(2)}; };
  const out = {};
  for (const s of sels) out[s] = [...document.querySelectorAll(s)].map(r);
  out.labels = [...document.querySelectorAll('.controls-labels p')].map(p => p.textContent);
  out.logo_text = document.querySelector('.logo h1').innerText;
  out.logo_font = getComputedStyle(document.querySelector('.logo h1')).fontFamily;
  out.montserrat_loaded = document.fonts.check('800 12px Montserrat');
  out.running_animations = document.getAnimations().length;
  out.scroll = {w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight,
                vw: innerWidth, vh: innerHeight};
  // 每个黑键跨在哪两个白键之间
  const whites = [...document.querySelectorAll('.white .key')].map(e => e.getBoundingClientRect());
  out.black_straddle = [...document.querySelectorAll('.black .key')].map(e => {
    const b = e.getBoundingClientRect();
    return whites.map((w, i) => [i + 1, Math.min(b.right, w.right) - Math.max(b.left, w.left)])
                 .filter(([, ov]) => ov > 0).map(([i, ov]) => [i, +ov.toFixed(2)]);
  });
  return out;
}
"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, vp in (("1280", {"width": 1280, "height": 800}), ("375", {"width": 375, "height": 812})):
            page = browser.new_page(viewport=vp)
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(500)
            page.screenshot(path=str(HERE / f"gt_{name}.png"), full_page=True)
            result[name] = page.evaluate(MEASURE_JS, SELECTORS)
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: {"animations": v["running_animations"], "font": v["montserrat_loaded"],
                          "scroll": v["scroll"]} for k, v in result.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
