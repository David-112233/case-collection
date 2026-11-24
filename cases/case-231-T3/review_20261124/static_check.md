# case-231 GT 自检记录（2026-11-24，静态检查）

## 结论

- **渲染自检未完成。** 本云端环境没有可用的 Chromium：`playwright install chromium` 的下载被出站代理拒绝（403，`cdn.playwright.dev` 不在允许名单）。没有截图，也没有浏览器里的测量。
- 已写好渲染自检脚本 [gt_check.py](gt_check.py)：在本地运行即可得到 1280×800、375×812 两个视口下 默认、悬停橙色键、播放中、播放 1.5 秒后、再次点击回到默认 五种状态的截图和 `measurements.json`（含运行中动画数、非零过渡数、音频是否在播放、各部件包围盒与变换）。
- 为了在没有浏览器的情况下看清构图，写了 [css3d_projection.py](css3d_projection.py)：用 GT 自己的 `transform`、`transform-origin`、尺寸逐个矩阵推算每个面的位置，按深度缓冲画成平面多边形。产物 `projection_<状态>_<宽>.png/json` **不是浏览器截图**：只画面的底色，忽略渐变、边框、内阴影和伪元素（扬声器点阵画成整块深色，磁带的深色边框、卷轴、橙色带子和右侧滑槽都没画出来）。它只用来判断哪些面朝向观者、各部件大致在哪。

## 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)：除把 `<meta name="viewport">` 从误贴在 body 里的嵌套文档移到 head 外，只有删除，没有新增或改写的样式值 |
| 残留动画与过渡 | `<style>` 中已无 `animation`、`transition`、`@keyframes` |
| 静止帧与基础样式一致 | 被删的 `radio` 关键帧的 0%/85% 帧与 `.radio` 基础 `transform` 完全相同（多出的 `rotateY(0deg)` 为恒等），`shadow` 关键帧 0%/60%/85%/100% 帧的 `height: 400%; left: 0%` 与 `.shadow-1` 基础值相同；删掉动画后播放状态的机身和投影就停在这一帧 |
| `circle` 关键帧 | 来源里只被 `.is-circle-active` 引用，而脚本中给扬声器加这个类的那行作者已注释掉，来源运行时也从不生效；作为死代码一并删除 |
| 内联脚本 | 与来源逐字相同（只删了 `//# sourceURL=pen.js`）；`node --check` 通过。脚本仍会切换 `is-radio-active`、`is-shadow-active` 两个类，它们在 GT 里已没有样式，切换无视觉效果 |
| id 与 class | 与来源完全相同（`audio`、`button-cta`、`circles`、`cover`、`radio`、`shadow`、`soff`、`son`） |
| HTML 标签闭合 | Python html.parser 检查无未闭合、无错配 |
| 外部资源 | 只剩一首歌：`raw.githubusercontent.com/ricardoolivaalonso/recursos/master/asiatic-a/song.mp3`。本环境 curl 下载成功：80 710 字节，MPEG layer III，44.1 kHz，时长约 11.5 秒。是否能在浏览器里播放未核实 |
| 数值投影（1280×800，默认） | 机身约占 x 489–794、y 314–540，水平、垂直都居中；前脸和右侧面可见，顶面只露出一条窄边；投影向右后方拉出，右端到 x≈979。播放状态下仓门由上沿外倾变为竖直，橙色键整体后退 |

## 待本地补做

1. 运行 `gt_check.py`，确认 `running_animations`、`nonzero_transitions`、`nonzero_animation_names` 在所有状态下都为 0；`*_playing` 的 `audio.paused` 为 false，`*_back_to_default` 为 true 且 `currentTime` 为 0。
2. 看 `failed_requests` 是否为空（歌曲能否加载）。
3. 对照截图核对 `input.json` 里由 CSS 推算的外观描述（见 `input_problem.md` 第 3 节），尤其是：扬声器点阵的样子、磁带的深色边框与两个卷轴、右侧的滑块与滑槽、仓门倾斜的方向。
