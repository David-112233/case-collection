# CSS 3D Studio Room (Mine! 😅)

来源：<https://codepen.io/jh3y/pen/XWdQBRx>（作者 jh3y，CodePen 公开作品，默认 MIT 许可）

当前阶段：`gt_ready`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C036；档位：T3（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：立体工作室、室内遮挡

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，房间里所有物体的结构、三维数值、配色和外部图片都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性 | 与作品和评分无关 |
| 删除自动播放、循环的背景音乐 `<audio>`（assets.codepen.io 的 mp3）、右下角的“声音开关”按钮及其 `--index` 规则，以及只为切换声音而写的整段脚本 | 准静态要求去掉自动播放的媒体；声音与画面和评分无关，脚本没有其他作用 |
| 删除“椅子旋转”按钮（`#spin` 及其标签、`#spin:checked` 规则、`--index` 规则）和 `.chair__top` 上的无限旋转动画及 `@keyframes spin` | 打开后椅子持续自转，是循环动画，不是可静止的状态切换 |
| 剩下的两个按钮重新编号：`[for='dark']` 的 `--index` 1 → 0，`[for='zoom']` 3 → 1 | 删掉两个按钮后右下角的按钮列不留空位，“灯光”在最下，“缩放”在其上，相对顺序与来源相同 |
| 夜间模式下台灯方块、墙上光斑、书架光斑的 `fade` 循环变色动画（10 秒一轮，粉 → 蓝 → 紫 → 绿）改为固定 `background: var(--fade-one)`，并删除 `@keyframes fade` | 准静态要求去掉循环动画 |
| 删除两块显示器屏幕里的 `<iframe>`（分别嵌入 css-tricks.com 和 jhey.dev 两个外站首页）；`.monitor iframe` 样式保留 | 嵌入的是实时外站网页：一个拒绝被嵌入，显示浏览器的错误页；另一个显示作者个人站，内容随时间变化（含实时天气、正在播放的歌曲等），不是准静态，也无法写进题目。删除后屏幕显示显示器自身的灰色面（白天 #808080，夜间 #404040）。**待用户确认**，见 input_problem.md |
| `--transition: 0.2s` 改为 `0s` | 来源所有过渡（缩放、开关灯、百叶窗翻转、海报阴影、背景色）都用这个变量，改为 0 后点击直接到终态，只改一处数值 |

- **静止状态：** 循环变色固定在 0%/100% 帧的粉色 `#f7baba`（关键帧的起止帧，变量里排第一，也是开灯瞬间的颜色）；椅子固定在不转时的朝向，即来源未开旋转时的样子。
- **保留的交互：** 右下角两个圆形图标按钮。“灯光”：点击进入夜间模式并保持（墙面、地板、家具变暗，背景变深蓝，百叶窗合上，台灯、墙面和书架亮起粉色光），再点回到白天。“缩放”：点击后镜头拉近到正对书桌的视角并隐藏椅子和另一个按钮，再点回到默认视角。两者都瞬时切换。
- **保留但无作用的代码：** `audio { display: none; }` 和 `.dg.ac` 两条样式（元素已删除或来源本就没有），不影响画面，按最小修改不删。
- **保留的外部资源：** normalize.css 5.0.0；pexels 的三张照片（窗外景色、桌面木纹、地毯）；assets.codepen.io 的盆栽 PNG 和椅背头像 PNG。
