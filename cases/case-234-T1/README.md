# 📸 Polaroid Camera In CSS

来源：<https://codepen.io/fossheim/pen/xxboBzO>（作者 fossheim，CodePen 公开作品，默认 MIT 许可）

当前阶段：`admitted`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C008；档位：T1（入库时按来源源码暂定，GT 完成后已复核，仍为 T1，见下文“档位复核”）。
- 特色：拍立得、凹面取景器

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

`ground_truth.html` 以 `source.html` 为基础，只做删除，`<style>` 的全部样式、相机的 DOM 结构和文案逐字未动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical；`<body translate="no">` 改为 `<body>` | 与作品和评分无关（用户同意删除） |
| 删除内嵌文档里的 `<link rel="stylesheet" href="/style.css">` 和 `<script src="/script.js" defer></script>` | 相对路径，离开 CodePen 后加载不到。样式已全部内联在 `<style>` 里；`/script.js` 内容**未核验**，按推断它在 CodePen 上也不存在（理由见 [static_check.md](review_20261124/static_check.md)），删掉不改变画面 |

- **未改但需要知道的地方：** 作者把一整份 HTML 文档粘进了 HTML 面板，`<body>` 里还嵌着一层 `<!DOCTYPE html><html><head>…<body>`。浏览器会忽略多出的 `html`、`head`、`body` 标签，画面不受影响；为尊重源码保留原样。`.sensor` 的 `backround-size` 拼写错误、几处被渐变盖住的 `background-color: red`、两个空的 `div`（`.title`、`.type`）也保持原样。
- **静止状态：** 来源本身没有动画、过渡、悬停样式或脚本，GT 不需要固定静止状态，画面就是来源的唯一状态。
- **保留的交互：** 无。来源没有可交互的部分，GT 也不加。
- **外部资源：** GT 不加载任何外部资源；标志文字用本地字体 `"Helvetica Neue", "Helvetica", sans-serif`。
- **窄屏：** 相机固定 570×470、不缩放，375 视口下向右溢出约 195 px 并出现横向滚动（按规范推算）。来源如此，GT 不加响应式。

## 档位复核

GT 无任何动态：无动画、无过渡、无悬停或点击效果。按难度模型 v2.1 为 **T1**，与目录名一致，不需要 retier。前提是 `/script.js` 确实不存在或不带交互；若用户知道原作有脚本交互，档位需重判。

## GT 自检

见 [review_20261124/static_check.md](review_20261124/static_check.md)。**截图和测量没做成**：云端环境没有可用的浏览器。渲染自检脚本 [review_20261124/gt_check.py](review_20261124/gt_check.py) 已备好，可在本地运行。画面描述来自样式推算，尚未经渲染验证。
