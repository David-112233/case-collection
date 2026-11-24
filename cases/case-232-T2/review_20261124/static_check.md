# case-232 GT 自检记录（2026-11-24，静态检查）

## 状态：脚本已写好，云端未能运行

`gt_selfcheck.py` 在 1280×900 与 375×812 两个视口下，对 `ground_truth.html` 和 `source.html` 各截默认态与三张卡片逐张悬停态，并测量卡片位置、右半边的变换矩阵与底色、箭头透明度与位移、Bitter 字体是否加载、页面是否横向溢出、是否有运行中的动画，结果写入 `gt_selfcheck.json`。

本次云端会话里 `requirements.txt` 的 playwright 能装，但 Chromium 无法下载（环境把浏览器下载地址设成了不可达，也没有预装浏览器），所以**截图和测量都还没有产生**。在本地运行：

```
pip install -r requirements.txt
python -m playwright install chromium
python cases/case-232-T2/review_20261124/gt_selfcheck.py
```

## 已做的不依赖浏览器的核验

- `ground_truth.html` 与 `source.html` 的差异见 [source_to_gt.diff](source_to_gt.diff)：只有删除，没有新增或改写的样式值。
- GT 中已无 `transition`、`animation`、`@keyframes`，也没有脚本。
- 字体样式表 `https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Bitter:wght@400;700&family=Righteous&display=swap` 在云端返回 200，内含 Bebas Neue、Bitter（400、700）、Righteous 的字体定义。页面只用到 Bitter。Bitter 700 的字体文件（fonts.gstatic.com）在云端也能下载（返回 200）。
- Python html.parser 检查 GT 无未闭合、无错配的标签。

## 按 CSS 推算的版式（未经截图核验）

以下数值由样式规则手算，等截图跑出来后以 `gt_selfcheck.json` 为准。

- `ol` 保留浏览器默认的 40px 左内边距，`body` 四周 80px 内边距；网格列宽 `minmax(280px, 1fr)`、列距 48px，`justify-items: center`；卡片固定 360×120px。
- **1280 宽**：可用宽 1080px，排 3 列、每列 328px，卡片比列宽 32px、两侧各溢出 16px。三张卡片同一行，左边缘约在 x=104、480、856，顶边约 y=96；卡片之间 16px 空隙，正好被下一张卡片向左上偏移 16px 的斜线背板填上。整组中心约在 x=660，比视口中心偏右约 20px。
- **375 宽**：可用宽只有 175px，网格按最小列宽 280px 排成 1 列，三张卡片上下排列（行距 64px），卡片右边缘约到 x=440，**页面横向溢出约 65px**。来源本身就不是响应式的。
- **悬停终态**：右半边以卡片竖直中线为轴 `rotateY(-50deg)`，父级透视 1000px。按矩阵推算，右半边外缘转向观者，投影后外缘约在中线右侧 134px（静止时 180px），外缘高度约 139px（上下各凸出约 10px），呈外侧更高的梯形；底色由白变 #f5f5f5。外缘右侧露出约 46px 宽的浅绿底面，白色箭头（16×16，平时透明）出现并右移 12px，落在这条露出的区域里（距卡片左缘约 332–348px，竖直居中）。左半边不动。
