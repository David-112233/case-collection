# case-236 GT 自检记录（2026-11-24）

## 结论

- **已渲染核对。** 按用户同意的方式，用云端浏览器经 raw.githack.com 打开提交 `c04f99c` 中的 `cases/case-236-T3/ground_truth.html`（retier 前的路径），在 1280×800 和 500×800 两个视口截图查看。截图不入库。
- 页面不引用任何外部资源，打开即完整渲染。画面与 `input.json` 的描述一致：游戏机平放、长轴从左上斜向右下，粉色左手柄、灰色主机、青色右手柄，能看到近侧长侧面（中部一个长条插口和两侧两个圆孔）和右手柄端面，右侧远角有黑色肩键，投影向右侧和远侧伸出。
- 500×800 下模型按 vmin 缩放后几乎占满宽度，右端肩键和投影的边缘贴近视口右缘。
- 同一提交的 `source.html` 在 1280×800 下截图，与 GT 画面逐处相同（GT 只删了脚本和过渡，初始画面不受影响）。
- 这台无头浏览器里，手柄弧形边角处有几处面片穿插（能隐约看到内侧的面），来源与 GT 完全一样，属于来源 CSS 3D 在该渲染器下的表现，不是 GT 改动造成的；input 没有描述这些细节。

## 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)：只有删除（样板、`cursor: pointer`、`.main` 的 `transition`、整段交互脚本），没有新增或改写的样式值 |
| 残留动画、过渡、脚本 | `ground_truth.html` 中已无 `animation`、`transition`、`@keyframes`、`<script>` |
| 初始视角不变 | 来源的 `moveModel()` 只在按下鼠标拖动或滚轮时写入 `.main` 的内联变换；打开时 `.main` 用 CSS 原值，GT 保留该值，所以初始画面相同（截图对比已确认） |
| HTML 标签闭合 | Python html.parser 检查无未闭合、无错配 |
| 外部资源 | 无 |

## 本地可补做

运行 [gt_check.py](gt_check.py)：得到 1280×800、500×800、375×812 截图和 `measurements.json`，确认 `running_animations`、`nonzero_transitions` 为 0，拖动和滚轮后 `main_transform` 与部件包围盒不变。
