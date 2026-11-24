# CSS Lighthouse Scene

来源：<https://codepen.io/agathaco/pen/JaGQPr>（作者 agathaco，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C048；档位：T1（入库时按来源源码暂定为 T2，GT 完成后复核改为 T1，见下文“档位复核”）。
- 特色：夜景灯塔、光束与远山

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 由 `source.html` 复制后只做以下改动，场景结构、颜色、尺寸、位置都不动（完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)）：

| 改动 | 原因 |
|---|---|
| 删除 `apple-touch-icon`、`apple-mobile-web-app-title`、`icon`、`mask-icon` 四个 CodePen 图标与元信息，删除 `<link rel="canonical">`、`stopExecutionOnTimeout` 脚本和 `//# sourceURL=pen.js`，`<body translate="no">` 改为 `<body>` | CodePen 页面样板，与评分无关（用户同意删除）。脚本块里作者的教程链接注释保留 |
| 删除星星的 `twinkle`（闪烁）、水波纹的 `wave`（左右晃动）两组循环动画，以及 90 条只供它们错开节奏的 `animation-delay` | 持续循环动画。删除后停在关键帧的起止状态，即样式本身的状态：星星完全不透明，波纹在原位 |
| 删除光束的 `lightRotate`（20 秒来回扫动）和灯笼光晕的 `lightGlow`（20 秒明灭） | 持续循环动画。删除后停在样式本身的状态，也就是这两个动画在每个 20 秒周期开头（0%）的状态：光束容器 `rotateY(0)`，光束向右斜伸、远端渐隐；光晕 `.glow` 透明不可见（灯笼本身的常亮光晕来自 `.middle::before`，不受影响） |
| 删除帆船的 `boat`（100 秒从右向左驶过）和船影的 `boatShadow`，改为固定的 `transform`：帆船 `translateX(47.5vw) scale(0.8)`，船影 `skewX(-37deg) translateX(-29px)` | 持续循环动画。帆船在动画开头位于画面右侧之外（`120vw`），若只删动画，帆船会停在画面最左端、按原尺寸显示，这是来源里从未出现的样子；所以按来源关键帧线性插值，取第 40 秒的值：帆船驶到画面中部的海面（47.5vw），船影随之倾斜。第 40 秒恰好是光束、光晕的第三个周期开头，与上一条的状态属于同一时刻 |
| 删除不再使用的六组 `@keyframes` | 动画已删除 |

- **静止状态：** 选来源第 40 秒这一时刻：光束处于周期开头的位置，向右斜伸，覆盖月亮附近的天空；灯笼常亮；帆船在海面中部；星星和波纹为样式本身的状态。理由：这一时刻所有主要元素（灯塔、光束、远山、月亮、帆船、星星、波纹）都在画面内，光束、光晕两个动画在这一刻恰好回到样式本身的值，改动最少；帆船只能另取一个在画面内的时刻。
- **作品价值提醒：** 来源的看点之一是灯塔光束来回扫动、帆船驶过的持续动画，GT 去掉后只剩静态夜景（灯塔、光束、远山交叠、海面、月亮、帆船的前后层次）。按“能做的照做”处理，是否仍收录请用户定，见 [input_problem.md](input_problem.md)。
- **交互：** 来源没有任何交互，GT 也没有。
- **档位复核：** GT 无任何动态、没有交互，按难度模型 v2.1 为 **T1**，已用 `registry.py retier` 由暂定 T2 改为 T1（目录名随之改为 `case-254-T1`），`classification.json` 的 `tier_status`、`tier_basis`、`tier_note` 已手动同步。
- **渲染核对：** 云端浏览器 1280、500 宽截图，画面静止、无渲染问题；500 宽时灯塔按固定像素占去大半画面（来源如此，未改）。详见 [review_20261124/static_check.md](review_20261124/static_check.md)，截图测量脚本为 [review_20261124/shot_gt.py](review_20261124/shot_gt.py)。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 写出，等用户审核 GT 与 input。取舍与待定问题（含作品价值主要在动画、是否仍收录）见 [input_problem.md](input_problem.md)。
