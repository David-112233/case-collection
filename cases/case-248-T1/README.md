# CSS folded poster effect

来源：<https://codepen.io/lynnandtonic/pen/PoZpjOr>（作者 lynnandtonic，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C037；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：折痕海报、纸面光影

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 由 `source.html` 复制后只删 CodePen 样板，样式、结构、图片、文案一律不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本，`<body translate="no">` 改为 `<body>`，删除脚本块里的 `//# sourceURL=pen.js` | CodePen 样板，与作品和评分无关（用户同意删除） |

- **保留不动：** CodePen 重置样式表 `reset-2.0.min.css`（作者在 pen 设置里选用的重置，影响默认边距等版式，属于作品的一部分）；脚本块里只剩作者署名注释，没有可执行代码；三张海报图片（assets.codepen.io）。
- **静止状态：** 来源本身没有动画、过渡和交互，默认画面就是静止画面，无须另选。
- **档位复核：** GT 无动态、无交互，仍为 **T1**，目录名不变。
- **自检：** 见 [review_20261124/static_check.md](review_20261124/static_check.md)。已用云端浏览器经 raw.githack.com 在 1280、500 宽下核对：三张图片和重置样式表都加载，渲染正常，GT 不需要修改；500 宽时内容区不缩、出现横向滚动条，来源如此。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 和渲染截图写出，等用户审核 GT 与 input。取舍和待定问题见 [input_problem.md](input_problem.md)。
