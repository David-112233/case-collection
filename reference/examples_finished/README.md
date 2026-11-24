# 完成态样板（节选）

两个主仓库案例的**节选文件**，用来看“一个加工完成的案例”里 input、规则草稿和说明长什么样：

- `case-227-T1`：现行规则格式（`semantic-eval-rules/3.0`）的样板，含 `input.json`、`rules_drafts/manual_v1/eval_rules.json`、`review.md`、`README.md`。
- `case-224-T1`：同格式的第二个样板。

这些文件是从主仓库逐字节复制的，**只复制了其中一部分**：GT、截图、评测报告等没有带来，所以 README 里指向它们的链接是断的，属正常。规则格式以 `semantic-eval-rules/3.0` 为准；主仓库里更早的案例用过其他版本，不要照抄。写完规则后用 `python scripts/case_tools/check_rules.py cases/case-NNN-TX` 自检。
