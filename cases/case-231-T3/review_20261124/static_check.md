# case-231 GT 自检记录（2026-11-24）

## 结论

- **渲染核对已做（云端浏览器）。** 用户把仓库改为公开后，经用户同意，用云端浏览器经 raw.githack.com 打开 `main` 上的 `cases/case-231-T3/ground_truth.html`，在 1280×800 和 500×900 两个视口查看默认、点击喇叭图标播放、播放约 2 秒后、再次点击停止四种状态，另用 2 倍、3 倍局部截图看细节。浏览器工具的最小宽度是 500，**375 宽无法实现**，用 500 代替。截图只在核对时查看，没有入库。
- **核对结论：** `input.json` 里按 CSS 推算的视角、部件位置、配色、仓门方向和播放切换都与渲染一致，input 不用改（逐条见 `input_problem.md` 第 1 节）。GT 没有发现需要修改的渲染问题。
- **没能核实的：** ① 播放键的悬停变色：云端浏览器的页面快照里只有喇叭图标可操作，播放键没有可指向的引用，无法悬停或点击它，播放切换是通过喇叭图标触发的；② 喇叭图标悬停放大 1.1 倍：截图里看不出明确差别；③ 歌曲是否真的在播放：浏览器控制台有报错或警告但内容不可见，无法读取音频状态。这三项仍以源码为准，可在本地运行 [gt_check.py](gt_check.py)（需要 Playwright Chromium）补测。
- 早先在没有浏览器时用矩阵推算画的 `projection_*.png` 示意图和推算脚本已删除；它们推算的各部件位置与这次渲染一致。

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
| 渲染（1280×800） | 机身约占 x 489–794、y 314–540，水平、垂直居中；正面和右侧面可见，顶面只露一条窄边；投影向画面右侧拉出，右端到 x≈979；喇叭图标在 y 50–80、水平居中。播放时仓门由前倾变为贴合仓口，播放键缩进机身并略变深，图标换成带声波的样式；播放约 2 秒后画面不变；停止后复原 |
| 渲染（500×900） | 机身等比缩小到约 120px 宽、仍在正中；扬声器方孔、磁带卷轴和橙色带子在 3 倍局部图里清楚可辨；播放与停止的变化同 1280 |
| 放大截图的伪影 | 1280 宽用 2 倍放大截取局部时，机身顶面右半（扬声器上方）出现一块灰色；1 倍截图里没有。属浏览器在高分辨率下对 3D 平面排序的绘制伪影，GT 不改 |

## 待本地补做

1. 运行 `gt_check.py`，确认 `running_animations`、`nonzero_transitions`、`nonzero_animation_names` 在所有状态下都为 0；`*_playing` 的 `audio.paused` 为 false，`*_back_to_default` 为 true 且 `currentTime` 为 0。
2. 看 `failed_requests` 与 `hover_cta` 状态，补测歌曲加载和播放键悬停变色；375 宽的截图也在这一步补上。
