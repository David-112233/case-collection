# 评测流程 v6：从规则到出分

- 生效：2026-10-18（DEC-038），计分政策版本 `evidence-severity/1.0`
- 来源：用户与 Codex 商定的 16 步链路（全文与执行记录见 EVAL-PIPELINE-HANDOFF-20261003），去掉第 8 步中的人工一致性验证和外观评分后形成。该交接文件是历史记录，里面的旧公式、外观分和 DEC-030 实验权重**不属于本流程**。
- 计分细节：[评分细则 v6](scoring_rubric_v6.md)。任务输入输出：[任务定义 v5.2](TASK_DEFINITION_v5_2_synced.md)。

## 一、总原则

新案例与新轮次的实现范围按 [输出契约 v2](output_contract_v2.md)（DEC-048），允许 JS、外部字体、图片和 HTML style 属性。通用新政策为 `scripts/eval_rules_generation/preparation/evaluation_policy_v2.json`，原 `evaluation_policy.json` 保留历史受限版本；计分公式相同。2026-11-17 已接入并定向验证新版 JS/网络策略，准备配置须显式绑定本轮 policy/contract；通用测试通过不等于具体案例可发布，仍需完整 GT 自测和当前执行包验证。

1. **计分单位是 Evidence。** 规则中的每条 mandatory 条件是一条 Evidence，单独判 PASS / FAIL / UNRESOLVED；FAIL 按轻 0.5、中 1、重 1.5 扣分。Requirement 只负责组织条件和报告小计，不再是扣分单位。
2. **出分公式：** `D = max(0, 10 − Σ 该维度失败 Evidence 扣分)`；`Final = max(0, 0.5·D1 + 0.5·D2 − 2 × 独立普通门禁违规数)`。缺一个维度时另一维度占 100%；致命门禁（G1）计 0。
3. **评测器不确定就记未决。** 缺证据、采证失败、定位失败、API 失败或原因不明一律 UNRESOLVED，不扣分；有 mandatory 未决或未判档的 FAIL 时不发布正式分，只出诊断分。
4. **同一事实只扣一次。** 门禁与 Evidence 之间、不同 Evidence 之间重复的，记 0 并写明扣在哪一条。DEC-029 依赖阻断照旧：已确认的上游模型失败实际阻断下游条件时，下游判 FAIL，各按自己的 Evidence 扣分。
5. **先冻结，后生成。** 规则、政策和 Judge 配置冻结后才生成被测输出；看到输出后不改条件、不调严重度、不修补 HTML。
6. **不在当前流程：** Judge 与人工的一致性验证、外观评分。两者都是后续工作；外观分不计入总分。
7. **旧公式已退役。** 不再计算“每条失败 Requirement 扣 2 分”，也不把它作为对照列。历史结果原样保留，不重算。

## 二、角色

| 阶段 | 谁做 | 不能做什么 |
|---|---|---|
| 准备（步骤 1–7、9） | 用户、Codex、Claude、程序、API | 不读被测模型输出；不从 GT 反推要求 |
| 正式运行（步骤 10–16） | 程序 + 已冻结配置的 Judge | Codex / Claude 不手工改判、不修补输出 |
| 审核与验收 | 用户 | 执行者不得自写 accepted |

Judge 的来源（程序谓词、API 模型名、或 Claude 判定）必须写入运行记录。同一批次里各模型使用同一种 Judge，否则结果不能直接比较。当前正式运行器实现的是“程序谓词 + API Judge”；由 Claude 逐条判定（DEC-030 后期的做法，见 `runtime/experiment/claude_judge/`）尚未接入运行器，只能产出注明来源的诊断分。

## 三、准备阶段

