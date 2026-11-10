"""Record a screening decision (human judgement by Claude) into screening.csv.

decide.py KEY DECISION TIER HITS REASON "EVIDENCE" ["NOTES"] [JS_POLICY]
  DECISION: accept | reject | hold
  TIER: T1..T6 or '-'
  HITS: e.g. H2,H4,H8 or '-'
  REASON: '-' for accept; D0 (single component/decorative/one-rule), D1 (below threshold),
          C1 (DEC-036: common technique, or answer retrievable online), R02 (duplicate of another candidate),
          J1 (JS core, no CSS equivalent), X1 (unusable source / external dependency), T* (other tier, keep for later batch)
  JS_POLICY: none | remove | replace | reject
"""
import csv
import sys
from datetime import date
from pathlib import Path

PATH = Path(__file__).resolve().parent / "screening.csv"
FIELDS = ["key", "url", "decision", "tier", "hits", "reason", "js_policy", "evidence", "notes", "decided_on"]

args = sys.argv[1:]
key, decision, tier, hits, reason, evidence = args[:6]
notes = args[6] if len(args) > 6 else ""
js_policy = args[7] if len(args) > 7 else "none"
assert decision in {"accept", "reject", "hold"}, decision
author, pen = key.split("__", 1)
row = {
    "key": key, "url": f"https://codepen.io/{author}/pen/{pen}", "decision": decision, "tier": tier, "hits": hits,
    "reason": reason, "js_policy": js_policy, "evidence": evidence, "notes": notes, "decided_on": date.today().isoformat(),
}
rows = []
if PATH.exists():
    rows = [r for r in csv.DictReader(PATH.open(encoding="utf-8")) if r["key"] != key]
rows.append(row)
with PATH.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
print(f"{decision} {key} {tier} {hits} {reason}")
