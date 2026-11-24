# case-233 GT 自检记录

## 渲染核对（2026-11-24，云端浏览器）

用云端浏览器打开 `https://raw.githack.com/David-112233/case-collection/main/cases/case-233-T3/ground_truth.html`（用户同意的地址格式），在 1280×800 和 500×800 下各截默认画面，在两个宽度下各打开一次 How to? 面板，并在 1280 宽下关闭面板。截图未提交。

| 核对项 | 结论 |
|---|---|
| 外部资源能否加载 | 能。`starter.css`、`3d.css`、`howto.css` 生效（场景成立、面板有样式），蛋糕海绵气孔、盘面纹理等贴图都显示，Montserrat 字体生效 |
| 去掉 `camera.js` 后画面是否完整 | 完整。相机停在 CSS 初值，蛋糕、盘子、水果、叶片、投影都正常，说明相机初值不依赖脚本写入 |
| 画面是否静止 | 是。相隔约 1 分钟的两张 1280 宽默认截图目视一致，蛋糕不自动旋转 |
| 视角与缺口 | 斜上方俯视；缺口在蛋糕右侧、朝右前方敞开；只看得到缺口靠后一侧的切面，靠前一侧的切面背对观者（原 input 写“两个切面都能看到”，已改） |
| 切面分层 | 从上到下：粉红顶层、浅棕黄海绵、粉色奶油夹层、浅棕黄海绵、红褐底层，与推算一致 |
| 盘子 | 明显是多边形（十四边形）而不是圆形，原 input 写“圆形盘子”，已改 |
| 水果与叶片 | 10 个半球形水果，7 红 3 浅橙米色，从左前方一端数第 2、5、8 个为浅色；7 片叶片从水果之间探出，看不出“哪颗草莓上有 3 片”，原 input 的这句已删 |
| 投影 | 盘子右侧和下方有大片模糊投影；蛋糕阴影落在盘面右侧、伸进缺口 |
| 盘面上的锯齿边 | 盘面右侧、缺口下方能看到一条锯齿形的明暗分界，是蛋糕阴影（`.cake-base-shadow`）与盘面叠出的效果，来源同样如此，GT 未改，input 不写 |
| 500 宽 | 整组等比缩小，盘子刚好容纳在视口宽度内；How to? 仍在右上角 |
| How to? 面板 | 点击后 URL 变为 `#howto`，面板出现：浅灰圆角卡片、粗体大标题、显示桌面端 7 条列表（ctrl/alt/shift 为按键样式），页面其余部分压上半透明灰色遮罩；1280 宽时居中，500 宽时贴顶并几乎占满宽度。触屏列表未显示（浏览器为鼠标设备）。遮罩就是 `href="#"` 的关闭链接，聚焦后回车，URL 变为 `#`，面板和遮罩消失，回到默认画面 |
| 面板有无过渡 | 打开后两张相隔约 10 秒的截图里，卡片宽度从约 467px 变为约 462px，可能是 `howto.css` 里有很短的开合过渡或悬停效果；截图间隔太长无法判断，本地运行 `gt_check.py` 看 `nonzero_transitions` |

## 静态检查（2026-11-24，渲染核对之前）

### 当时的结论

- **渲染自检未完成。** 本云端环境没有可用的 Chromium（`playwright install chromium` 的下载被环境拒绝），出站代理对 `shadowshahriar.github.io` 返回 403。这个作品的画面高度依赖该站点上的三份样式表（`starter.css`、`3d.css`、`howto.css`）、七张纹理图和 `camera.js`，**一份都读不到**，所以本环境既不能截图，也不能读这些文件的源码。
- 已写好渲染自检脚本 [gt_check.py](gt_check.py)：在能联网的本地运行，得到 1280×800、375×812 两个视口下 GT 的默认、拖拽后、双击后、打开 How to? 面板、再关闭面板五种状态的截图，同视口下 `source.html` 的默认截图（用于对比），以及 `measurements.json`（运行中动画数、带过渡的元素、`--px` 与相机变量的计算值、场景变换、各部件包围盒、失败请求、画面是否随时间或拖拽变化）。

### 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)，只有删除，没有新增或改写的样式值 |
| 残留动画与脚本 | `ground_truth.html` 中已无 `animation`、`transition`、`@keyframes`、`<script>` |
| HTML 标签闭合 | Python html.parser 检查无未闭合、无错配；`<div>` 数与来源相同（81） |
| 外部资源 | 保留 Google Fonts（Montserrat）、`starter.css`、`3d.css`、`howto.css` 与七张纹理图；删除 CodePen favicon、canonical、`stopExecutionOnTimeout` 和 `camera.js` |

### 当时列的待补项（第 1、3、5 项已由上面的渲染核对完成，第 2、4 项仍可用 gt_check.py 补测）

1. **去掉 `camera.js` 后画面是否完整。** 读不到 `camera.js`，无法确认它是否在初始化时写入画面必需的值（例如 `--px` 尺寸单位、透视距离或场景变换）。看 `gt_*_default.png` 与 `source_*_default.png` 是否同一视角、同一大小；`measurements.json` 里 `px_var` 应非空、`scene_transform` 应不是 `none`。如果 GT 画面塌了，说明相机初值由脚本写入，需要把来源截图里的相机值写成静态 CSS（这一步会新增样式值，要先问用户）。
2. **外部样式表里有没有动画或过渡。** `running_animations` 应为 0、`nonzero_transitions` 应为空。若 `howto.css` 给面板开合加了过渡，按准静态要求要去掉时长，但那需要在 GT 里加一条覆盖规则，先报给用户。
3. **How to? 面板的开合方式。** 按标记推断是 `:target`（链接 `href="#howto"`，关闭按钮 `href="#"`），由 `howto.css` 实现。`gt_*_howto_open.png` 应显示面板，`gt_*_howto_closed.png` 应回到默认画面。
4. **拖拽和双击应不再改变画面**：`unchanged_by_drag`、`unchanged_by_dblclick` 应为 true；`static_over_time` 应为 true。
5. 对照截图核对 `input.json` 里按源码推断的外观描述（见 `../input_problem.md`）。
