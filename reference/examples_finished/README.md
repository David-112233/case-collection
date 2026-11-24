# 完成态样板：GT → input → 规则

四个主仓库案例的**真实完成件**，逐字节复制，用来看“一个加工完成的案例”长什么样，尤其是 `eval_rules.json` 怎么写。四份规则都是现行格式 `semantic-eval-rules/3.0`，状态都是用户确认过的（217、221、222 为 `USER_CONFIRMED_FROZEN`，227 为 `USER_CONFIRMED_DRAFT`），都能通过 `python scripts/case_tools/check_rules.py reference/examples_finished/case-NNN-TX --rules rules_drafts/manual_vN/eval_rules.json`。

每个样板包含三样东西，对应加工顺序里的三步：

- `ground_truth.html`：参考答案（第一步）；
- `input.json`：由 GT 写出的题目（第二步）；
- `rules_drafts/manual_vN/eval_rules.json` 和 `review.md`：规则与说明（用户通过 input 之后才写）。

| 样板 | 来源作品 | 类型 | 规则规模 | 适合学什么 |
|---|---|---|---|---|
| `case-227-T1` | CSS leaning card effect | 静态，一个卡片效果页 | 7 个 Requirement，72 条 | **最小的完整样板**，先看这个。另附 `gt_selfcheck.py`，是程序条件的 GT 自查脚本 |
| `case-217-T1` | Pure CSS Isometric Towers | 静态，空间关系（等距塔楼插画） | 14 个，53 条 | 空间、朝向、遮挡关系怎么写成可判定的条件；`review.md` 里记着用户的 5 条确认决定 |
| `case-221-T1` | UI Design: Stats Dashboard | 静态，完整网页 | 12 个，95 条 | 完整页面怎么拆；含 1 条**常识条目**（`source: common_sense`，理由写在 `common_sense_reason`） |
| `case-222-T2` | UI Design: Wedding Planning App | 完整网页加简单交互 | 17 个静态 + 2 个动态，140 条 | 多画布的大页面；动态部分只有链接悬停和输入框聚焦，正是“准静态 GT”保留的那类简单交互。另附 GT 自查脚本与结果 |

## 使用时注意

- **这些是别人的案例，只看写法，不要照抄内容。** 条件的数量和粒度取决于你自己的 input：一个可独立失败的事实写一条，不为增加扣分拆细，也不把能独立失败的事实合并。
- **来源引文必须逐字出现在 input 里。** `source_quote` 是 input 的原句，`check_rules.py` 会逐条核对；常识条目（`source: common_sense`）不引 input，但必须写理由，且不得引入新的业务内容或具体样式数值。
- **条件的判定方式分两种：** 能从样式、几何、DOM 直接读出的事实由程序判，定性的交给 Judge。看样板里 `kind`、`decider` 等字段怎么标。
- **`review.md` 里指向 `build_rules.py` 的链接是断的。** 那是主仓库案例里“用一张表生成规则”的辅助脚本，是各案例专用的，这里没带。你可以自己决定怎么生成规则文件，只要最终格式一致并通过自检。
- 主仓库里更早的案例用过其他规则格式（`v5.2-input-draft/1`、`v6-input-draft/1` 等），**不要参照它们**。
- 这四例的 `ground_truth.html` 和 `input.json` 是它们当时的版本。**新案例的 GT 要做成准静态（无动画、只留简单交互），规则只依据 input，不依据 GT。**
