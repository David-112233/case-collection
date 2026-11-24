# case-228 GT 自检记录（2026-11-24）

## 结论

- **已做渲染核对（见文末“渲染核对”）。** 方法：项目共用的云端浏览器经 raw.githack.com 打开仓库提交 f00d72d 里的 `ground_truth.html`（用户同意此方式），视口 1280×800 和 500×800（浏览器最小宽度 500，375 无法实现），每个宽度看点击滚轮前后两种状态；截图只用于核对，未入库。
- 最初的本地渲染尝试未完成： 本云端环境没有可用的 Chromium：`playwright install chromium` 的下载被环境拒绝，且出站代理对 `cdnjs.cloudflare.com`、`use.fontawesome.com`、`pro.fontawesome.com`、`public.codepenassets.com` 均返回 403，即使有浏览器，jQuery、图标脚本和 prefixfree 也加载不到，截图不能代表真实效果。
- 已写好渲染自检脚本 [gt_check.py](gt_check.py)，在能联网的本地运行即可得到 1280×800、375×812 两个视口、默认与切换后两种状态的截图和 `measurements.json`（含运行中动画数、非零过渡数、图标是否转成 SVG、失败请求、各部件包围盒）。
- 下面是不需要浏览器的检查。

## 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)，只有删除，没有新增或改写的样式值 |
| 残留动画与过渡 | `ground_truth.html` 中已无 `transition`、`animation:`、`@keyframes`（仅剩作者注释掉的 `/*@keyframes start*/`） |
| 静止帧与基础样式一致 | 被删的四个关键帧的 `from` 帧与各元素的基础样式逐项相同：`hover-ipod` from 为 `translateY(0)`（基础为无变换）；`hover-screen`、`hover-wheel` from 与 `.screen-scene`、`.wheel-scene` 的基础 `transform` 相同；`light` from 的宽高 22.5vw、opacity 0.2、blur 2px、box-shadow 35px 25px 与 `.light-scene` 基础值相同 |
| 内联脚本语法 | `node --check` 通过 |
| HTML 标签闭合 | Python html.parser 检查无未闭合、无错配 |
| 外部资源 | 保留作者引用的 4 个外部资源；CodePen 的 favicon、canonical、`stopExecutionOnTimeout` 已删 |

## 仍可在本地补做（可选）

1. 运行 `gt_check.py`，确认 `running_animations`、`nonzero_transitions`、`nonzero_animation_names` 在两种状态下都为 0。
2. 确认 `icons_as_svg` 为 4（MENU、前进、后退、播放/暂停四个图标由 use.fontawesome.com 的 all.js 渲染），并看 `failed_requests` 里 pro.fontawesome.com 的 CSS 是否失败。按源码推断该 CSS 不影响画面：四个图标是脚本里用 `FontAwesome.library.add` 注册的自定义 SVG，不依赖 Pro 字体。
3. 对照截图核对 input.json 里按源码推断的外观描述（见 `input_problem.md`）。

## 渲染核对（2026-11-24，云端浏览器）

| 项目 | 结果 |
|---|---|
| 外部资源 | 滚轮上四个图标都以 SVG 显示（MENU、快进、快退、播放/暂停），说明 jQuery 与 Font Awesome all.js 已加载；点击切换生效，说明 jQuery 正常。Pro CSS 是否加载失败看不到控制台，无法确认，但画面不依赖它 |
| 默认状态、视角 | 与 input 一致：机身居中，长轴左上到右下，底端在右下更近；可见正面、左侧长边厚度和底端端面（端面上有长方形充电口和圆形耳机孔）；屏幕近顶端、滚轮近底端、都在正面中线上 |
| 默认状态、颜色 | 珊瑚红背景；正面明黄最亮，底端端面略暗，左侧长边更暗，圆角处分段过渡；黑屏、白滚轮、中央按钮与正面同色；投影为半透明深色圆角矩形，偏向机身左侧并露出在左长边外 |
| 切换 | 点击滚轮立即进入发光模式并保持，再点立即回到默认，没有过渡；发光模式画面静止 |
| 发光模式 | 背景黑；投影消失；正面浅灰蓝，侧边与端面白色，轮廓有蓝色外发光；充电口和耳机孔变蓝；中央按钮浅蓝；机身周围一团暗淡的蓝灰色光晕 |
| 视口缩放 | 500 宽时整体按宽度等比缩小、仍居中；图标字号固定，在小滚轮上显得拥挤、彼此贴近 |

### 发现的渲染问题（来源本身就有，GT 未改）

发光模式下，屏幕和滚轮会部分或全部被半透明的机身正面盖住：1280 宽时屏幕只有右侧一条仍是黑色，滚轮右侧一块较亮，其余部分沿一条斜线被正面覆盖、发灰；500 宽时屏幕和滚轮几乎完全被盖住，只隐约可见。默认状态没有这个问题。

- 用同一方式打开 `source.html` 并切换，来源在动画的不同时刻都有同样的问题，所以不是 GT 选静止帧造成的。
- 原因推断：屏幕和滚轮只比机身正面高约 0.14vw，发光模式给机身各面加了 0.8 的不透明度后，浏览器的三维深度排序把它们排到了正面之下。来源的悬浮动画让机身和屏幕、滚轮同向上移 20px，二者间距不变，所以换成其他静止帧也解决不了。
- 处理：为尊重源码，GT 不改；input 里不再描述发光模式下屏幕和滚轮的样子。是否要对 GT 做修正交用户决定，见 `input_problem.md`。
