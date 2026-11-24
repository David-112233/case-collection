# case-239 GT 自检记录（2026-11-24）

## 结论

- **默认状态已渲染核对。** 按用户同意的方式，用云端浏览器经 raw.githack.com 打开提交 `9d18464` 中的 `ground_truth.html`，在 1280×800 和 500×800 两个视口截图查看。截图不入库。
- 画面与 `input.json` 的默认状态描述一致：磁带竖立、正面朝向观者偏左，能看到右侧端面和窄顶面；窗口里两个暗黄色卷轴；投影向右侧伸出。模型按 vw 缩放，500 宽下变小但完整居中；文字字号按 vmax，窄屏下相对显得大一些。
- **悬停未能在云端浏览器里核对：** 浏览器工具认为页面上唯一可选中的文字被 3D 面片遮挡，悬停操作超时。悬停效果按源码推算：jQuery 在 `mouseover` 时把 `.cassette-scene` 的 `translateZ` 由 -8vw 改为 -6vw（场景已绕 X 轴转 80°，局部 Z 轴即地面法线，所以是竖直抬起 2vw），两块投影透明度由 0.3 改为 0.2 并加 `box-shadow: 0 0 20px 10px` 的模糊边缘；`mouseleave` 时复原。投影所在的 `.shadow-scene` 不动，所以磁带与投影分开。待本地运行 `gt_check.py` 截图确认。
- Inter 字体：作者的引用地址是 `css3?family=Inter`，很可能无效，文字回退为系统无衬线字体，与来源相同。

## 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)：只删样板、`spin` 动画与关键帧、5 处 `transition`，没有新增或改写的样式值，内联脚本未改 |
| 残留动画与过渡 | `ground_truth.html` 中已无 `animation`、`transition`、`@keyframes` |
| 静止帧 | 卷轴停在 `spin` 的 `from` 帧 `rotateY(0deg)`，与基础样式相同 |
| 外部资源 | jQuery 3.5.1、prefixfree 1.0.7 在云端浏览器中正常（页面完整渲染）；注释里的两张纹理图片不加载 |

## 待本地补做

运行 [gt_check.py](gt_check.py)：确认 `running_animations`、`nonzero_transitions` 为 0；悬停后 `.cassette-scene` 的 `transform` 变化、两块投影 `opacity` 为 0.2 且有 `box-shadow`，移开后复原；对照悬停截图核对 input 的动效描述。
