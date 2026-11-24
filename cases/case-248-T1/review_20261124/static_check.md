# case-248 GT 自检记录（2026-11-24）

## 不依赖浏览器的核验

- `ground_truth.html` 与 `source.html` 的差异见 [source_to_gt.diff](source_to_gt.diff)：只删 CodePen 样板，样式和结构没有任何新增或改写。
- GT 中没有 `animation`、`transition`、`@keyframes`，脚本块里只有作者署名注释。
- 云端 shell 被代理拦截，不能直接下载外部资源，外部资源改在浏览器里核对（见下）。

## 云端浏览器渲染核对

**方法：** 用项目的云端浏览器打开 `https://raw.githack.com/David-112233/case-collection/aebc1a3/cases/case-248-T1/ground_truth.html`（提交 aebc1a3 即 gt_ready 的 GT；直接进入页面，没有提示页），视口 1280×900 和 500×900，截整页和局部放大图查看。工具最小宽度 500，375 宽没法在云端核对。截图只在核对时查看，没有入库。另在同一浏览器打开重置样式表地址，确认能取到内容。

**结论：GT 渲染正常，外部资源全部加载，没有需要修改的问题。**

| 核对项 | 结果 |
|---|---|
| 外部资源 | 三张海报图片（assets.codepen.io）都显示；`reset-2.0.min.css` 可访问，内容为 Eric Meyer 式重置（各元素边距清零、`body` 行高 1 等） |
| 1280 版式 | 浅鲑鱼橙背景；三行两列，内容区约 650px 宽、水平居中；左列原图约 250px 宽、无边框，右列折叠海报约 300px 宽；同行两张竖直居中对齐 |
| 折叠海报 | 白边（经滤镜后呈浅灰白）；颜色比原图明显更淡更灰；竖向折痕在正中，横向折痕在高度三分之一、三分之二处，都贯穿白边，表现为细亮线加细暗线；折面上有轻微明暗渐变；四周柔和投影；纸下方有一条窄阴影带，上深下浅，两端略内收 |
| 500 宽 | 内容区不缩，右列折叠海报被截在视口外，出现横向滚动条（来源如此，不是响应式） |
| 动态 | 无动画、无交互 |

## 本地补跑

`gt_selfcheck.py` 在 1280×900 与 375×812 下截整页，并测量原图与折叠海报的位置尺寸、滤镜、伪元素尺寸、图片与重置样式表是否加载、运行中的动画数、页面是否横向溢出：

```
pip install -r requirements.txt
python -m playwright install chromium
python cases/case-248-T1/review_20261124/gt_selfcheck.py
```
