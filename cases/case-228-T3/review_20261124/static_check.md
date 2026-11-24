# case-228 GT 自检记录（2026-11-24，静态检查）

## 结论

- **渲染自检未完成。** 本云端环境没有可用的 Chromium：`playwright install chromium` 的下载被环境拒绝，且出站代理对 `cdnjs.cloudflare.com`、`use.fontawesome.com`、`pro.fontawesome.com`、`public.codepenassets.com` 均返回 403，即使有浏览器，jQuery、图标脚本和 prefixfree 也加载不到，截图不能代表真实效果。
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

## 待本地补做

1. 运行 `gt_check.py`，确认 `running_animations`、`nonzero_transitions`、`nonzero_animation_names` 在两种状态下都为 0。
2. 确认 `icons_as_svg` 为 4（MENU、前进、后退、播放/暂停四个图标由 use.fontawesome.com 的 all.js 渲染），并看 `failed_requests` 里 pro.fontawesome.com 的 CSS 是否失败。按源码推断该 CSS 不影响画面：四个图标是脚本里用 `FontAwesome.library.add` 注册的自定义 SVG，不依赖 Pro 字体。
3. 对照截图核对 input.json 里按源码推断的外观描述（见 `input_problem.md`）。
