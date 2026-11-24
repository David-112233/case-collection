# CSS '90s 3D Audio Cassette [CHALLENGES]

来源：<https://codepen.io/RaduBratan/pen/MWyKrRZ>（作者 RaduBratan，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C017；档位：T2（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：立体磁带、卷轴与投影

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只做删除，结构、样式数值、内联脚本、外部资源引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性、`//# sourceURL=pen.js` | 与作品和评分无关（用户同意删除） |
| 删除两个卷轴 `.cyl-2` 上的无限旋转动画 `spin`（5 秒一圈）及其 `@keyframes` | 持续动画 |
| 删除 `.cassette-scene`、`.shadow-scene`、`.shadow-shape1`、`.shadow-shape2`、`.cassette-shape` 上的 `transition: 0.6s ease` | 悬停效果改为直接到终态，与 case-231 处理悬停过渡的原则相同 |

- **静止状态：** 卷轴停在 `spin` 的 `from` 帧（`rotateY(0deg)`），与卷轴的基础样式相同，删掉动画不需要另写数值；卷轴上的六个齿是对称图形，任一角度看起来都差不多，选起点最符合“尽量尊重源码”。
- **保留的交互：** 鼠标移到磁带上（jQuery `mouseover`）时，磁带整体抬高（场景 `translateZ` 由 -8vw 变为 -6vw），地面上的两块投影变淡（透明度 0.3 到 0.2）并出现模糊扩散的边缘；移开（`mouseleave`）后还原。改动后瞬时完成。
- **保留的外部资源：** jQuery 3.5.1（cdnjs）、prefixfree 1.0.7（public.codepenassets.com）、Google Fonts 的 Inter（作者写的是 `css3?family=Inter`，地址本身可能无效，字体回退到 sans-serif，保留原样）。注释掉的两张纹理图片不加载。
- **档位复核：** GT 只剩“悬停磁带时抬起、投影变淡变虚，移开即还原”，相当于难度模型 v2.1 的“卡片 hover 上浮 + 阴影加深”，按 T2 判定，与入库暂定一致，不改名（投影是另一个元素，这一点的取舍见 input_problem.md 第 3 节）。
- **自检：** 默认状态已用云端浏览器经 raw.githack.com 在 1280、500 两个宽度截图核对；悬停在云端浏览器里触发不了，按源码推算，待本地运行 `review_20261124/gt_check.py`。见 [review_20261124/static_check.md](review_20261124/static_check.md)。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 写出，等用户审核 GT 与 input。写与不写的取舍和待定问题见 [input_problem.md](input_problem.md)。
