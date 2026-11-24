# 3D Radio 

来源：<https://codepen.io/ricardoolivaalonso/pen/ExPpgqG>（作者 ricardoolivaalonso，CodePen 公开作品，默认 MIT 许可）

当前阶段见台账（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C005；档位：T3（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：立体收音机、磁带仓与凹槽

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |
| `ground_truth.html` | 准静态参考页（2026-11-24，duet），改动见下 |
| `review_20261124/` | GT 自检：静态检查记录、源码差异、本地渲染自检脚本、CSS 3D 数值投影示意 |
| `input.json` | 由 GT 写出的题目（2026-11-24，duet），**等用户审核** |
| `input_problem.md` | input 的推算依据、取舍和待用户定的事 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，结构、样式数值、id 与 class、内联脚本、外部资源引用都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性、`//# sourceURL=pen.js` | 与作品和评分无关（用户同意删除） |
| 删除作者把整份 HTML 文档贴进 CodePen 时留在 body 里的嵌套 `<!DOCTYPE>`、`<html lang="es">`、`<head>`、`<body>` 及闭合标签、重复的 `<meta charset>`，以及指向不存在文件的 `main.css`、`main.js`；其中的 `<meta name="viewport">` 移到 head | 浏览器解析时本就忽略这些嵌套标签，两个相对路径文件在来源中也是 404；viewport 声明保留原文，只换到规范位置 |
| 删除 `.is-radio-active`（机身左右摇摆）、`.is-shadow-active`（投影伸缩）两个无限往复动画及其 `@keyframes radio`、`shadow` | 准静态要求去掉持续动画 |
| 删除 `.is-circle-active` 与 `@keyframes circle` | 来源里给扬声器加这个类的那行脚本作者已注释掉，从不生效，属死代码 |
| 删除 `.cover`、`.is-cover-active`（仓门开合 0.2s）、`.is-button-active`（按键 0.1s）、`.button--cta:hover .button__front`（悬停变色 0.1s）上的 `transition` | 点击切换改为直接到终态（用户同意）；悬停变色的 0.1s 过渡按同一原则去掉，变色本身保留 |

- **静止状态：** 播放时的机身摇摆和投影伸缩固定在关键帧的 0%/85% 帧，它与机身、投影的基础样式完全相同，删掉动画不用另写数值，也就是“播放中”机身保持端正、不摇摆。另一端的帧（机身抬高 0.2vw 并左右偏转 2°）只是往复动画的一瞬，不适合当静止状态。
- **保留的交互：** ① 点击橙色键或顶部的喇叭图标：开始循环播放歌曲，橙色键保持按下，透明仓门由前倾变为竖直合上，喇叭图标由静音（带 ×）换成有声波；再点一次全部复原、歌曲停止并回到开头。切换瞬时完成，状态保持到下次点击。② 悬停橙色键时它的正面变深一点；悬停喇叭图标时图标放大到 1.1 倍。
- **保留的外部资源：** 只有一首歌（raw.githubusercontent.com 上作者仓库里的 `song.mp3`，约 11.5 秒）。本环境用 curl 下载成功、格式正确，**未在浏览器里核实播放**。
- **档位复核：** GT 仍有“点击后进入并保持播放状态”（按键、仓门、图标、音乐都保持到再次点击），按难度模型 v2.1 为 T3，与入库暂定一致，不改名。
- **自检：** 本环境装不了浏览器，只完成了静态检查和 CSS 3D 数值投影示意，见 [review_20261124/static_check.md](review_20261124/static_check.md)；渲染自检脚本 `review_20261124/gt_check.py` 已备好，待本地运行。
