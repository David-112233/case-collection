# MC Escher Cube 23150 with CSS only

来源：<https://codepen.io/HunorMarton/pen/BazeOpE>（作者 HunorMarton，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C033；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：埃舍尔方块、桥面穿插

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只做删除，立方体图案的结构、选择器、变换和颜色数值都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性、`//# sourceURL=pen.js` | 与作品和评分无关 |
| 删除 `.container` 上的 `zoom-out` 动画（四行 `animation-*`）及其 `@keyframes` | 准静态要求去掉自动播放的动画。它是载入时整幅图案从 2 倍缩到 1 倍的一次性 3 秒入场动画 |
| 删除右下角的 YouTube 徽标链接 `#youtube` 和悬停时弹出的 `#youtube-card` 文案卡片，以及它们的全部样式（含 0.5s 的悬停放大过渡） | 作者为自己的教程视频做的推广入口，链接到站外视频，与作品画面和评分无关。**这是本案唯一的悬停交互，删除后档位从 T2 变为 T1，见下面的档位复核，待用户确认** |

- **静止状态：** 入场动画固定在终态 `scale(1)`。终态与 `.container` 的基础样式（无变换）相同，删掉动画后不需要另写数值；起始的 2 倍放大只是入场过程的一端，图案被裁掉大半，不代表作品。
- **保留：** 作者在脚本面板里的注释（只有注释，没有代码），不影响渲染。
- **外部资源：** GT 不加载任何外部资源。

## 档位复核

GT 无任何动态：入场动画已去掉，唯一的悬停交互（YouTube 推广徽标放大并弹出卡片）随徽标一起删除。按难度模型 v2.1 由暂定 **T2 改为 T1**，已用 `registry.py retier` 改名并同步 classification.json。若用户决定保留徽标，应改回 T2。

## GT 自检

见 [review_20261124/static_check.md](review_20261124/static_check.md)。经 raw.githack.com 在云端浏览器打开 GT，在 1280×800、1280×992、500×800 截图并放大核对，截图未入库；本地可运行 `review_20261124/shot_gt.py` 重新得到截图和测量。

## input

[input.json](input.json) 由 GT 写出，问题与取舍见 [input_problem.md](input_problem.md)。外观已按截图核对。阶段 `input_draft`：等用户审核 GT 与 input，规则草稿和 `generation_prompt.txt` 尚未写。

注意：这幅图案由十几种不同的格子按 4 排 × 6 格的单元重复组成，文字只能写到花样类别一层，是否可评测待用户定（见 input_problem.md 第 2 节）。
