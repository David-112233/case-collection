# CSS '00s 3D iPod Nano [CHALLENGES]

来源：<https://codepen.io/RaduBratan/pen/mdPrWmo>（作者 RaduBratan，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C002；档位：T3（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：iPod Nano、凹屏与滚轮

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只做删除，结构、样式数值、文案、外部资源引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性、`//# sourceURL=pen.js` | 与作品和评分无关（用户同意删除） |
| 删除 `body.animation .case-scene` 的 `hover-ipod`、`.screen-scene` 的 `hover-screen`、`.wheel-scene` 的 `hover-wheel`、`.light-scene` 的 `light` 四个无限往复动画及其 `@keyframes` | 准静态要求去掉持续动画 |
| 删除 `body`、`body.animation`、`.shadow-scene`、`.shadow-shape` 上的 `transition` | 点击切换改为直接到终态（用户同意） |

- **静止状态：** 四个动画都固定在 `from` 帧。`from` 帧的数值与各元素的基础样式完全相同，删掉动画后不需要另写任何数值，最符合“尽量尊重源码”；画面是机身、屏幕、滚轮贴合在一起的完整机身，而 `to` 帧是机身上浮、屏幕和滚轮与机身拉开的分离状态，只是往复动画的一端。
- **保留的交互：** 点击滚轮切换发光模式（jQuery `toggleClass("animation")`），再点一次回到默认；切换瞬时完成，状态保持到下次点击。
- **保留的外部资源：** prefixfree、jQuery 3.5.1、Font Awesome 5.2.0 免费版 all.js、Font Awesome Pro 5.2.0 CSS。滚轮上的四个图标是脚本注册的自定义 SVG，由 all.js 渲染，按源码不依赖 Pro CSS；Pro CSS 很可能因授权加载失败，但不影响画面。**两点都未在浏览器里核实**，见 [review_20261124/static_check.md](review_20261124/static_check.md)。
- **档位复核：** GT 仍有“点击滚轮进入并保持发光模式”这一可保持的状态切换，按难度模型 v2.1 为 T3，与入库暂定一致，不改名。
- **自检：** 静态检查之外，已用云端浏览器经 raw.githack.com 在 1280 与 500 宽、点击前后核对渲染，图标和点击切换都正常。发现发光模式下屏幕和滚轮被半透明的机身正面盖住，来源本身就有，GT 未改，待用户定，见 [review_20261124/static_check.md](review_20261124/static_check.md)。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 写出，等用户审核 GT 与 input。外观描述中按源码推断、尚未经渲染核对的部分，以及写与不写的取舍，见 [input_problem.md](input_problem.md)。
