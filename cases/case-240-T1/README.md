# CSS-Art Teenage Engineering OP-1 Portable Synthesizer

来源：<https://codepen.io/shunyadezain/pen/QWyVwep>（作者 shunyadezain，CodePen 公开作品，默认 MIT 许可）

当前阶段见 [registry.csv](../registry.csv)（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C022；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：合成器面板、旋钮浮雕

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |
| `ground_truth.html` | 准静态参考页（见下文“GT 相对来源的改动”） |
| `review_20261124/` | GT 自检：来源差异、静态检查与渲染核对记录、本地测量脚本 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只删 CodePen 样板，结构、样式数值、文案、字体引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 头部样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本 | 与作品和评分无关（用户同意删除） |
| `<body translate="no">` 改为 `<body>`；删除脚本末尾的 `//# sourceURL=pen.js` | CodePen 预览页加的内容，与评分无关 |

- **静止状态：** 来源没有动画、过渡和悬停样式，脚本里只有两行作者注释（保留），GT 就是来源的唯一画面，不需要选静止帧。
- **保留的交互：** 无（来源没有）。
- **外部资源：** 只有 CSS 里 `@import` 的 Google Fonts：Catamaran 200、Jura 300、Tulpen One。
- **窄屏：** 机身布局宽 550px，再整体 `scale(1.5)` 显示为约 825×297px，来源没有窄屏适配，窄视口下左右两端会溢出；GT 保持原样，input 只面向桌面宽屏。
- **档位复核：** GT 没有任何动态和交互，按难度模型 v2.1 为 T1，与入库暂定一致，不改名。
