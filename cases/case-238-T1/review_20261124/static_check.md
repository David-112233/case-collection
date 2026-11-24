# case-238 GT 自检记录（2026-11-24）

## 结论

- **已渲染核对。** 按用户同意的方式，用云端浏览器经 raw.githack.com 打开提交 `5a71563` 中的 `ground_truth.html`，在 1280×800 和 500×800 两个视口截图查看。截图不入库。
- 手写字体 Gochi Hand 已加载。1280 宽下磁带在左、歌单卡在右，整体居中，画面与 `input.json` 一致。
- **500 宽下出现横向滚动条：** 两个部件都是固定 550 px 宽，放在两栏网格里，窄视口下磁带超出右边、歌单卡完全在视口外。这是来源本身的布局（GT 未改），所以 input 写了“页面面向桌面宽屏”，没写窄屏要求。

## 已做的检查

| 检查 | 结果 |
|---|---|
| 与来源的差异 | 见 [source_to_gt.diff](source_to_gt.diff)：只删 CodePen 样板 |
| 动态 | 来源与 GT 都没有 `animation`、`transition`、`:hover`、脚本 |
| 外部资源 | Google Fonts 的 Gochi Hand，云端浏览器中加载成功 |

## 本地可补做

运行 [gt_check.py](gt_check.py) 得到两个视口的截图、整页截图和各部件包围盒。
