# CSS 3D Cake 🍰

来源：<https://codepen.io/bofengbu/pen/JjvYZoJ>（作者 bofengbu，CodePen 公开作品，默认 MIT 许可）

当前阶段：`admitted`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C007；档位：T2（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：分层蛋糕、夹心切面

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只做删除，结构、样式数值、文案、外部样式表与纹理引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性 | 与作品和评分无关（用户同意删除） |
| 删除外部脚本 `camera.js` 及其初始化脚本（`new Camera()…init()`） | 它提供拖拽旋转、Ctrl/Alt/Shift + 拖拽平移和改透视、滚轮缩放、双击开关自动旋转，属于拖拽类复杂交互和持续动画，准静态 GT 不保留 |
| 删除 `[data-camera][data-autorotate]` 下的三条自动旋转规则（场景 `rotateCamera`、草莓两片 `rotateSphereBefore/After`）及两个 `@keyframes` | 去掉持续动画。去掉 `camera.js` 后 `data-autorotate` 不会再被设置，这三条已是死代码，一并删掉 |

- **静止状态：** 相机固定在作者在内联 CSS“camera configuration”里写的初值：`--cameraZ: 108`、`--cameraY: 46`、`--perspective: 800`。这是作品加载后的起始视角，也是唯一由作者明确给出的视角；蛋糕本身转了 `--cake-rZ: -108deg`，与相机的 108 正好抵消，说明作者让切掉的那一块缺口在起始视角下朝向观者，夹心切面最完整。草莓用的是“两片交叉圆片”的做法，静止时停在基础样式给的角度（即去掉动画后的状态，与 `from` 帧一致）。
- **保留的交互：** 右上角的 “How to?” 链接与说明面板（`#howto`），按标记推断是 `:target` 开合：点链接打开面板并保持，点面板的关闭区域（`href="#"`）关闭。面板文字列出的是 `camera.js` 的手势，GT 已不支持这些手势；按“尽量尊重源码”保留原文，是否删掉整块面板待用户定（见 [input_problem.md](input_problem.md)）。
- **外部资源：** 保留 Google Fonts（Montserrat）、`starter.css`、`3d.css`、`howto.css` 与七张纹理图（海绵、海绵切面、蛋糕顶面、盘子三张、噪点）。场景容器的透视与相机变换、`--px` 尺寸单位、页面背景图层、说明面板的样式都在这三份样式表里，**本环境读不到，均未核实**；也无法确认 `camera.js` 有没有在初始化时写入画面必需的值。详见 [review_20261124/static_check.md](review_20261124/static_check.md)。
- **自检：** 本环境无法渲染，只完成了静态检查；渲染自检脚本 [review_20261124/gt_check.py](review_20261124/gt_check.py) 已备好，待本地运行。
