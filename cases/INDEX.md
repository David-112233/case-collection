# 案例总览

由 `data_intake/tools/registry.py render-index` 生成，**不要手写**。状态来源是 [registry.csv](registry.csv)。

阶段分布：admitted 25，gt_ready 3，input_draft 4

| 案例 | 档位 | 来源 | 特色 | 阶段 | 处理者 | 更新 | 用户审核 | 备注 |
|---|---|---|---|---|---|---|---|---|
| [case-228-T3](case-228-T3/) | T3 | [RaduBratan__mdPrWmo](https://codepen.io/RaduBratan/pen/mdPrWmo) | iPod Nano、凹屏与滚轮 | input_draft | duet | 2026-11-24 | pending | GT 仅静态自检，渲染自检待本地运行 review_20261124/gt_check.py；input 外观按源码推断，待核对（见 input_problem.md）；档位复核仍为 T3 |
| [case-229-T1](case-229-T1/) | T1 | [fossheim__VweaNYW](https://codepen.io/fossheim/pen/VweaNYW) | 卡西欧键盘、黑白键叠压 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；云端无浏览器，外观由 CSS 推算，截图待本地运行 gt_selfcheck.py |
| [case-230-T1](case-230-T1/) | T1 | [glennphilp__DBLzOW](https://codepen.io/glennphilp/pen/DBLzOW) | 剪纸叠字、倾斜阴影 | input_draft | duet | 2026-11-24 | pending | 等用户审核 GT 与 input；外观由 CSS 推算，截图待本地运行 shot_gt.py |
| [case-231-T3](case-231-T3/) | T3 | [ricardoolivaalonso__ExPpgqG](https://codepen.io/ricardoolivaalonso/pen/ExPpgqG) | 立体收音机、磁带仓与凹槽 | gt_ready | duet | 2026-11-24 | pending | GT 已做（仅静态自检，渲染自检待本地运行 review_20261124/gt_check.py）；档位复核仍为 T3 |
| [case-232-T2](case-232-T2/) | T2 | [Ak-407__MYgKoME](https://codepen.io/Ak-407/pen/MYgKoME) | 折叠卡片、页面折角 | input_draft | duet | 2026-11-24 | pending | input 已由 GT 写出，等用户审核；外观由 CSS 推算待本地渲染核对 |
| [case-233-T2](case-233-T2/) | T2 | [bofengbu__JjvYZoJ](https://codepen.io/bofengbu/pen/JjvYZoJ) | 分层蛋糕、夹心切面 | admitted | duet | 2026-11-24 | pending |  |
| [case-229-T1](case-229-T1/) | T1 | [fossheim__VweaNYW](https://codepen.io/fossheim/pen/VweaNYW) | 卡西欧键盘、黑白键叠压 | admitted | duet | 2026-11-24 | pending |  |
| [case-230-T1](case-230-T1/) | T1 | [glennphilp__DBLzOW](https://codepen.io/glennphilp/pen/DBLzOW) | 剪纸叠字、倾斜阴影 | gt_ready | duet | 2026-11-24 | pending | GT 只删 CodePen 样板；截图自检未做（云端无浏览器），脚本已备 |
| [case-231-T3](case-231-T3/) | T3 | [ricardoolivaalonso__ExPpgqG](https://codepen.io/ricardoolivaalonso/pen/ExPpgqG) | 立体收音机、磁带仓与凹槽 | admitted | duet | 2026-11-24 | pending |  |
| [case-232-T2](case-232-T2/) | T2 | [Ak-407__MYgKoME](https://codepen.io/Ak-407/pen/MYgKoME) | 折叠卡片、页面折角 | admitted | duet | 2026-11-24 | pending |  |
| [case-233-T2](case-233-T2/) | T2 | [bofengbu__JjvYZoJ](https://codepen.io/bofengbu/pen/JjvYZoJ) | 分层蛋糕、夹心切面 | gt_ready | duet | 2026-11-24 | pending | GT 去掉 camera.js（拖拽相机）与自动旋转，保留 How to? 面板；外部 CSS 与 camera.js 被代理拦截未核实，渲染自检待本地运行 review_20261124/gt_check.py |
| [case-234-T1](case-234-T1/) | T1 | [fossheim__xxboBzO](https://codepen.io/fossheim/pen/xxboBzO) | 拍立得、凹面取景器 | admitted | duet | 2026-11-24 | pending | 引用外部 script.js，内容未核验，档位按未见动态暂定 |
| [case-235-T3](case-235-T3/) | T3 | [ricardoolivaalonso__NWJeBPE](https://codepen.io/ricardoolivaalonso/pen/NWJeBPE) | 立体办公室、家具分层 | admitted | duet | 2026-11-24 | pending | WebGL 画布（three.js），非 HTML/CSS 结构，评分可行性待用户确认 |
| [case-236-T3](case-236-T3/) | T3 | [ricardoolivaalonso__QWJxYXE](https://codepen.io/ricardoolivaalonso/pen/QWJxYXE) | Switch机身、按键凹凸 | admitted | duet | 2026-11-24 | pending |  |
| [case-237-T3](case-237-T3/) | T3 | [dustindwayne__bGyYoar](https://codepen.io/dustindwayne/pen/bGyYoar) | 唱片机、正面浮雕 | admitted | duet | 2026-11-24 | pending |  |
| [case-238-T1](case-238-T1/) | T1 | [MadeByArne__bGWwRoX](https://codepen.io/MadeByArne/pen/bGWwRoX) | 磁带窗口、带芯叠层 | admitted | duet | 2026-11-24 | pending |  |
| [case-239-T2](case-239-T2/) | T2 | [RaduBratan__MWyKrRZ](https://codepen.io/RaduBratan/pen/MWyKrRZ) | 立体磁带、卷轴与投影 | admitted | duet | 2026-11-24 | pending |  |
| [case-240-T1](case-240-T1/) | T1 | [shunyadezain__QWyVwep](https://codepen.io/shunyadezain/pen/QWyVwep) | 合成器面板、旋钮浮雕 | admitted | duet | 2026-11-24 | pending |  |
| [case-241-T1](case-241-T1/) | T1 | [meylon__qByaYVp](https://codepen.io/meylon/pen/qByaYVp) | 圆环凹面、错落连线 | admitted | duet | 2026-11-24 | pending |  |
| [case-242-T2](case-242-T2/) | T2 | [zenete__BaMbmqW](https://codepen.io/zenete/pen/BaMbmqW) | 房间吊顶、扇叶遮叠 | admitted | duet | 2026-11-24 | pending |  |
| [case-243-T3](case-243-T3/) | T3 | [alvaromontoro__zxvqodP](https://codepen.io/alvaromontoro/pen/zxvqodP) | 四工位办公室、隔板交错 | admitted | duet | 2026-11-24 | pending |  |
| [case-244-T1](case-244-T1/) | T1 | [kevinleclair1__XJgQrr](https://codepen.io/kevinleclair1/pen/XJgQrr) | 交织五环、前后交替 | admitted | duet | 2026-11-24 | pending |  |
| [case-245-T2](case-245-T2/) | T2 | [HunorMarton__BazeOpE](https://codepen.io/HunorMarton/pen/BazeOpE) | 埃舍尔方块、桥面穿插 | admitted | duet | 2026-11-24 | pending |  |
| [case-246-T1](case-246-T1/) | T1 | [ehckk__WNzGYKy](https://codepen.io/ehckk/pen/WNzGYKy) | 彩虹书架、书脊深度 | admitted | duet | 2026-11-24 | pending |  |
| [case-247-T3](case-247-T3/) | T3 | [jh3y__XWdQBRx](https://codepen.io/jh3y/pen/XWdQBRx) | 立体工作室、室内遮挡 | admitted | duet | 2026-11-24 | pending |  |
| [case-248-T1](case-248-T1/) | T1 | [lynnandtonic__PoZpjOr](https://codepen.io/lynnandtonic/pen/PoZpjOr) | 折痕海报、纸面光影 | admitted | duet | 2026-11-24 | pending |  |
| [case-249-T3](case-249-T3/) | T3 | [ricardoolivaalonso__RwBZMGB](https://codepen.io/ricardoolivaalonso/pen/RwBZMGB) | 开盖随身听、内腔层次 | admitted | duet | 2026-11-24 | pending |  |
| [case-250-T1](case-250-T1/) | T1 | [thebabydino__NLWdwz](https://codepen.io/thebabydino/pen/NLWdwz) | 圆片信息图、编号叠盖 | admitted | duet | 2026-11-24 | pending |  |
| [case-251-T1](case-251-T1/) | T1 | [thebabydino__eQvWLB](https://codepen.io/thebabydino/pen/eQvWLB) | 彩色折纸条、交替折角 | admitted | duet | 2026-11-24 | pending |  |
| [case-252-T1](case-252-T1/) | T1 | [thebabydino__pBmMaJ](https://codepen.io/thebabydino/pen/pBmMaJ) | 斜切编号条、圆标压层 | admitted | duet | 2026-11-24 | pending |  |
| [case-253-T2](case-253-T2/) | T2 | [ykadosh__bGKgxbe](https://codepen.io/ykadosh/pen/bGKgxbe) | 机械键盘、错排立体键帽 | admitted | duet | 2026-11-24 | pending | 档位 T2/T3 有争议（键盘按下瞬时反馈）；React 自 esm.sh 引入 |
| [case-254-T2](case-254-T2/) | T2 | [agathaco__JaGQPr](https://codepen.io/agathaco/pen/JaGQPr) | 夜景灯塔、光束与远山 | admitted | duet | 2026-11-24 | pending |  |
