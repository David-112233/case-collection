# Pure CSS Cassette Tape and Cassette Box with A/B Sides Label

来源：<https://codepen.io/MadeByArne/pen/bGWwRoX>（作者 MadeByArne，CodePen 公开作品，默认 MIT 许可）

当前阶段：`gt_ready`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C016；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：磁带窗口、带芯叠层

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只删 CodePen 样板，结构、样式、文案、字体引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`<body translate="no">` 的属性 | 与作品和评分无关（用户同意删除） |

- **来源本身就是静态的：** 没有动画、过渡、悬停或脚本，所以不需要选静止状态。HTML 末尾作者多写的两个 `</div>` 浏览器会忽略，保留原样。
- **保留的外部资源：** Google Fonts 的 Gochi Hand（手写体）。
- **档位复核：** 无动态、无交互，按难度模型 v2.1 为 T1，与入库暂定一致，不改名。
- **自检：** 见 [review_20261124/static_check.md](review_20261124/static_check.md)。
