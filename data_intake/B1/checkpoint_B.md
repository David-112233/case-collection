# B1 检查点 B：5 例完整案例待审

- 日期：2026-10-18；作者：Claude（人工编写，未调用 API）。
- 顺序：源码 → 渲染实测 → input.json → ground_truth.html → 无头 Chromium（Playwright 1.62）离线自测。
- 状态：**待用户审核**；审核通过后以下哈希即为冻结版本，之后才允许生成模型输出与编写 eval_rules。

| 案例 | input.json SHA-256 | ground_truth.html SHA-256 |
|---|---|---|
| case-211-T4 | `4c3c041966e22e1f1ef1b16c143b970f3dba7474537c4c93451eb01ade8141b7` | `c33832965be640608fe87f0e09aa19697e09d81d7a31c47a084e55eb852e772f` |
| case-212-T4 | `7c8294738d03067ff3d404f21d8fcc84166744f1c802c0b37216d0766620eab8` | `bbf4899dbce9318ee826f22158807517b48debcc1dd0f538070d59fd6c2b61bb` |
| case-213-T1 | `e1419c0aa059d330c5a05e6108b8919e6830eb7944d5085a7d51e14ddd38b200` | `e5fd7abe9c4e1d12cc4c2c5b48b410307401e0e83621dd7d08a1d08df6eaead0` |
| case-214-T4 | `00d5cf7680843a74abe8fbf8ee4488f5ba620a93c38ae6cd669579bd4c801336` | `362121c04def3016886cbf1a16d296e93c72e89d63047f401cb35e06401f9f31` |
| case-217-T1 | `dc39098bfa50e9184e88e9984563989379c199e7e78631075881d6517be8cb82` | `feae209d66671aa28ce77c7eca6bd6d74706a23702f461c728caf830abb72f23` |

## 自测要点

| 案例 | 自测内容 | 结果 |
|---|---|---|
| case-211-T4 | 初始/横切到 Hong Kong/纵切到第 2 张/点击 NO、SE 标签；375px 标题与标签栏不重叠 | 只显示当前国家名称与照片、非当前照片 0.1、图注同步；无外部请求 |
| case-212-T4 | 悬停第 2 张卡片；横向滚动 300px 后吸附；375px 菜单开合两次 | 其余卡片 0.6+模糊、红角滑入；吸附到第 3 张居中；菜单开关与图标切换正常 |
| case-213-T1 | 1280/800/640/480/360 五档宽度测量 | 几何与原作一致（箭头 50px、回缩 100px、斜边 12px、四档版式）；无外部请求 |
| case-214-T4 | 初始/滚动按钮×2/Week Two/Week One | 当前日面板展开、编号上浮、▲指针随当前日平移；Week Two 使 Day 8 居中；最左端左按钮变灰 |
| case-217-T1 | 1280/375 渲染与各体块投影范围测量 | 与原作一致；375px 平台左端超出 32px（input 已允许） |

## 相对来源的改动（均写入 input，不是 GT 自行添加）

- case-211：原主题样式表不可得，配色/尺寸由 input 自定；国旗 emoji 在 Windows Chromium 无字形，改为国家代码 IS/HK/SE/PT/NO；删除浏览器支持提示条与作者笔记弹窗；照片改为按国家着色的占位图。
- case-212：4 张同名“Project Title”改为互不相同的标题；介绍文案去掉实现提示；删除讲解 JS 的说明段；Tailwind/Inter 外链改为内联样式与通用字体。
- case-213：原说明框直接给出实现代码（`article:nth-child(2n){--p:1}`），改为中性文案；外部字体改为通用无衬线。
- case-214：外部图标字体（Material Symbols）改为箭头字符、交通 emoji 和 ▲ 指针；Week Two 改为定位 Day 8 并居中。
- case-217：删除引用真实设计师的署名与社交图标；只描述从该视角可见的体块（背向镜头的窗户不写入）。

## 未完成

- case-215-T4、case-216-T1 尚未编写 input/GT（检查点 B 通过后继续）。
- 5 例均未编写 eval_rules.json，未生成模型输出。
