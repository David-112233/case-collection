# CSS infographic

来源：<https://codepen.io/meylon/pen/qByaYVp>（作者 meylon，CodePen 公开作品，默认 MIT 许可）

当前阶段见 [registry.csv](../registry.csv)（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C026；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：圆环凹面、错落连线

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |
| `ground_truth.html` | 准静态参考页（见下文“GT 相对来源的改动”） |
| `review_20261124/` | GT 自检：来源差异、静态检查与渲染核对记录、本地测量脚本 |
| `input.json` | 由 GT 写出的题目草稿，等用户审核 |
| `input_problem.md` | input 的核对结果、取舍与待定问题 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只删 CodePen 样板，结构、样式数值、文案都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 头部样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical | 与作品和评分无关（用户同意删除） |
| `<body translate="no">` 改为 `<body>` | CodePen 预览页加的属性，与评分无关 |

- **静止状态：** 来源没有脚本、动画、过渡和悬停样式，GT 就是来源的唯一画面，不需要选静止帧。
- **保留的交互：** 无（来源没有）。
- **外部资源：** 无。源码里的图标写成 `<i class="far fa-building">1</i>`，但作品没有引用 Font Awesome（原始捕获里也没有），所以圆圈中央显示的是斜体数字 1 至 6，不是大楼图标。GT 照来源保留，不补引图标库；input 按实际显示的数字写。
- **窄屏：** 来源在 992px 以下改为一行横排、容器固定 1300px 宽并可横向滚动；GT 保持原样，input 只面向桌面宽屏。
- **档位复核：** GT 没有任何动态和交互，按难度模型 v2.1 为 T1，与入库暂定一致，不改名。
- **自检：** 做了静态检查；用云端浏览器经 raw.githack 在 1280 与 500 宽视口截图核对，画面与源码推算一致，GT 不改。精确测量的 Playwright 脚本 `review_20261124/gt_check.py` 已备好，待本地运行（375 视口也待本地）。见 [review_20261124/static_check.md](review_20261124/static_check.md)。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 写出，已对照截图核对，等用户审核 GT 与 input。写与不写的取舍和待定问题见 [input_problem.md](input_problem.md)。
