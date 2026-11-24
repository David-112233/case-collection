# Paper Cut-Out Effect w/CSS

来源：<https://codepen.io/glennphilp/pen/DBLzOW>（作者 glennphilp，CodePen 公开作品，默认 MIT 许可）

当前阶段：`input_draft`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C004；档位：T1（**暂定**，依据入库时的来源源码；`ground_truth.html` 完成后按 GT 的驱动方式重新判定，必要时用 `registry.py retier` 改名）。
- 特色：剪纸叠字、倾斜阴影

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动

`ground_truth.html` 由 `source.html` 复制，只删了与评分无关的 CodePen 样板，`<style>` 和 `<body>` 内容逐字未动：

| 改动 | 原因 |
|---|---|
| 删除 `apple-touch-icon`、`icon`、`mask-icon` 三个 CodePen 图标链接和 `apple-mobile-web-app-title` 元信息 | CodePen 页面样板，与作品无关，且是外部请求 |
| 删除 `<link rel="canonical">`（指向 CodePen 原作） | CodePen 样板；来源链接已记在本 README 和 metadata.json |
| `<body translate="no">` 改为 `<body>` | CodePen 给页面加的属性，与渲染无关 |

未改但需要知道的地方：

- **无动画、无交互。** 来源没有脚本、关键帧、过渡或悬停样式，GT 不需要固定静止状态。
- **字体**：标题只写了 `font-family: "Helvetica"`，没有通用族回退，也不加载外部字体。各系统多会把 Helvetica 映射到同类无衬线体，没有映射时会落到浏览器默认字体。保持来源原样。
- **来源里的无效声明**：`::before` 的第二条 `text-shadow` 写了四个长度值（文字阴影不支持扩展半径），`::after` 里有一行没有属性名的 `-ms-linear-gradient(...)`，还有 `-ms-` 前缀的变换。浏览器会忽略这些，实际生效的是第一条阴影和标准 `transform`。保持原样。
- **`rotateY` 与 `translateZ`**：父元素没有设 `perspective`，所以这两项几乎看不出效果，可见的倾斜主要来自 `skew`。保持原样。
- **窄屏**：五个字母实际总宽约 470px。宽度不足约 490px 时会换成两行，第一个 N 的纸片层和阴影与字母错开，页面横向溢出（来源相同）。input 只面向桌面宽屏，GT 未修，是否要修待用户定。
- **外部资源**：GT 不加载任何外部资源。

## GT 自检

见 [review_20261124/static_check.md](review_20261124/static_check.md)。本机装不了浏览器，改用项目的云端浏览器经 raw.githack 打开 GT，在 1280 和 500 宽截图核对（工具最小宽度 500），截图未入库。完整的双视口截图和测量仍可在本地运行 `review_20261124/shot_gt.py` 得到。

## 档位复核

GT 无任何动态：无动画、无过渡、无悬停或点击效果。按难度模型 v2.1 仍为 **T1**，与目录名一致，不需要 retier。

## input

[input.json](input.json) 由 GT 写出，问题与取舍见 [input_problem.md](input_problem.md)。外观描述已按云端浏览器截图核对并修正。阶段 `input_draft`：等用户审核 GT 与 input，规则草稿和 `generation_prompt.txt` 尚未写。

## 规则草稿

[rules_drafts/manual_v1/eval_rules.json](rules_drafts/manual_v1/eval_rules.json)，人可读版 [review.md](rules_drafts/manual_v1/review.md)：8 个 Requirement / 21 条 mandatory，全部来自用户 2026-11-24 改定的 input，没有常识条目，只计 D1，桌面单视口。`check_rules.py` 通过。等用户审核；台账阶段仍为 `input_draft`，因为 `input_approved` 只能由用户设置。`generation_prompt.txt` 未写：仓库里没有 `output_prompt_v2.txt` 模板。
