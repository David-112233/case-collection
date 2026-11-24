# Folding card animation

来源：<https://codepen.io/Ak-407/pen/MYgKoME>（作者 Ak-407，CodePen 公开作品，默认 MIT 许可）

当前阶段：`admitted`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C006；档位：T2（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：折叠卡片、页面折角

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

入库时的下一步说明（保留原文）：duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动

`ground_truth.html` 由 `source.html` 复制后只做以下改动，结构、样式、文案、字体引用与版式其余不动（`diff source.html ground_truth.html` 可复现）：

| 改动 | 原因 |
|---|---|
| 删除 `apple-touch-icon`、`apple-mobile-web-app-title`、`icon`、`mask-icon` 四个 CodePen 图标与元信息，删除 `<link rel="canonical">`，`<body translate="no">` 改为 `<body>` | CodePen 页面样板，与评分无关；来源与作者见本文件开头 |
| 删除 `.articles__article` 的 `animation-name: animateIn` 及其时长、延迟、填充、缓动五行，删除三个 `<li>` 上只供动画延迟用的 `style="--animation-order:N"` | 入场动画。来源里**没有** `@keyframes animateIn`，这组声明本来就不产生可见效果，删掉后静止画面不变 |
| 删除 `.articles__link:after`、`.articles__content--rhs`、`.articles__link:hover:after` 三处 `transition` | 去掉悬停过渡的时长与箭头的 0.25s 延迟，悬停时直接到终态、移开直接还原（按用户同意的“一次性过渡去掉时长、直接到终态”处理，悬停同样处理，见 `input_problem.md` 问题 2） |

保留未动：Google Fonts 样式表整条引用（其中 Bebas Neue、Righteous 页面并未使用，来源如此）；`<a>` 没有 `href`（来源如此，因此卡片不可键盘聚焦）；375 宽下的横向溢出（来源不是响应式）。

**静止状态**：默认画面就是来源的静止画面，三张卡片完整展开、箭头不可见；没有需要另选的动画帧。

**保留的交互**：悬停卡片时右半边向观者翻折约 50°、变浅灰，卡片右侧露出浅绿底面并出现白色箭头；指针离开即还原。

**外部资源**：Google Fonts 样式表在云端可访问（返回 200，含 Bitter 400/700）；渲染核对确认 Bitter 已加载。没有外部脚本或图片。

**自检**：见 [review_20261124/](review_20261124/static_check.md)。已用云端浏览器经 raw.githack.com 在 1280、500 宽下核对，渲染与推算一致，GT 无渲染问题；375 宽和脚本测量可在本地补跑 `gt_selfcheck.py`。

**档位复核**：仍为 **T2**。GT 唯一的动态是悬停卡片时卡片自身的右半边和自身的箭头伪元素发生变化，指针离开即还原、不保持状态，符合难度模型 v2.1“悬停只改被指向元素自身”的 T2 定义；目录名不变。疑点见 `input_problem.md` 问题 4。
