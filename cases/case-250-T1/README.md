# Responsive infographic banners with CSS variables

来源：<https://codepen.io/thebabydino/pen/NLWdwz>（作者 thebabydino，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C039；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：圆片信息图、编号叠盖

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 由 `source.html` 复制后只删 CodePen 样板，样式、结构、文案一律不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical，`<body translate="no">` 改为 `<body>` | CodePen 样板，与作品和评分无关（用户同意删除）。来源没有脚本 |

- **静止状态：** 来源本身没有动画、过渡和交互，默认画面就是静止画面，无须另选。
- **保留不动：** 三个响应式断点（625、480、225px）；标题前的 emoji 图标（经灰度滤镜显示为灰色，具体字形取决于系统 emoji 字体）；字体栈 `trebuchet ms, verdana, sans-serif`（系统字体，不加载外部字体）。
- **档位复核：** GT 无动态、无交互，仍为 **T1**，目录名不变。
- **自检：** 见 [review_20261124/static_check.md](review_20261124/static_check.md)。已用云端浏览器经 raw.githack.com 在 1280、600、500 宽下核对，480px 以下用自检辅助页 `frame_view.html`（把 GT 放进 450px 宽的 iframe，不属于 GT）核对，渲染与来源一致，GT 不需要修改。来源在 600、500 宽时 02、04 横幅的文字左端被切，GT 照来源保留，见 `input_problem.md`。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 和渲染截图写出，写了宽屏、中等宽度、窄屏三套版式，等用户审核 GT 与 input。取舍和待定问题见 [input_problem.md](input_problem.md)。
