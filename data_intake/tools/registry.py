"""Case ledger for cases/: stage tracking and the human-readable INDEX.md.

    python data_intake/tools/registry.py render-index
    python data_intake/tools/registry.py set-stage CASE_ID STAGE [--note TEXT]
    python data_intake/tools/registry.py set-owner CASE_ID OWNER
    python data_intake/tools/registry.py set-user-review CASE_ID pending|accepted|rejected --by-user "<the user's own words>"
    python data_intake/tools/registry.py retier CASE_ID T1..T6 [--apply]

Order of work: source.html -> quasi-static ground_truth.html -> input.json (written from the GT) -> user reviews GT and input
-> eval rules -> user reviews rules -> freeze -> sync. Stages (they only move forward):
  admitted -> gt_ready -> input_draft (duet stops, waits for the user) -> input_approved (user only) -> rules_draft
  -> ready_for_review (duet stops, waits for the user) -> frozen -> synced (both local).
Moving backward requires --note with the reason. input_approved needs --by-user "<the user's words>"; frozen and synced need
--local; rules_draft and later cannot be reached before input_approved. user_review may only be changed on the user's
explicit instruction. The tier in the directory name is provisional until the GT exists: retier renames the case directory
and is allowed only while the stage is admitted, gt_ready or input_draft (dry run unless --apply).
"""
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CASES = REPO / "cases"
REGISTRY = CASES / "registry.csv"
FIELDS = ["case_id", "source_key", "tier", "owner", "stage", "updated", "note", "user_review"]
STAGES = ["admitted", "gt_ready", "input_draft", "input_approved", "rules_draft", "ready_for_review", "frozen", "synced"]
LOCAL_ONLY = {"frozen", "synced"}
RETIER_OK = {"admitted", "gt_ready", "input_draft"}
OWNERS = {"duet", "dot", "claude", "codex"}
REVIEWS = {"pending", "accepted", "rejected"}


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def read() -> list[dict]:
    if not REGISTRY.exists():
        return []
    with REGISTRY.open(encoding="utf-8-sig", newline="") as handle:
        return [r for r in csv.DictReader(handle) if r.get("case_id") and r["case_id"] != "case_id"]


def write(rows: list[dict]) -> None:
    rows = sorted(rows, key=lambda r: r["case_id"])
    with REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def next_number(rows: list[dict]) -> int:
    numbers = [int(r["case_id"].split("-")[1]) for r in rows]
    return max(numbers + [227]) + 1


def find(rows: list[dict], case_id: str) -> dict:
    for row in rows:
        if row["case_id"] == case_id:
            return row
    sys.exit(f"unknown case_id {case_id}")


