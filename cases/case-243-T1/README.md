# CSS: Severance Office

来源：<https://codepen.io/alvaromontoro/pen/zxvqodP>（作者 alvaromontoro，CodePen 公开作品，默认 MIT 许可）

当前阶段见 [registry.csv](../registry.csv)（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C029；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：四工位办公室、隔板交错

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

`ground_truth.html` 以 `source.html` 为基础，四个工位和中央立柱的结构、样式数值都不动，只删 CodePen 样板和旋转动画。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 头部样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical；`<body translate="no">` 改为 `<body>` | 与作品和评分无关（用户同意删除） |
| 删除 `article` 的 `animation: spin 20s -13s linear infinite` 和 `@keyframes spin` | 勾选后整个场景绕竖轴持续旋转，准静态要求去掉 |
| `article` 的 `transform` 由 `… rotate3d(0,0,1,-30deg) translate3d(0px, 100px, -100px)` 改为 `… rotate3d(0,0,1, 234deg)` | 固定在来源打开时的默认画面，见下 |
| 删除左上角的“Animate”复选框（`<label><input type="checkbox"> Animate</label>`）、它的 `label` 样式，以及“未勾选时暂停动画”的 `body:has(input:not(:checked)) *` 规则 | 复选框唯一的作用是开关旋转；旋转去掉后它没有任何效果，留着会误导 |

- **静止状态：** 来源打开时复选框未勾选，动画以 `-13s` 的延迟暂停，画面停在关键帧的 13/20 处，即绕竖轴 234°；由于动画一直生效（只是暂停），`article` 上原来写的 `rotate -30deg` 加平移从来不会显示。GT 把这一默认画面写成静态 `transform`（数值由关键帧线性插值得出，与 `spin` 关键帧同一写法），所以 GT 与来源打开时看到的画面相同。另一个可选做法是改用 `article` 原来写的 `-30deg` 加平移，那是作者写下却从未显示的姿态，没有选。
- **保留的交互：** 无（来源唯一的交互是开关旋转的复选框）。
- **外部资源：** 无。
- **档位复核：** 去掉旋转和复选框后，GT 没有任何动态和交互，按难度模型 v2.1 为 T1，由暂定 T3 改为 T1（`registry.py retier`）。
- **作品价值：** 旋转只是展示用的可选动画，作品的空间价值在四个工位围绕中央立柱交错排列、隔板与电脑和桌面的遮挡、抽屉厚度、键盘与地面投影，静止后都在，所以照常改造。
