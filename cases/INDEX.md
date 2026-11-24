# 案例总览

由 `data_intake/tools/registry.py render-index` 生成，**不要手写**。状态来源是 [registry.csv](registry.csv)。

阶段分布：admitted 1，gt_ready 4，input_draft 22

| 案例 | 档位 | 来源 | 特色 | 阶段 | 处理者 | 更新 | 用户审核 | 备注 |
|---|---|---|---|---|---|---|---|---|
| [case-228-T3](case-228-T3/) | T3 | [RaduBratan__mdPrWmo](https://codepen.io/RaduBratan/pen/mdPrWmo) | iPod Nano、凹屏与滚轮 | input_draft | duet | 2026-11-24 | pending | GT 仅静态自检，渲染自检待本地运行 review_20261124/gt_check.py；input 外观按源码推断，待核对（见 input_problem.md）；档位复核仍为 T3 |
| [case-229-T1](case-229-T1/) | T1 | [fossheim__VweaNYW](https://codepen.io/fossheim/pen/VweaNYW) | 卡西欧键盘、黑白键叠压 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；云端无浏览器，外观由 CSS 推算，截图待本地运行 gt_selfcheck.py |
| [case-230-T1](case-230-T1/) | T1 | [glennphilp__DBLzOW](https://codepen.io/glennphilp/pen/DBLzOW) | 剪纸叠字、倾斜阴影 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；外观由 CSS 推算，截图待本地运行 shot_gt.py |
| [case-231-T3](case-231-T3/) | T3 | [ricardoolivaalonso__ExPpgqG](https://codepen.io/ricardoolivaalonso/pen/ExPpgqG) | 立体收音机、磁带仓与凹槽 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；云端无浏览器，外观由 CSS 推算，待本地运行 review_20261124/gt_check.py 核对（见 input_problem.md） |
| [case-232-T2](case-232-T2/) | T2 | [Ak-407__MYgKoME](https://codepen.io/Ak-407/pen/MYgKoME) | 折叠卡片、页面折角 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；外观由 CSS 推算待本地渲染核对 |
| [case-233-T3](case-233-T3/) | T3 | [bofengbu__JjvYZoJ](https://codepen.io/bofengbu/pen/JjvYZoJ) | 分层蛋糕、夹心切面 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；外部 CSS 与 camera.js 未核实，外观由内联 CSS 推算，渲染自检待本地运行 review_20261124/gt_check.py；说明面板留不留待定（删则改 T1），见 input_problem.md |
| [case-234-T1](case-234-T1/) | T1 | [fossheim__xxboBzO](https://codepen.io/fossheim/pen/xxboBzO) | 拍立得、凹面取景器 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；外观由 CSS 推算待本地渲染核对；/script.js 未核验，无交互与 T1 档位待用户确认 |
| [case-235-T1](case-235-T1/) | T1 | [ricardoolivaalonso__NWJeBPE](https://codepen.io/ricardoolivaalonso/pen/NWJeBPE) | 立体办公室、家具分层 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；外观依据目标图与模型投影，待本地渲染核对；交互全删（T1）、屏幕黑底、竖屏裁切待用户确认 |
| [case-236-T1](case-236-T1/) | T1 | [ricardoolivaalonso__QWJxYXE](https://codepen.io/ricardoolivaalonso/pen/QWJxYXE) | Switch机身、按键凹凸 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；已经 raw.githack.com 渲染核对；无交互，已 retier 为 T1 |
| [case-237-T3](case-237-T3/) | T3 | [dustindwayne__bGyYoar](https://codepen.io/dustindwayne/pen/bGyYoar) | 唱片机、正面浮雕 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；默认状态已渲染核对，播放状态按源码推算待本地截图；动态价值主要在唱片旋转，已去掉 |
| [case-238-T1](case-238-T1/) | T1 | [MadeByArne__bGWwRoX](https://codepen.io/MadeByArne/pen/bGWwRoX) | 磁带窗口、带芯叠层 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；已渲染核对；来源本身静态，窄屏会横向滚动，按桌面宽屏写 |
| [case-239-T2](case-239-T2/) | T2 | [RaduBratan__MWyKrRZ](https://codepen.io/RaduBratan/pen/MWyKrRZ) | 立体磁带、卷轴与投影 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；默认状态已渲染核对，悬停按源码推算待本地截图；悬停也改投影，按 T2 判定待确认 |
| [case-240-T1](case-240-T1/) | T1 | [shunyadezain__QWyVwep](https://codepen.io/shunyadezain/pen/QWyVwep) | 合成器面板、旋钮浮雕 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；已经 raw.githack 渲染核对；待定：网格单位写法、字体名（见 input_problem.md） |
| [case-241-T1](case-241-T1/) | T1 | [meylon__qByaYVp](https://codepen.io/meylon/pen/qByaYVp) | 圆环凹面、错落连线 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；已经 raw.githack 渲染核对；待定：992px 以下横排是否写入、像素尺寸（见 input_problem.md） |
| [case-242-T1](case-242-T1/) | T1 | [zenete__BaMbmqW](https://codepen.io/zenete/pen/BaMbmqW) | 房间吊顶、扇叶遮叠 | input_draft | duet | 2026-11-24 | pending | 等用户审核；云端渲染有大块白色缺口，待本地 GPU 复核（见 input_problem.md 第 1 节）；档位已由 T2 改为 T1 |
| [case-243-T1](case-243-T1/) | T1 | [alvaromontoro__zxvqodP](https://codepen.io/alvaromontoro/pen/zxvqodP) | 四工位办公室、隔板交错 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；已经 raw.githack 渲染核对，与来源默认画面一致；待定：删复选框改 T1、画面静止一句、小细节（见 input_problem.md） |
| [case-244-T1](case-244-T1/) | T1 | [kevinleclair1__XJgQrr](https://codepen.io/kevinleclair1/pen/XJgQrr) | 交织五环、前后交替 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；外观已按 raw.githack 截图核对；难度偏低，是否保留待定 |
| [case-245-T1](case-245-T1/) | T1 | [HunorMarton__BazeOpE](https://codepen.io/HunorMarton/pen/BazeOpE) | 埃舍尔方块、桥面穿插 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；外观已按截图核对；花样只能写到类别层，是否可评测待定；删 YouTube 徽标待确认 |
| [case-246-T1](case-246-T1/) | T1 | [ehckk__WNzGYKy](https://codepen.io/ehckk/pen/WNzGYKy) | 彩虹书架、书脊深度 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；外观已按截图核对；地板穿过最下层是来源瑕疵，GT 未改待定 |
| [case-247-T3](case-247-T3/) | T3 | [jh3y__XWdQBRx](https://codepen.io/jh3y/pen/XWdQBRx) | 立体工作室、室内遮挡 | gt_ready | duet | 2026-11-24 | pending | GT 已完成：去掉音乐、椅子旋转和夜灯循环变色，过渡归零；保留灯光与缩放两个开关，待渲染核对 |
| [case-248-T1](case-248-T1/) | T1 | [lynnandtonic__PoZpjOr](https://codepen.io/lynnandtonic/pen/PoZpjOr) | 折痕海报、纸面光影 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；云端浏览器 1280/500 渲染核对通过，图片与重置样式表均加载；档位复核仍为 T1 |
| [case-249-T3](case-249-T3/) | T3 | [ricardoolivaalonso__RwBZMGB](https://codepen.io/ricardoolivaalonso/pen/RwBZMGB) | 开盖随身听、内腔层次 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；云端渲染核对通过（默认态、播放态）；音频播放未核实；播放态结束方式待用户定；档位复核仍为 T3 |
| [case-250-T1](case-250-T1/) | T1 | [thebabydino__NLWdwz](https://codepen.io/thebabydino/pen/NLWdwz) | 圆片信息图、编号叠盖 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；1280/600/500 渲染核对通过；窄屏版式核对中；来源中等宽度文字被切待用户定；档位复核仍为 T1 |
| [case-251-T1](case-251-T1/) | T1 | [thebabydino__eQvWLB](https://codepen.io/thebabydino/pen/eQvWLB) | 彩色折纸条、交替折角 | admitted | duet | 2026-11-24 | pending |  |
| [case-252-T1](case-252-T1/) | T1 | [thebabydino__pBmMaJ](https://codepen.io/thebabydino/pen/pBmMaJ) | 斜切编号条、圆标压层 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；云端浏览器 1280/500 渲染核对通过；档位复核仍为 T1；窄屏版式是否写入 input 待定 |
| [case-253-T2](case-253-T2/) | T2 | [ykadosh__bGKgxbe](https://codepen.io/ykadosh/pen/bGKgxbe) | 机械键盘、错排立体键帽 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；云端浏览器渲染核对通过（按住状态用预览页核对）；档位复核仍为 T2（键盘按键只改键帽自身），待用户确认；音效未写入 input |
| [case-254-T1](case-254-T1/) | T1 | [agathaco__JaGQPr](https://codepen.io/agathaco/pen/JaGQPr) | 夜景灯塔、光束与远山 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；档位由 T2 改为 T1（GT 去掉全部动画，定格来源第 40 秒）；云端浏览器 1280/500 渲染核对通过；作品价值主要在动画，是否仍收录待用户定 |
