# CSS3D Room furniture challenge...

来源：<https://codepen.io/zenete/pen/BaMbmqW>（作者 zenete，CodePen 公开作品，默认 MIT 许可）

当前阶段见 [registry.csv](../registry.csv)（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C028；档位：T2（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：房间吊顶、扇叶遮叠

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |
| `ground_truth.html` | 准静态参考页（见下文“GT 相对来源的改动”） |
| `review_20261124/` | GT 自检：来源差异、静态检查与渲染核对记录、本地测量脚本 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，结构、样式数值、外部资源引用、作者注释都不动，只删 CodePen 样板和动画。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 头部样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本；`<body translate="no">` 改为 `<body>`；删除脚本末尾的 `//# sourceURL=pen.js` | 与作品和评分无关（用户同意删除） |
| 删除吊扇转子 `light > u:nth-of-type(5)` 的 `animation: rotate 3s linear infinite` 及 `@keyframes rotate` | 吊扇持续旋转，准静态要求去掉 |
| 删除三片扇叶的 `animation: rlight …`（三个相位）及 `@keyframes rlight` | 扇叶随转动明暗交替的持续动画 |
| 删除扇叶上的 `transition: all 0.2s …` | 没有触发它的状态变化，只是过渡残留 |
| 删除两个 `@media (max-width: 400px)` 里的 `animation-play-state: paused` | 动画删掉后这两句不再起作用；同一媒体查询里作者写的窄屏静止姿态（转子 `rotate(180deg)`、扇叶 `rotateY(-45deg)`）保留不动 |

- **静止状态：** 吊扇固定在动画起点，即各元素的基础样式：转子 `rotate(0)`，三片扇叶按源码的 20°、120°、240° 均匀分布，亮度为原色（`rlight` 只在 50% 帧把亮度降到一半，起点和终点都是原色）。删掉动画后不用另写任何数值，最尊重源码。
- **保留的交互：** 无（来源没有悬停、点击等交互）。
- **外部资源：** 作者引用的 `codepen.io/zenete/pen/eYLjgaq.css` 与 `.js`（作者另一个作品的样式和脚本）保留；能否加载、起什么作用见渲染核对。
- **档位复核：** 去掉吊扇动画后，GT 没有任何动态和交互，按难度模型 v2.1 为 T1，由暂定 T2 改为 T1（`registry.py retier`）。
- **作品价值：** 来源的唯一动态就是吊扇旋转，它是装饰性的；作品的空间价值在房间透视、窗洞与吊顶凹槽、吊扇多层圆盘与扇叶的遮叠，静止后都还在，所以照常改造，没有停下。
