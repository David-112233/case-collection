# CSS Mechanical Keyboard

来源：<https://codepen.io/ykadosh/pen/bGKgxbe>（作者 ykadosh，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C042；档位：T2（GT 完成后复核仍为 T2，待用户确认）。
- 特色：机械键盘、错排立体键帽

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 由 `source.html` 复制后只做以下改动，其余结构、样式、脚本、文案、字体与外部资源引用都不动（完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)）：

| 改动 | 原因 |
|---|---|
| 删除 `apple-touch-icon`、`apple-mobile-web-app-title`、`icon`、`mask-icon` 四个 CodePen 图标与元信息，删除 `<link rel="canonical">`、`stopExecutionOnTimeout` 脚本和 `//# sourceURL=pen.js`，`<body translate="no">` 改为 `<body>` | CodePen 页面样板，与评分无关（用户同意删除）；来源与作者见本文件开头 |
| 删除 `.key` 的 `transition: transform 0.1s ease-out` | 按键按下、松开时键帽位移的过渡。按“一次性过渡保留交互、去掉时长”处理：按下即到下沉位置，松开即回原位 |

- **保留：** React 19 与 ReactDOM（esm.sh）、Google Fonts BioRhyme 700、CodePen 的 reset-2.0 样式表（作者在 CodePen 选用的 CSS 重置，影响版式）；按键时播放的机械键盘音效（cdn.yoavik.com 的 mp3，由按键触发而非自动播放，不影响画面，也无法用截图判定，按尊重源码保留，是否写入 input 见 [input_problem.md](input_problem.md)）。
- **静止状态：** 来源没有持续或自动播放的动画，默认画面即全部键帽抬起的静止画面，无需另选。
- **保留的交互：** 在物理键盘上按住 0–9、`.`、`+`、`-` 中的某个键时，小键盘上同字符的键帽下沉（沿键盘平面向右下移动 2rem，侧面变短，像被按下）；松开即还原。只有被按的那个键帽变化，页面上没有其他元素随之变化。
- **档位复核：** 仍为 **T2**。唯一的动态是按住键盘按键时对应键帽自身下沉、松开即还原，不保持状态、不驱动其他元素，类比“悬停只改自身”；触发是键盘而不是鼠标，**档位待用户确认**（见 [input_problem.md](input_problem.md) 第 3 节）。
- **外部资源与渲染：** 云端浏览器核对 React、BioRhyme、reset 样式表都正常加载，画面无渲染问题；500 宽时键盘被裁、出现横向滚动条（来源不是响应式，未改）。详见 [review_20261124/static_check.md](review_20261124/static_check.md)，截图测量脚本为 [review_20261124/shot_gt.py](review_20261124/shot_gt.py)。`review_20261124/pressed_preview.html` 只是自检用的按住状态预览，不属于 GT。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 写出，等用户审核 GT 与 input。取舍与待定问题见 [input_problem.md](input_problem.md)。
