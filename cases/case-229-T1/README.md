# CasioPT-1.css

来源：<https://codepen.io/fossheim/pen/VweaNYW>（作者 fossheim，CodePen 公开作品，默认 MIT 许可）

当前阶段：`admitted`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C003；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：卡西欧键盘、黑白键叠压

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |
| `ground_truth.html` | 准静态参考页（见下文“GT 相对来源的改动”） |
| `review_20261124/` | GT 自检：静态检查、来源差异、本地渲染脚本 |
| `input.json` | 由 GT 写出的题目草稿，等用户审核 |
| `input_problem.md` | input 的推断依据、取舍与待定问题 |

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只删 CodePen 样板，结构、样式数值、文案、字体引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 头部样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical | 与作品和评分无关（用户同意删除） |
| `<body translate="no">` 改为 `<body>` | CodePen 预览页加的属性，与评分无关 |

- **静止状态：** 来源本身没有动画、过渡、脚本和交互，GT 就是来源的唯一画面，不需要选静止帧。作者的注释（教程链接、赞助链接）保留。
- **保留的交互：** 无（来源没有）。
- **外部资源：** 只有作者在 HTML 里引用的 Google Fonts Montserrat 800（用于 “CASIO PT-1” 标志）。从本环境请求字体 CSS 与拉丁子集 woff2 均返回 200；浏览器内是否实际应用未核实。
- **窄屏：** 机身固定 960px 宽，来源没有窄屏适配，375 宽视口下会横向溢出；GT 保持原样，input 只面向桌面宽屏。
- **档位复核：** GT 没有任何动态，按难度模型 v2.1 为 T1，与入库暂定一致，不改名。
- **自检：** 做了静态检查和按 CSS 推算的几何；之后用云端浏览器经 raw.githack 在 1280 与 500 宽视口截图核对，画面无渲染问题，GT 不改。精确测量的 Playwright 脚本已备好，待本地运行（375 视口也待本地）。见 [review_20261124/static_check.md](review_20261124/static_check.md)。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 写出，等用户审核 GT 与 input。外观描述已对照截图核对并修正 3 处，核对结果和写与不写的取舍见 [input_problem.md](input_problem.md)。
