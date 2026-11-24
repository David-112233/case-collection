"""Admit user-selected candidates into cases/ (dot runs this, only after the user marked the candidate 1).

    python data_intake/tools/admit_case.py KEY --tier T1            # dry run: prints what would be created, writes nothing
    python data_intake/tools/admit_case.py KEY --tier T1 --apply    # really create cases/case-NNN-TX/

Refuses when: the key is not status=selected in ledger/review.csv, pending/<KEY>/ lacks a source file or its hashes
do not match metadata.json, the tier is missing, or the target directory already exists.
Number = highest case number in cases/registry.csv (at least 227) + 1. Tier is fixed at admission and never renamed.
Files created (same set as main-repo case-227): README.md, classification.json, metadata.json, original_srcdoc.html,
source.html, source_original.html. After --apply: registry.csv row, review.csv row updated, pending/<KEY>/ removed.
"""
import csv
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry  # noqa: E402

REPO = registry.REPO
INTAKE = REPO / "data_intake"
PENDING = INTAKE / "pending"
REVIEW = INTAKE / "ledger" / "review.csv"
REVIEW_FIELDS = ["key", "url", "c_id", "agent", "status", "feature", "user_mark", "case_id", "source_location", "note"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_review() -> list[dict]:
    with REVIEW.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_review(rows: list[dict]) -> None:
    with REVIEW.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def plan(key: str, tier: str, review_rows: list[dict], reg_rows: list[dict]) -> dict:
    if not re.fullmatch(r"T[1-6]", tier or ""):
        sys.exit("--tier must be T1..T6")
    row = next((r for r in review_rows if r["key"].lower() == key.lower()), None)
    if not row or row["status"] != "selected":
        sys.exit(f"refused: {key} is not status=selected in ledger/review.csv (status={row['status'] if row else 'missing'})")
    src = PENDING / key
    for name in ("original_srcdoc.html", "source.html", "metadata.json"):
        if not (src / name).is_file():
            sys.exit(f"refused: {src / name} missing")
    meta = json.loads((src / "metadata.json").read_text(encoding="utf-8"))
    if sha(src / "original_srcdoc.html") != meta.get("original_srcdoc_sha256") or sha(src / "source.html") != meta.get("source_html_sha256"):
        sys.exit("refused: source hashes do not match metadata.json")
    number = registry.next_number(reg_rows)
    case_id = f"case-{number:03d}-{tier}"
    target = registry.CASES / case_id
    if target.exists():
        sys.exit(f"refused: {target} already exists")
    return {"row": row, "src": src, "meta": meta, "case_id": case_id, "target": target, "tier": tier}


def build_readme(p: dict, cls: dict) -> str:
    meta, row = p["meta"], p["row"]
    return f"""# {meta.get('title') or p['case_id']}

来源：<{meta.get('url')}>（作者 {meta.get('author')}，CodePen 公开作品，默认 MIT 许可）

当前阶段：`admitted`（入库于 {registry.today()}），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：{row.get('c_id') or '-'}；档位：{p['tier']}（{cls.get('tier_basis', '依据见 classification.json')}）。
- 特色：{row.get('feature') or '-'}

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

待 duet 补：`input.json`、`ground_truth.html`、`rules_drafts/manual_v1/`、GT 自检记录（见 [cases/README.md](../README.md)）。
"""


def apply(p: dict, reg_rows: list[dict], review_rows: list[dict]) -> None:
    src, target, meta, row = p["src"], p["target"], dict(p["meta"]), p["row"]
    target.mkdir(parents=True)
    shutil.copyfile(src / "original_srcdoc.html", target / "original_srcdoc.html")
    shutil.copyfile(src / "source.html", target / "source.html")
    shutil.copyfile(src / ("source_original.html" if (src / "source_original.html").is_file() else "source.html"), target / "source_original.html")
    meta.update(case_id=p["case_id"], review_id=row.get("c_id") or None, admitted_at=registry.today(), admitted_by="admit_case.py")
    meta["source_original_sha256"] = sha(target / "source_original.html")
    (target / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    cls = {}
    if (src / "classification.json").is_file():
        cls = json.loads((src / "classification.json").read_text(encoding="utf-8"))
    cls.update(case_id=p["case_id"], tier=p["tier"])
    cls.setdefault("review_id", row.get("c_id") or None)
    cls.setdefault("spatial_feature", row.get("feature") or None)
    (target / "classification.json").write_text(json.dumps(cls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (target / "README.md").write_text(build_readme(p, cls), encoding="utf-8", newline="\n")
    reg_rows.append({"case_id": p["case_id"], "source_key": row["key"], "tier": p["tier"], "owner": "duet", "stage": "admitted",
                     "updated": registry.today(), "note": "", "user_review": "pending"})
    registry.write(reg_rows)
    row.update(status="admitted", case_id=p["case_id"], source_location=f"cases/{p['case_id']}")
    write_review(review_rows)
    shutil.rmtree(src)


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0].startswith("-") or "--tier" not in args:
        print(__doc__)
        return 2
    key, tier, do_apply = args[0], args[args.index("--tier") + 1], "--apply" in args
    review_rows, reg_rows = read_review(), registry.read()
    p = plan(key, tier, review_rows, reg_rows)
    print(("APPLY" if do_apply else "DRY RUN"), f"{key} -> cases/{p['case_id']}/")
    for name in ("README.md", "classification.json", "metadata.json", "original_srcdoc.html", "source.html", "source_original.html"):
        print("  +", name)
    print(f"  registry.csv: +1 row (stage admitted, owner duet); review.csv: {key} -> admitted; remove pending/{key}/")
    if do_apply:
        apply(p, reg_rows, review_rows)
        registry.render_index()
    else:
        print("nothing written (add --apply to create)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
