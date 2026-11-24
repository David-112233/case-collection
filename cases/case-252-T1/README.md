# Responsive banners (clean markup, CSS grid & variables)

来源：<https://codepen.io/thebabydino/pen/pBmMaJ>（作者 thebabydino，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C041；档位：T1（入库时暂定，GT 完成后复核仍为 T1）。
- 特色：斜切编号条、圆标压层

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 由 `source.html` 复制后只做以下改动，`<style>` 与 `<body>` 内容逐字不动（完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)）：

| 改动 | 原因 |
|---|---|
| 删除 `apple-touch-icon`、`apple-mobile-web-app-title`、`icon`、`mask-icon` 四个 CodePen 图标与元信息，删除 `<link rel="canonical">`，`<body translate="no">` 改为 `<body>` | CodePen 页面样板，与评分无关（用户同意删除）；来源与作者见本文件开头 |

- **保留：** `prefixfree-1.0.7.min.js`（作者在 CodePen 选用的 CSS 前缀补全脚本，现代浏览器下不改变画面，与 case-228 的处理一致）；两种版式之间的响应式切换（775px 以下变为窄屏版式，这是作品的一部分）。
- **静止状态：** 来源没有任何动画、过渡或交互，默认画面即静止画面，无需另选。
- **档位复核：** 仍为 **T1**（无任何动态、无交互），目录名不变。
- **自检：** 截图测量脚本 [review_20261124/shot_gt.py](review_20261124/shot_gt.py)，渲染核对见 [review_20261124/static_check.md](review_20261124/static_check.md)。

## input 草稿（2026-11-24，duet）

[input.json](input.json) 由 GT 写出，外观经云端浏览器渲染核对（1280、500 宽），等用户审核 GT 与 input。取舍与待定问题见 [input_problem.md](input_problem.md)。