| 步骤 | 做什么 | 主要产物 | 要点 |
|---|---|---|---|
| 1. 接收并核对规则 | 核对 input 与已修订规则的对应、覆盖和归因 | `rules_drafts/manual_vN/eval_rules.json` | Requirement 来源是 input 加基本常识（DEC-037）。**条件就是扣分单位**：一个可独立失败的事实写一条，不为增加扣分拆细，也不把独立事实合并 |
| 2. 固定环境与政策 | 浏览器、视口、字体、网络、容差、门禁、计分政策 | `scripts/eval_rules_generation/preparation/evaluation_policy_v2.json`（新版本） | 计分口径只来自所冻结政策的 `scoring_policy`；案例规则里的 `scoring` 块是历史字段，不参与计分 |
| 3. Evidence 可执行化 | 每条 Evidence 写明目标、属性、预期、谓词、容差、状态及程序 / Judge 路线 | `evaluation_preparation/vN/compiled_eval_rules.json` | 能从样式、几何、DOM 读出的事实优先走程序谓词；不能自动判的条件保留，不删除 |
| 4. 目标描述与采样计划 | 分开“找谁”和“查什么”；规定状态、截图、交互 | `target_registry.json`、`acquisition_plan.json` | 保留实际顺序、多余对象和歧义，不先筛出“正确答案” |
| 5. GT 锚点绑定 | 把逻辑目标绑到 GT 对象，保存参考特征 | `gt_binding_spec.json`、`gt_reference.json`、参考截图 | GT 选择器不能当模型选择器；GT 外观不能变成新要求 |
| 6. 共享执行能力 | 浏览器会话、目标匹配、采证、判定、判档、门禁、聚合 | `scripts/eval_rules_generation/runtime/` | 只支持明确列举的模式，遇到边界输出未决 |
| 7. GT 自检与反例 | 在冻结条件下跑 GT；用合成页面检查错误能被识别、合法替代实现能通过 | `preparation_validation.json`、`validation/` | GT 应接近满分；自检不通过要先查规则或评测器，不改分 |
| 8. Judge 协议 | 固定 Judge 模型、提示词、输出契约、重试和未决处理 | `judge_config.json`、`judge_prompt.txt` | 只固定协议并冻结；与人工的一致性验证不在当前流程 |
| 9. 冻结评测包 | 规则、政策、锚点、采样计划、执行器和 Judge 配置组成一个版本 | `releases/<name>.json`、案例 `FREEZE*.json` | 冻结之后才生成被测输出；任何变更都要冻结新包 |

## 四、正式运行

| 步骤 | 做什么 | 运行产物 | 要点 |
|---|---|---|---|
| 10. 接收与预检 | 保存原始 HTML，核对案例、input、Prompt、模型和评测版本 | `subject_manifest.json`、`run_manifest.json`、`original.html` | 版本不匹配就拒绝运行，结构化记录失败阶段 |
| 11. Quality Gate | 判 G1–G5 | `gate_results.json` | G1 失败终止评分并计 0；普通门禁每条独立违规扣 2；与 Evidence 同一事实时只保留记录不扣分 |
| 12. 目标映射 | 枚举模型页面候选，与 GT 参考特征匹配，必要时 API 消歧 | `target_bindings.json` | 区分真实缺失和定位失败；定位失败是 UNRESOLVED |
| 13. 独立采证 | 按采样计划做静态测量、交互、时间采样 | `collection-NN/evidence_package.json`、PNG | 只采证据、不下结论；补采用新目录，保留前次记录 |
| 14. Evidence 判定 | 程序谓词判明确事实；Judge 判定性条件 | `evidence_verdicts.json`、`judge/` | Judge 只判当前条件，不新增要求、不改容差、不用推测补事实 |
| 14b. 严重度判档 | 对每条已确认 FAIL 的 Evidence 判轻 / 中 / 重 | `severity/severity_results.json` | 只依据该条的失败事实；材料不足记 UNRESOLVED，不默认中档；不改 PASS/FAIL；文字截断类按评分细则 §6.2.1 锚点（DEC-046） |
| 15. 聚合与归因 | 合并依赖阻断、门禁去重、Evidence 之间去重、Requirement 小计 | `requirement_results.json`、`attribution.json` | 未决与已确认 FAIL 分别保留，不互相掩盖 |
| 16. 计分与发布 | 按第一节公式算 D1、D2、Final，判断能否正式发布 | `score_result.json` | 条件齐备才有 `formal_score`；否则只有诊断分，并列出未决清单 |