def render_index() -> None:
    rows = read()
    counts = {s: sum(1 for r in rows if r["stage"] == s) for s in STAGES}
    lines = ["# 案例总览", "", "由 `data_intake/tools/registry.py render-index` 生成，**不要手写**。状态来源是 [registry.csv](registry.csv)。", ""]
    if not rows:
        lines.append("暂无案例。")
    else:
        lines.append("阶段分布：" + "，".join(f"{s} {n}" for s, n in counts.items() if n))
        lines += ["", "| 案例 | 档位 | 来源 | 特色 | 阶段 | 处理者 | 更新 | 用户审核 | 备注 |", "|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            meta = {}
            cls = {}
            try:
                meta = json.loads((CASES / r["case_id"] / "metadata.json").read_text(encoding="utf-8"))
                cls = json.loads((CASES / r["case_id"] / "classification.json").read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
            url = meta.get("url") or ""
            link = f"[{r['source_key']}]({url})" if url else r["source_key"]
            feature = (cls.get("spatial_feature") or "").replace("|", "/")
            note = (r["note"] or "").replace("|", "/")
            lines.append(f"| [{r['case_id']}]({r['case_id']}/) | {r['tier']} | {link} | {feature} | {r['stage']} | {r['owner']} | {r['updated']} | {r['user_review']} | {note} |")
    (CASES / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"INDEX.md rendered: {len(rows)} cases")


def retier(rows: list[dict], case_id: str, tier: str, apply: bool) -> None:
    import re
    if not re.fullmatch(r"T[1-6]", tier):
        sys.exit("tier must be T1..T6")
    row = find(rows, case_id)
    if row["stage"] not in RETIER_OK or row["user_review"] == "accepted":
        sys.exit(f"refused: the tier can only change while the stage is {sorted(RETIER_OK)} (now {row['stage']})")
    new_id = re.sub(r"-T\d$", f"-{tier}", case_id)
    if new_id == case_id:
        sys.exit("tier unchanged")
    old_dir, new_dir = CASES / case_id, CASES / new_id
    if new_dir.exists():
        sys.exit(f"refused: {new_dir} already exists")
    print(("APPLY" if apply else "DRY RUN"), f"{case_id} -> {new_id}: rename directory, update registry row, replace the id inside README.md, metadata.json, classification.json")
    if not apply:
        print("nothing written (add --apply)")
        return
    old_dir.rename(new_dir)
    for name in ("README.md", "metadata.json", "classification.json"):
        f = new_dir / name
        if f.exists():
            text = f.read_text(encoding="utf-8").replace(case_id, new_id)
            if name == "README.md":
                text = text.replace(f"档位：{case_id[-2:]}", f"档位：{tier}")
            if name == "classification.json":
                text = text.replace(f'"tier": "{case_id[-2:]}"', f'"tier": "{tier}"')
            f.write_text(text, encoding="utf-8", newline=chr(10))
    row.update(case_id=new_id, tier=tier, updated=today(), note=(row["note"] + f" | 档位由 {case_id[-2:]} 改为 {tier}（按 GT 重新判定）").strip(" |"))
    write(rows)
    render_index()


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    cmd = args[0]
    if cmd == "render-index":
        render_index()
        return 0
    rows = read()
    if cmd == "set-stage" and len(args) >= 3:
        row, new = find(rows, args[1]), args[2]
        if new not in STAGES:
            sys.exit(f"stage must be one of {STAGES}")
        note = args[args.index("--note") + 1] if "--note" in args else ""
        cur_i, new_i, gate = STAGES.index(row["stage"]), STAGES.index(new), STAGES.index("input_approved")
        if new_i < cur_i and not note:
            sys.exit("moving a stage backward needs --note with the reason")
        if new == "input_approved":
            if "--by-user" not in args or not args[args.index("--by-user") + 1].strip():
                sys.exit("input_approved can only be set on the user's explicit instruction: pass --by-user \"<user's words>\"")
            note = (note + " | " if note else "") + "用户通过 GT 与 input：" + args[args.index("--by-user") + 1].strip()
        if new_i > gate and cur_i < gate:
            sys.exit("refused: the user has not approved the GT and input yet (stage input_approved comes first)")
        if new in LOCAL_ONLY and "--local" not in args:
            sys.exit(f"{new} is done locally by the user or Claude: pass --local")
        row.update(stage=new, updated=today())
        if note:
            row["note"] = note
    elif cmd == "retier" and len(args) >= 3:
        retier(rows, args[1], args[2], "--apply" in args)
        return 0
    elif cmd == "set-owner" and len(args) == 3:
        if args[2] not in OWNERS:
            sys.exit(f"owner must be one of {sorted(OWNERS)}")
        row = find(rows, args[1])
        row.update(owner=args[2], updated=today())
    elif cmd == "set-user-review" and len(args) >= 3:
        if args[2] not in REVIEWS:
            sys.exit(f"user_review must be one of {sorted(REVIEWS)}")
        if "--by-user" not in args or not args[args.index("--by-user") + 1].strip():
            sys.exit("user_review can only be changed on the user's explicit instruction: pass --by-user \"<user's words>\"")
        row = find(rows, args[1])
        quote = args[args.index("--by-user") + 1].strip()
        row.update(user_review=args[2], updated=today(), note=f"{row['note']} | 用户：{quote}".strip(" |"))
    else:
        print(__doc__)
        return 2
    write(rows)
    render_index()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
