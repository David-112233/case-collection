# Responsive infographic/ CSS variables, grid layout

来源：<https://codepen.io/thebabydino/pen/eQvWLB>（作者 thebabydino，CodePen 公开作品，默认 MIT 许可）

当前阶段：`admitted`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C040；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：彩色折纸条、交替折角

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 由 `source.html` 复制后只删 CodePen 样板，样式、结构、文案、字体与图片引用一律不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical，`<body translate="no">` 改为 `<body>` | CodePen 样板，与作品和评分无关（用户同意删除）。来源没有脚本 |

- **静止状态：** 来源本身没有动画、过渡和交互，默认画面就是静止画面，无须另选。
- **保留不动：** Google Fonts 的 KoHo 字体样式表；页面背景图（s3-us-west-2.amazonaws.com 上的 `kreator_rockharz_july_2018.jpg`，上面盖一层 80% 白）；两个断点（39em、15em）；卡片里的水果 emoji；内联样式里未被使用的 `--idx` 变量；选择器 `article :after`（带空格，作用于卡片内所有子元素的 `::after`，来源如此）。
- **档位复核：** GT 无动态、无交互，仍为 **T1**，目录名不变。
- **自检：** 见 [review_20261124/](review_20261124/)。渲染核对结论写在 `static_check.md`。
