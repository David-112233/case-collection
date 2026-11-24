"""case-249 GT 自检脚本：双视口、点击前后截图 + 状态测量。

用法（仓库根目录）：
    python cases/case-249-T3/review_20261124/gt_selfcheck.py

需要 requirements.txt 里的 playwright 和 chromium 浏览器。
对 ground_truth.html 在 1280×900 与 375×812 下各截两张：默认态（仓门打开）和点击播放键后（仓门合上、
播放键按下、地面声波条出现）。同时记录运行中的动画数、相关类名、音频是否开始播放、仓门变换矩阵。
结果写到本目录：gt_<视口>_default.png、gt_<视口>_playing.png、measure.json（截图不入库）。
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
GT = HERE.parent / "ground_truth.html"

STATE_JS = """
() => {
  const q = (s) => document.querySelector(s);
  const a = q('#a');
  return {
    running_animations: document.getAnimations().length,
    button_class: q('.button5').className,
    lid_class: q('.c').className,
    lid_transform: getComputedStyle(q('.c')).transform,
    button_left: getComputedStyle(q('.button5')).left,
    waves_visible: getComputedStyle(q('.waves')).visibility,
    wave_heights: [...document.querySelectorAll('.wave')].map(w => +w.getBoundingClientRect().height.toFixed(1)),
    audio: {paused: a.paused, currentTime: +a.currentTime.toFixed(2), readyState: a.readyState,
            duration: a.duration, src: a.currentSrc.split('/').pop()},
    scroll: {w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight,
             vw: innerWidth, vh: innerHeight},
  };
}
"""


def main():
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        for name, vp in (("1280", {"width": 1280, "height": 900}), ("375", {"width": 375, "height": 812})):
            page = browser.new_page(viewport=vp)
            page.goto(GT.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=str(HERE / f"gt_{name}_default.png"))
            r = {"default": page.evaluate(STATE_JS)}
            page.evaluate("document.querySelector('.button5').click()")
            page.wait_for_timeout(800)
            page.screenshot(path=str(HERE / f"gt_{name}_playing.png"))
            r["playing"] = page.evaluate(STATE_JS)
            # 播放中再点一次：来源在播放时移除了点击监听，状态不应变化
            page.evaluate("document.querySelector('.button5').click()")
            page.wait_for_timeout(300)
            r["second_click"] = page.evaluate(STATE_JS)
            result[name] = r
            page.close()
        browser.close()
    (HERE / "measure.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in result.items():
        print(k, {s: (v[s]["running_animations"], v[s]["lid_class"], v[s]["audio"]["paused"]) for s in v})


if __name__ == "__main__":
    main()
