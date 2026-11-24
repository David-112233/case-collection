# 通用输出契约 v2

用户于 2026-11-16 确认放开 JavaScript、外部字体和图片（DEC-048）。这是新案例和新轮次的通用政策，不是 case-213 的特例；既有冻结版本及结果保持原样。

| 内容 | 通用约定 |
|---|---|
| JavaScript | 允许内嵌脚本和事件处理属性；仍交付单文件，不依赖外部脚本文件 |
| 图片 | 允许外部图片；若某题明确要求字符、SVG 或其他内容，仍按该题要求 |
| 字体 | 允许外部字体及字体加载样式表；input 指定的字体须实际应用 |
| CSS | 页面样式可写在 head/style 内或 HTML 元素的 style 属性中；字体样式表可外链，不开放外部页面 CSS 框架 |
| 链接 | 允许普通导航链接，不把 href 当外部素材违规 |
| 动效 | 是否有动画/交互、是否要求纯 CSS，由案例 input 及明确范围决定，不是所有题都禁止动画 |
| 故障 | 评测网络、环境、采证故障或原因不明为 UNRESOLVED；不可一律算模型 FAIL |
| 计分 | DEC-038 不变：mandatory Evidence 按严重度扣分，未决不发布正式分 |

机器可读契约：[output_contract_v2.json](../schemas/output_contract_v2.json)。新准备政策：[evaluation_policy_v2.json](../schemas/evaluation_policy_v2.json)。生成模板：output_prompt_v2.txt。旧政策和旧模板保留为历史文件。2026-11-17 已完成 v2 执行器接入及定向测试；每个案例仍须完成执行冻结与完整 GT 自测，不能把通用接入测试当作正式发布资格。

## 文件责任边界

- 通用文件：本规范、机器契约、通用准备政策、Prompt 模板、共享编译/运行代码。不写案例文案、颜色、字体名、断点或目标选择器。
- 案例文件：`cases/case-NNN-TX/input.json`、`ground_truth.html`、`rules_drafts/manual_vN/`、`versions/v旧/`。保存该题要求、来源、审核状态；案例标识可由目录与规则元数据提供，不必改写用户原始 input。
- 轮次公共文件：`evaluations/RNN_<日期>_<轮次主题>/config/`、`round.json`、`generation/prompt.txt`。固定该轮统一政策、Judge 和生成约定；轮次名不绑定首个案例，后续可加入其他案例。
- 轮次案例文件：该轮 `cases/case-NNN-TX/` 下保存源快照、outputs、evaluation/preparation、evaluation/runtime。后续案例各用自己的目录，不复制首例业务内容。

建轮工具只提取已声明的通用配置字段，不把源案例的 case_id、gate_runtime、dependency_bindings 或案例采分批表复制到公共 config；被排除的字段名记入 round.json，Judge 模板以 PREPARING/disabled 开始。

新增案例先确定当前 input/GT/规则版本，再复制到轮次。不得让旧 preparation 内的 manual_rules_path 覆盖新规则选择；旧参数、选择器、冻结记录必须按新来源重新核验。允许共享脚本，不能直接共享案例条件或 GT 绑定。

## 接入到正式运行前

准备配置通过 `policy_path`、`output_contract_path` 显式绑定本轮快照，执行 release 保存路径与哈希；GT、采证与门禁使用相同政策。旧契约保留旧限制，v2 开启 JS 与允许的资源。页面外链 CSS 依据完整样式表内容分类，不能只凭字体服务域名放行；资源或分类证据不足记 UNRESOLVED。HTML style 属性及 favicon 图片均在允许范围。正式发布仍要求合成测试与当前案例完整 GT 自测通过。

允许并行准备与生成时，先冻结 input、规则、生成模板、输出契约及 Judge 提示词；生成保存独立语义冻结、原始响应和逐次费用账本。执行材料完成后再冻结 release，以 `semantic-first-generation/1.0` 来源链绑定输出，不伪称生成前已有完整执行包。案例示例见 R02 结构与执行记录。

外部字体/图片需要保存请求及加载结果、实际字形与页面稳定性证据；不因网络失败把模型扣分，也不通过删掉 input 文字或改 GT 来适配环境。审核、冻结、生成、评分仍是不同阶段。
