# CSS Record Player

来源：<https://codepen.io/dustindwayne/pen/bGyYoar>（作者 dustindwayne，CodePen 公开作品，默认 MIT 许可）

当前阶段：`gt_ready`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C014；档位：T3（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：唱片机、正面浮雕

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，结构、文案、样式数值、外部资源引用都不动。来源的 CSS 由 SCSS 循环编译，整份样式表重复了 9 遍（每遍只有一个音量刻度的样式不同），GT 保留这一结构，下面的删除在 9 份里同样执行。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性、`//# sourceURL=pen.js`；同时删除 CodePen 插进作者循环里的 `window.CP.shouldStopExecution(0)`、`window.CP.exitedLoop(0)` 两处调用 | 与作品和评分无关（用户同意删除）；两处调用依赖被删的样板脚本，留着会在播放时报错 |
| 删除 `.clickme:before`（“CLICK ME”上方的箭头）上下跳动的 `animation: point` | 持续动画 |
| 点击电源键开始播放时，脚本不再给唱片加 `spin 5s linear infinite`（持续旋转），也不再给唱臂加 `movebar 100s`（2% 时到 17°、之后 100 秒内缓慢扫到 34° 再回到 17°的循环），只保留原有的 `tb.style.transform = 'rotate(17deg)'` | 持续动画；唱臂直接停在 17°，即 `movebar` 2% 帧、也是 100% 帧的值 |
| 再次点击停止时，脚本把唱臂的 `mb1 3s`（3 秒内从 17° 转回 0°）改为直接设 `rotate(0deg)`，并删掉对唱片动画的暂停 | 点击触发的一次性过渡去掉时长，直接到终态（用户同意）；唱片已不转，暂停无对象 |
| 删除 `@keyframes spin`、`movebar`、`mb1`、`point` 及其 `-moz-`、`-webkit-`、`-o-` 前缀版本 | 上面几处删除后不再有引用 |
| 删除 `.clickme` 上的 `transition: all 0.7s`（提示淡出淡入）和 `.record` 上的 `transition: all 1s` | 点击后直接到终态；`.record` 的过渡只服务于旋转 |

- **静止状态：** 唱片停在初始角度（标签文字的位置与来源打开时相同）。默认状态唱臂在 0°，停在唱片右侧外；播放状态唱臂停在 17°，唱针落在唱片外圈上。17° 是来源点击后立刻写入的值，也是 `movebar` 动画第 2% 帧和结束帧的值，最能代表“正在播放”。“CLICK ME”箭头停在基础位置（`top: -30px`，即 `point` 动画的起点）。
- **保留的交互：** ① 点击电源键开始播放并保持：唱臂转到唱片上、电源指示灯由半透明白变为红色、下方“CLICK ME”提示消失、用 Tone.js 循环播放一段合成的摇滚乐；再点一次唱臂回到原位、指示灯恢复、提示重新出现、音乐停止。② 点击音量旋钮周围 1 至 9 的刻度，旋钮上的白色指示线转到对应刻度（只改指示线，来源本来就不改变音量）。两者都瞬时完成，状态保持到下次点击。
- **保留的外部资源：** Google Fonts 的 Bungee、Teko，normalize.css，Tone.js 15.1.2（cdnjs）。
- **作品价值说明：** 来源播放时唱片持续旋转、唱臂缓慢扫过，这部分动画按准静态要求去掉了；保留的是唱机正面的浮雕细节和点击开关的状态切换。
- **档位复核：** GT 有“点击电源键进入并保持播放状态，同时改变唱臂、指示灯和提示文字”的点击保持状态，按难度模型 v2.1 为 T3，与入库暂定一致，不改名。
- **自检：** 见 [review_20261124/static_check.md](review_20261124/static_check.md)。
