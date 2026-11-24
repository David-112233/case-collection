# case-230 GT 静态核对（2026-11-24）

## 截图与测量：未完成

云端环境装好了 `requirements.txt` 里的 playwright（1.65.2），但浏览器装不上：本环境把 Playwright 的浏览器下载地址设为不可用（`PLAYWRIGHT_DOWNLOAD_HOST` 指向本机关闭端口，并设置了 `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD`），`/opt/pw-browsers` 为空，系统也没有 chromium。没有绕过这个设置。

截图脚本已写好：[shot_gt.py](shot_gt.py)。有浏览器后在仓库根目录运行，会生成 GT 与 source 在 1280、375 两个视口的整页截图和 `measure.json`（每个字母的位置、颜色、字号、字体、两个伪元素的变换和阴影，以及行数、是否横向溢出）。

## 代码层面的核对（替代截图，未经渲染验证）

GT 与 `source.html` 的差别（见 [source_to_gt.diff](source_to_gt.diff)）只在 `<head>` 的 CodePen 样板和 `<body translate="no">`，`<style>` 与 `<body>` 内容逐字相同，所以两者渲染结果应一致。

按样式推算的静止画面（待截图确认）：

- 页面白底，无其他元素。标题 `h1#logo` 水平居中，顶部外边距 6em（h1 字号 32px，约 192px）。
- 五个字母 G、L、E、N、N 各为一个 `span`：蓝色 `#32A8E0`、粗体、字号 8rem（128px）、行高 1em，字体只写了 `Helvetica`（无通用族回退）。
- `::before`：同一字母，文字透明，`skew(0, 3deg)`（以左下角为原点，越往右越低），带 `0 3px 5px rgba(0,0,0,.25)` 的模糊阴影。效果是字母下方一层略向右下倾斜的灰色软影。
- `::after`：同一字母，白到 `#EEE` 的渐变填充（`background-clip: text`），`rotateY(11deg) translate3d(-4px,-2px,-20px) skew(-2deg,-6deg)`，以左下角为原点。父元素没有 `perspective`，所以 `rotateY` 只让字母水平略窄（约 2%），`translateZ` 无可见效果；`skewY(-6deg)` 让字母越往右越高。`z-index: 100` 使它盖在蓝色字母上。
- 合起来：白色字母与白底几乎同色，像一张从页面剪下、以左下角为轴向右上翘起的纸片；它没盖住的蓝色字母露在下边和右边，越往右露得越多，边缘有灰色软影。
- 宽度估算：五个字母加四个空格约 590px。1280 视口一行居中；375 视口放不下，按空格换行，估计为 “G L E” 与 “N N” 两行，不横向溢出。**这是估算，需截图确认。**

## 外部资源

GT 不加载任何外部资源（CodePen 图标与 canonical 链接已删）。`Helvetica` 是本地字体名，不是外部字体：macOS 自带；Windows 一般映射到 Arial；Linux 常由 fontconfig 映射到 Liberation Sans 或 Nimbus Sans。若某环境没有任何映射，会回退到浏览器默认字体（通常是衬线体）。来源如此，GT 未改。

## 交互与动画

无脚本、无 `@keyframes`、无 `transition`、无 `:hover` 等伪类。GT 无需去动画，也没有交互可测。
