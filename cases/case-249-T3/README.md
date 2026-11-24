# 3D Walkman - Pure CSS Art

来源：<https://codepen.io/ricardoolivaalonso/pen/RwBZMGB>（作者 ricardoolivaalonso，CodePen 公开作品，默认 MIT 许可）

当前阶段：`admitted`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C038；档位：T3（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：开盖随身听、内腔层次

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，结构、各部件的样式数值、文案、id 与 class、音频引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性、`//# sourceURL=pen.js` | 与作品和评分无关（用户同意删除） |
| 删除拖动旋转：脚本里的 `h`、`unit`、`mouseDown`、`mouseUp`、`moveFunc` 及 `#h` 的 `mousedown`、`body` 的 `mouseup` 监听；删除 `body` 的 `cursor: grab` | 按住拖动随鼠标改变视角属于复杂交互，固定在来源的初始视角（`.main` 样式里的 `perspective(700vmin) rotateX(66deg) rotateZ(40deg) translateZ(-28vmin)`，与拖动公式在画面中心时的结果相同）；没有拖动后抓手光标会误导 |
| 删除播放键侧面格栅边框的 `animation: btn` 及 `@keyframes btn` | 边框由灰蓝到黄色每秒循环一次的提示闪烁，属于持续动画。静止状态取基础样式的灰蓝色 `#9ebec7`（关键帧起点，不用另写数值）；黄色只是循环的一端 |
| 删除 `.cr` 规则及 `@keyframes circle` | 播放时第二个耳机插孔中心的条纹圆片每 4 秒转一圈，属于持续动画。删去后圆片停在基础样式（关键帧终点除旋转外与基础样式相同），脚本对 `.cr` 类的切换保留，不再产生效果 |
| 7 条声波条的 `animation`（`wave`、`wave-2`、`wave-3`）改为固定高度，删除三组 `@keyframes` | 播放时地面上的声波条持续起伏，属于持续动画。静止状态取页面载入后 1300ms 那一帧（按关键帧和 ease-in 计算）：7 条全部可见、中间最高，像均衡器，最能代表“正在播放”；从左到右高度为 8.75、7.94、7.74、11.375、9.41、7.94、8.75vmin。其他时刻两端两条常为 0 高度，看不出是一组声波 |
| 脚本中 `setTimeout(() => waveElement.classList.add('is-wave-playing'), 1100)` 改为点击时立即添加 | 点击后的一次性延时，按“一次性过渡去掉时长、直接到终态”处理 |
| 删除仓门 `.c`、`.is-c-close` 的 300ms 过渡和播放键 `.button5`、`.is-button-pressed` 的 100ms 过渡 | 同上，点击后直接到终态 |

- **静止状态：** 默认态即来源的初始画面：仓门以底边为轴向外打开约 19°，露出深色内腔，播放键在原位。播放态见上表，声波条固定在 1300ms 那一帧。
- **保留的交互：** 点击机身侧面的播放键：开始播放音频，播放键被按下（向机身内移动），仓门合上，地面上出现 7 条声波条。播放期间再点播放键无反应（来源在播放时移除了点击监听）；音频播放完毕后自动恢复默认态，可再次点击播放。切换都是瞬时的。
- **保留的外部资源：** 只有音频（rawcdn.githack.com 上作者仓库的 `audio.mp3`）。没有外部字体和图片，文字用浏览器默认无衬线字体。
- **疑点（默认照来源，未改）：** 播放态何时结束取决于音频长度；音频加载失败时 `play()` 被拒，`ended` 不会触发，页面会一直停在播放态。见 `input_problem.md`。
- **档位复核：** GT 有“点击后进入并保持播放态”（按键、仓门、声波条保持到音频结束），按难度模型 v2.1 为 **T3**，与暂定一致，目录名不变。
- **自检：** 见 [review_20261124/](review_20261124/)。`state_view.html` 是自检辅助页：在同源 iframe 里打开 GT 并自动点击指定元素，供只能截图的云端浏览器查看点击后的状态，不属于 GT。
