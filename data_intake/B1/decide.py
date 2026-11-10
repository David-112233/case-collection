"""Record a screening decision (human judgement by Claude) into screening.csv.

decide.py KEY DECISION TIER HITS REASON "EVIDENCE" ["NOTES"] [JS_POLICY]
  DECISION: accept | reject | hold
  TIER: T1..T6 or '-'
  HITS: e.g. H2,H4,H8 or '-'
  REASON: '-' for accept; D0 (single component/decorative/one-rule), D1 (below threshold),
          C1 (DEC-036: common technique, or answer retrievable online), R02 (duplicate of another candidate),
          J1 (JS core, no CSS equivalent), X1 (unusable source / external dependency), T* (other tier, keep for later batch)
  JS_POLICY: none | remove | replace | reject

With the environment variable COLLECT_AGENT=<name> the row goes to screening_<name>.csv instead, and the pen
must be claimed by <name> in claims.csv (see claim.py). Without it the legacy screening.csv is used.
"""
import csv
import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENT = os.environ.get("COLLECT_AGENT", "").strip()
PATH = ROOT / (f"screening_{AGENT}.csv" if AGENT else "screening.csv")
FIELDS = ["key", "url", "decision", "tier", "hits", "reason", "js_policy", "evidence", "notes", "decided_on"]

args = sys.argv[1:]
key, decision, tier, hits, reason, evidence = args[:6]
if AGENT:
    owner = None
    if (ROOT / "claims.csv").exists():
        for claimed in csv.DictReader((ROOT / "claims.csv").open(encoding="utf-8-sig", newline="")):
            if (claimed.get("key") or "").lower() == key.lower():
                owner = claimed["agent"]
                break
    if owner != AGENT:
        sys.exit(f"refused: {key} is {'claimed by ' + owner if owner else 'not claimed'}; claim it first (claim.py)")
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