## 五、运行入口

仓库根目录，PowerShell 先设 `$env:PYTHONUTF8='1'`：

```powershell
# 冻结评测包（步骤 9）
.\.venv\Scripts\python.exe -B -m scripts.eval_rules_generation.runtime.release --case <case目录> --preparation <case目录>/evaluation_preparation/vN --runtime <case目录>/evaluation_runtime --out <case目录>/evaluation_runtime/releases/<name>.json

# GT 自检（步骤 7）
.\.venv\Scripts\python.exe -B -m scripts.eval_rules_generation.runtime.evaluate --release <release.json> --gt-diagnostic --out <新目录>

# 被测输出评分（步骤 10–16）
.\.venv\Scripts\python.exe -B -m scripts.eval_rules_generation.runtime.evaluate --release <release.json> --subject-manifest <subject_manifest.json> --out <新目录>
```

每次运行使用新目录。旧的发布包绑定的是旧代码和旧政策的哈希，政策或代码更新后需要重新冻结发布包。按轮次组织的目录与命令见第七节。

案例专用的付费包装器、响应缓存等执行支持代码，也必须绑定到执行包：在该案例的 `runtime_config.json` 中用可选 `execution_support_paths` 列出仓库相对路径，发布器将其纳入哈希并拒绝越界或重复路径。通用发布器负责校验，案例配置负责声明自己的支持文件；不要把某轮模型、预算或缓存索引写成通用科研政策。历史响应复用必须核对完整请求、模型与配置来源、图片字节和原账本，并重新执行当前答案验证，不能直接搬用旧判定或重复记账。

### 2026-10-20：已有冻结输出接入（用户授权）

既有输出允许在**语义需求和规则已于生成前冻结、且原始生成记录可核验**的条件下，接入后来准备的可执行评测包。原始 `FREEZE_v2.json`、input、GT、manual规则与模型HTML均不修改。语义冻结时间、真实API生成时间、可执行评测包冻结时间分别记录；不得倒填时间或宣称执行器/Judge在生成前已经冻结。

`runtime.provenance` 为此生成独立的 `subject-manifest/1.1`：核验批次保存的冻结记录、input/规则快照、Prompt模板、原始API响应、选用清单及输出一致性。`evaluation_bundle_id` 表示本次执行包，不冒充生成时的 `rules_bundle_id`。原有“先冻结完整执行包再生成”的manifest入口继续执行其原校验。

```powershell
.\.venv\Scripts\python.exe -B -m scripts.eval_rules_generation.runtime.provenance --release <release.json> --batch evaluations/R01_20261020_48x8/generation/batches/generation_v2_24_20261020 --model deepseek-v4-pro-0813 --out <新subject_manifest.json>
```

当前适配器支持该批 `generation_summary.json` 已记录的DeepSeek Pro/Qwen输出；其他账本形状须先增加同等来源验证，不能直接拼接字段跳过核验。

新发布包使用 `evaluation-release/1.1` 与 `v6/2026-10-20` 发布政策：保留来源完整性、技术验证、完整GT自检门槛；不把人工一致性或科研accepted作为本轮程序出分的必要条件，也不生成它们已通过的声明。旧1.0包仍按其旧门槛解释。运行时所有mandatory、门禁及严重度未决仍阻止正式发布。

GT通过记录由 `runtime.validation_record` 从实际运行生成，并复核同bundle的 `run_manifest.json`、`evidence_verdicts.json` 与 `score_result.json`：完整执行且来源复查通过、真实GT身份、全mandatory覆盖且无失败/未决、门禁通过。仅手写 `gt_status: PASS` 不再能让新包进入READY。使用 `gt_reference_diagnostic` 的GT自检只证明已绑定GT上的采证/判定；模型定位器能力须由独立技术测试与模型实际定位记录证明，模型运行禁止使用GT选择器。

