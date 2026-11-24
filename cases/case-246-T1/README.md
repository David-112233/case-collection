# Simple CSS/SCSS 3D Bookshelf

来源：<https://codepen.io/ehckk/pen/WNzGYKy>（作者 ehckk，CodePen 公开作品，默认 MIT 许可）

当前阶段：`gt_ready`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C034；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：彩虹书架、书脊深度

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 由 `source.html` 复制，只删了与评分无关的 CodePen 样板，`<style>` 和作品的 HTML 逐字未动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 `apple-touch-icon`、`icon`、`mask-icon` 三个图标链接和 `apple-mobile-web-app-title` 元信息 | CodePen 页面样板，与作品和评分无关，且是外部请求 |
| 删除 `<link rel="canonical">` | CodePen 样板；来源链接已记在本 README 和 metadata.json |
| `<body translate="no">` 改为 `<body>` | CodePen 给页面加的属性，与渲染无关 |

未改但需要知道的地方：

- **无动画、无交互、无脚本。** 来源没有关键帧、过渡、悬停或任何脚本，GT 不需要固定静止状态。
- **保留的外部资源：** 作者在 CodePen 设置里选的 normalize.css 5.0.0（public.codepenassets.com）。作品自己的 `*` 规则已把内外边距清零，按源码推断这份样式对画面影响很小。
- **规模：** 一个书架（五层隔板、两侧外板、背板、底板、四条腿）、120 本书和一面墙，全部用 CSS 3D 盒子拼成，书的颜色和高度由 SCSS 编译出的逐本规则决定。
