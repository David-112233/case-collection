"""case-232 GT 自检：1280 / 375 双视口，默认态与逐张卡片悬停态截图 + 测量；默认态与 source.html 像素比对。
用法：python cases/case-232-T2/review_20261124/gt_selfcheck.py
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
CASE = HERE.parent
VIEWPORTS = {"1280": (1280, 900), "375": (375, 812)}

MEASURE = """() => {
  const r = e => { const b = e.getBoundingClientRect(); return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; };
  const cards = [...document.querySelectorAll('.articles__article')].map(li => {
    const link = li.querySelector('.articles__link');
    const rhs = li.querySelector('.articles__content--rhs');
    const lhs = li.querySelector('.articles__content--lhs');
    const after = getComputedStyle(link, '::after');
    const before = getComputedStyle(li, '::before');
    return {
      card: r(li), title: lhs.querySelector('.articles__title').textContent.trim(),
      footer: [...lhs.querySelectorAll('.articles__footer > *')].map(e => e.textContent.trim()),
      rhs_transform: getComputedStyle(rhs).transform, rhs_bg: getComputedStyle(rhs).backgroundColor,
      rhs_visual: r(rhs),
      lhs_bg: getComputedStyle(lhs).backgroundColor,
      link_bg: getComputedStyle(link).backgroundColor, link_perspective: getComputedStyle(link).perspective,
      arrow_opacity: after.opacity, arrow_transform: after.transform,
      backplate: {top: before.top, left: before.left, w: before.width, h: before.height, border: before.borderStyle + ' ' + before.borderWidth},
      title_font: getComputedStyle(lhs.querySelector('.articles__title')).fontFamily + ' ' + getComputedStyle(lhs.querySelector('.articles__title')).fontWeight,
    };
  });
  return {
    body_bg: getComputedStyle(document.body).backgroundColor,
    scroll_w: document.documentElement.scrollWidth, client_w: document.documentElement.clientWidth,
    bitter_400: document.fonts.check('400 16px Bitter'), bitter_700: document.fonts.check('700 16px Bitter'),
    running_animations: document.getAnimations().length,
    cards,
  };
}"""


def shoot(page, path, full=True):
    page.screenshot(path=str(HERE / path), full_page=full)


def main():
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, (w, h) in VIEWPORTS.items():
            for which in ("ground_truth", "source"):
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto((CASE / f"{which}.html").as_uri(), wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(1500)  # source 有 0.5s 过渡，等它稳定
                page.mouse.move(0, 0)
                page.wait_for_timeout(800)
                shoot(page, f"{which}_{name}_default.png")
                key = f"{which}_{name}"
                report[key] = {"default": page.evaluate(MEASURE)}
                n = page.locator(".articles__link").count()
                for i in range(n):
                    link = page.locator(".articles__link").nth(i)
                    link.scroll_into_view_if_needed()
                    link.hover()
                    if which == "ground_truth":
                        page.wait_for_timeout(50)  # GT 无过渡，应立即到终态
                        report[key][f"hover_{i+1}_immediate"] = page.evaluate(MEASURE)["cards"][i]
                    page.wait_for_timeout(1200)
                    report[key][f"hover_{i+1}"] = page.evaluate(MEASURE)
                    shoot(page, f"{which}_{name}_hover{i+1}.png", full=False)
                    page.mouse.move(0, 0)
                    page.wait_for_timeout(1200)
                page.close()
        browser.close()
    (HERE / "gt_selfcheck.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