```powershell
.\.venv\Scripts\python.exe -B -m scripts.eval_rules_generation.runtime.validation_record --gt-run <完整GT运行目录> --technical-record <技术测试记录.json> --out <新validation.json>
```

**2026-10-18 切换口径后的必做步骤：** 中央政策已改为 `evidence-severity/1.0`，各案例现有的 `compiled_eval_rules.json`、`acquisition_spec.json`、`acquisition_plan.json` 都是旧政策下生成的。冻结时程序会重新编译并比对，发现不一致就报“stale”。所以任何案例在下次评分前，都要先重跑准备步骤 3–5（各案例 `evaluation_preparation/vN/` 下的 `build_*` 入口，或多案例 `preparation/multi_case/run.py`），再重新冻结发布包。这一步只更新编译产物里的计分口径，不改变 Requirement 和条件。

## 六、不要使用的旧入口

以下只用于复现历史结果，清单见 archive/legacy_requirement_scoring：

- `scripts/eval_rules_generation/aggregate_requirement_scores.py`、`run_complete_case_scoring.py`、`case004_evaluate.py` 及 pilot56 系列脚本；
- `scripts/case135_rebuild/`、`scripts/case156_rebuild/`（已移入 `archive/small_scale_evals/2026-09_pilot56/scripts/`）；
- `docs/scoring_rubric_v5_2.md` 及更早的评分细则；
- 已归档的 `temporary-scoring` 技能。

## 七、按轮次组织（2026-11-03 起）

每轮评测一个文件夹 `evaluations/<轮次>/`，本轮的输入、生成记录、模型输出、准备产物、发布包、运行记录和汇总都放在里面；`cases/` 只存数据源。目录结构和规则见 evaluations/README。2026-10-20 的 48×8 批次已整体移入 R01_20261020_48x8。

一轮的步骤（仓库根目录，PowerShell，先设 `$env:PYTHONUTF8='1'`）：

```powershell
# 1. 建轮：复制 input/GT/规则和上一轮准备脚本（路径改到本轮），复制统一 Judge 模板
.\.venv\Scripts\python.exe -B -m scripts.evaluation_rounds.make_round --id R<序号>_<YYYYMMDD>_<简称> --cases <案例...> --models <模型...> --from-round <上一轮，如 R01_20261020_48x8> --config-from <Judge 模板所在目录；上一轮有 config/ 时可省略> --purpose "<目的>"

# 2. 在 evaluations/<轮次>/cases/<case>/evaluation/preparation/ 重跑准备脚本（步骤 3–5），然后冻结（步骤 9）
.\.venv\Scripts\python.exe -B -m scripts.eval_rules_generation.runtime.release --case evaluations/<轮次>/cases/<case> --preparation evaluations/<轮次>/cases/<case>/evaluation/preparation --runtime evaluations/<轮次>/cases/<case>/evaluation/runtime --out evaluations/<轮次>/cases/<case>/evaluation/runtime/releases/<name>.json

# 3. 在 round.json 的 cases.<case>.release 填 <name> 后生成；输出、subject manifest、用量和原始响应都写进本轮
.\.venv\Scripts\python.exe -B scripts/model_output_generation/generate_<model>_output.py <案例...> --round evaluations/<轮次>

# 4. GT 自检与被测输出评分，每次运行一个新目录
.\.venv\Scripts\python.exe -B -m scripts.eval_rules_generation.runtime.evaluate --release <release.json> --subject-manifest evaluations/<轮次>/cases/<case>/outputs/<model>.subject.json --out evaluations/<轮次>/cases/<case>/evaluation/runtime/runs/<model>_01
```

`make_round` 打印的 `manual_fix_needed` 列出脚本里没能自动改写的路径，须先人工改好；`warnings` 列出没有可复制准备材料的案例和规则与 input 版本不一致的案例。`--round` 目前只接入百炼的八个模型（`bailian_generation.py`）；Claude 与 Muse 的生成脚本仍写案例根目录。
