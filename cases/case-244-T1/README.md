# Interlocking Olymipic Rings

来源：<https://codepen.io/kevinleclair1/pen/XJgQrr>（作者 kevinleclair1，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C032；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：交织五环、前后交替

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

- **无动画、无交互。** 来源没有脚本、关键帧、过渡或悬停样式，GT 不需要固定静止状态。
- **嵌套的 `<html>`、`<head>`、`<body>`**：作者在 HTML 面板里写了整页骨架，被 CodePen 套进 `<body>`。浏览器解析时忽略多余的骨架标签，内部的 `<title>CSS z-index</title>` 落在 body 里且不显示，页面标题仍是外层的 “Interlocking Olymipic Rings”。保持原样。
- **套扣的做法**：五个整环之外，另有五个同尺寸、只有一条边框着色的“半透明环”（`overlap1`–`overlap5`）叠在对应整环上，用 `z-index` 把该环的一段四分之一弧提到相邻环之上，从而在每对相交环的两个交点上形成一上一下。
- **固定像素尺寸**：外框宽 735px、上边距 100px，不随视口缩放；视口窄于约 735px 时页面横向溢出（来源相同）。GT 未修。
- **外部资源**：GT 不加载任何外部资源。

## GT 自检

见 [review_20261124/static_check.md](review_20261124/static_check.md)。经 raw.githack.com 在云端浏览器打开 GT，在 1280 和 500 宽截图，并放大核对了八个交点，截图未入库；本地可运行 `review_20261124/shot_gt.py` 重新得到截图和测量。

## 档位复核

GT 无任何动态：无动画、无过渡、无悬停或点击效果。按难度模型 v2.1 仍为 **T1**，与目录名一致，不需要 retier。

## input

[input.json](input.json) 由 GT 写出，问题与取舍见 [input_problem.md](input_problem.md)。外观已按截图核对。阶段 `input_draft`：等用户审核 GT 与 input，规则草稿和 `generation_prompt.txt` 尚未写。

注意：入库评语认为本案复杂度明显低于参考案例，是否保留待用户定（见 input_problem.md 第 3 节）。
