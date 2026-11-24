"""Structural self-check of a case's rules draft. It does NOT judge rule quality.

    python scripts/case_tools/check_rules.py cases/case-228-T1 [--rules rules_drafts/manual_v1/eval_rules.json]

Checks: files exist and parse; input_sha256 equals the sha256 of input.json; case_id matches the directory;
requirement / evidence ids are unique and every mandatory evidence has check, kind and source; for evidence with
source=input the source_quote occurs verbatim in the named input fields; common_sense evidence states a reason;
dependency references point to existing evidence. Exit code 0 only when nothing failed (warnings do not fail).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

INPUT_FIELDS = ["business_background", "functional_requirements", "layout_constraints", "motion_constraints", "forbidden"]


def norm(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    case = Path(args[0]).resolve()
    rel = args[args.index("--rules") + 1] if "--rules" in args else "rules_drafts/manual_v1/eval_rules.json"
    errors, warnings = [], []
    input_path, rules_path = case / "input.json", case / rel
    for p in (input_path, rules_path):
        if not p.is_file():
            print(f"FAIL missing file: {p}")
            return 1
    try:
        inp = json.loads(input_path.read_text(encoding="utf-8"))
        rules = json.loads(rules_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL JSON parse error: {exc}")
        return 1

    current = rules.get("schema_version") == "semantic-eval-rules/3.0"
    if not current:
        warnings.append(f"schema_version {rules.get('schema_version')!r} is not the current format 'semantic-eval-rules/3.0'; "
                        "evidence-level checks are downgraded to warnings. Follow reference/examples_finished/ for the current shape.")
    problems = errors if current else warnings

    digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    if rules.get("input_sha256") != digest:
        errors.append(f"input_sha256 mismatch: rules={rules.get('input_sha256')} actual={digest}")
    match = re.match(r"case-(\d+)", case.name)
    if match and rules.get("case_id") not in (case.name, f"case-{match.group(1)}"):
        errors.append(f"case_id {rules.get('case_id')!r} does not match directory {case.name!r}")
    if inp.get("case_id") and match and inp["case_id"] not in (case.name, f"case-{match.group(1)}"):
        warnings.append(f"input.json case_id {inp['case_id']!r} differs from directory name")

    field_text = {k: norm(str(inp.get(k, ""))) for k in INPUT_FIELDS}
    req_ids, evidence_ids, deps = set(), set(), []
    n_req = n_ev = 0
    for dim in ("static_requirements", "dynamic_requirements"):
        for req in rules.get(dim) or []:
            n_req += 1
            rid = req.get("id")
            if not rid or rid in req_ids:
                errors.append(f"{dim}: missing or duplicate requirement id {rid!r}")
            req_ids.add(rid)
            if not req.get("mandatory_evidence"):
                problems.append(f"{rid}: no mandatory_evidence")
            seen_local = set()
            for ev in req.get("mandatory_evidence") or []:
                n_ev += 1
                eid = ev.get("id")
                full = f"{rid}.{eid}"
                if not eid or eid in seen_local:
                    problems.append(f"{rid}: missing or duplicate evidence id {eid!r}")
                seen_local.add(eid)
                evidence_ids.add(full)
                for need in ("check", "kind", "source"):
                    if not ev.get(need):
                        problems.append(f"{full}: missing field {need}")
                src = ev.get("source")
                if src == "input":
                    quote, fields = norm(ev.get("source_quote", "")), ev.get("source_fields") or []
                    if not quote:
                        problems.append(f"{full}: source=input but no source_quote")
                    elif not any(quote in field_text.get(f, "") for f in (fields or INPUT_FIELDS)):
                        problems.append(f"{full}: source_quote not found verbatim in {fields or 'input'}")
                elif src == "common_sense":
                    if not (ev.get("reason") or ev.get("note")):
                        problems.append(f"{full}: common_sense evidence needs a reason")
                elif src not in ("project_output_contract",):
                    warnings.append(f"{full}: unusual source {src!r}")
                for d in ev.get("depends_on") or ev.get("dependencies") or []:
                    deps.append((full, d))
    for owner, dep in deps:
        target = dep if "." in str(dep) else None
        if target and target not in evidence_ids:
            problems.append(f"{owner}: dependency {dep!r} does not exist")
    if not rules.get("quality_gate"):
        warnings.append("no quality_gate list")

    print(f"{case.name}: {n_req} requirements, {n_ev} mandatory evidence, {len(rules.get('quality_gate') or [])} gates")
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("FAIL ", e)
    print("RESULT", "PASS" if not errors else f"FAIL ({len(errors)} problems)")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
