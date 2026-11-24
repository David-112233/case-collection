# case-237 GT 自检记录（2026-11-24）

## 结论

- **默认状态已渲染核对。** 按用户同意的方式，用云端浏览器经 raw.githack.com 打开提交 `8dc0eb9` 中的 `ground_truth.html`，在 1280×800 和 500×800 两个视口截图查看。截图不入库。
- 外部字体 Bungee、Teko 已加载（标志、“VOL”、标签文字、“CLICK ME”都是对应字体），标签文字读作“COOL BAND ALBUM”。画面与 `input.json` 的默认状态描述一致。
- 唱机面板是固定像素尺寸（450×450），不随视口缩放；500 宽下左右各留约 25 px，“CLICK ME”贴近右侧。
- **点击音量刻度已核对：** 点击刻度 9 后，旋钮指示线立即转到指向 9，无过渡。
- **点击电源键未能在云端浏览器里核对：** 电源键是没有文字的 `div`，浏览器工具只能按页面结构里的元素点击，拿不到这个元素。播放状态按源码推算：唱臂的旋转中心是右上角底座圆心（`.tonebar` 本身没有尺寸），顺时针 17° 后，杆端唱头从底座正下方约 305 px 处向左移约 89 px，落在唱片半径约 169 px 处（唱片半径约 187 px），即唱片外圈靠右下；指示灯变量 `--pwlight` 变为 `red`；提示 `opacity` 变为 0。待本地运行 `gt_check.py` 截图确认。

## 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)：只删除样板、CodePen 循环保护调用、动画、过渡和无引用的关键帧；脚本里把两处动画赋值改为直接写终态变换，没有新增样式值 |
| 残留动画与过渡 | `ground_truth.html` 中已无 `animation`、`transition`、`@keyframes`、`window.CP` |
| 静止帧 | 唱臂播放时停在 17°，与 `movebar` 2% 帧、100% 帧相同；停止时 0°，与 `mb1` 终帧相同；箭头停在 `point` 动画起点（基础 `top: -30px`） |
| 内联脚本语法 | `node --check` 通过 |
| HTML 标签闭合 | 与来源相同，未改动 HTML 结构 |
| 外部资源 | Google Fonts（Bungee、Teko）、normalize.css、Tone.js 15.1.2；字体在云端浏览器里加载成功，Tone.js 是否加载、音乐能否播放未核实 |

## 待本地补做

运行 [gt_check.py](gt_check.py)：确认点击电源键后 `running_animations`、`nonzero_transitions` 为 0，唱臂 `transform` 为 17°、`--pwlight` 为 red、提示 `opacity` 为 0，2 秒后仍不变；`tone` 为 `object`；再次点击后全部复原。
