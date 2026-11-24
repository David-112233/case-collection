# case-233 GT 自检记录（2026-11-24，静态检查）

## 结论

- **渲染自检未完成。** 本云端环境没有可用的 Chromium（`playwright install chromium` 的下载被环境拒绝），出站代理对 `shadowshahriar.github.io` 返回 403。这个作品的画面高度依赖该站点上的三份样式表（`starter.css`、`3d.css`、`howto.css`）、七张纹理图和 `camera.js`，**一份都读不到**，所以本环境既不能截图，也不能读这些文件的源码。
- 已写好渲染自检脚本 [gt_check.py](gt_check.py)：在能联网的本地运行，得到 1280×800、375×812 两个视口下 GT 的默认、拖拽后、双击后、打开 How to? 面板、再关闭面板五种状态的截图，同视口下 `source.html` 的默认截图（用于对比），以及 `measurements.json`（运行中动画数、带过渡的元素、`--px` 与相机变量的计算值、场景变换、各部件包围盒、失败请求、画面是否随时间或拖拽变化）。

## 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)，只有删除，没有新增或改写的样式值 |
| 残留动画与脚本 | `ground_truth.html` 中已无 `animation`、`transition`、`@keyframes`、`<script>` |
| HTML 标签闭合 | Python html.parser 检查无未闭合、无错配；`<div>` 数与来源相同（81） |
| 外部资源 | 保留 Google Fonts（Montserrat）、`starter.css`、`3d.css`、`howto.css` 与七张纹理图；删除 CodePen favicon、canonical、`stopExecutionOnTimeout` 和 `camera.js` |

## 待本地补做（按风险排序）

1. **去掉 `camera.js` 后画面是否完整。** 读不到 `camera.js`，无法确认它是否在初始化时写入画面必需的值（例如 `--px` 尺寸单位、透视距离或场景变换）。看 `gt_*_default.png` 与 `source_*_default.png` 是否同一视角、同一大小；`measurements.json` 里 `px_var` 应非空、`scene_transform` 应不是 `none`。如果 GT 画面塌了，说明相机初值由脚本写入，需要把来源截图里的相机值写成静态 CSS（这一步会新增样式值，要先问用户）。
2. **外部样式表里有没有动画或过渡。** `running_animations` 应为 0、`nonzero_transitions` 应为空。若 `howto.css` 给面板开合加了过渡，按准静态要求要去掉时长，但那需要在 GT 里加一条覆盖规则，先报给用户。
3. **How to? 面板的开合方式。** 按标记推断是 `:target`（链接 `href="#howto"`，关闭按钮 `href="#"`），由 `howto.css` 实现。`gt_*_howto_open.png` 应显示面板，`gt_*_howto_closed.png` 应回到默认画面。
4. **拖拽和双击应不再改变画面**：`unchanged_by_drag`、`unchanged_by_dblclick` 应为 true；`static_over_time` 应为 true。
5. 对照截图核对 `input.json` 里按源码推断的外观描述（见 `../input_problem.md`）。
