"""Record a screening decision into this batch's screening.csv (data_intake/batches/<batch>/screening.csv).

decide.py KEY DECISION TIER HITS REASON "EVIDENCE" ["NOTES"] [JS_POLICY]
  DECISION: accept | reject | hold
  TIER: T1..T6 or '-'
  HITS: e.g. H2,H4,H8 or '-'
  REASON: '-' for accept; D0 (single component/decorative/one-rule), D1 (below threshold),
          C1 (DEC-036: common technique, or answer retrievable online), R02 (duplicate of another candidate),
          J1 (JS core, no CSS equivalent), X1 (unusable source / external dependency), T* (other tier, keep for later batch)
  JS_POLICY: none | remove | replace | reject

Required: COLLECT_AGENT=<name>. The pen must be claimed by <name> in ledger/claims.csv (see claim.py).
Optional: COLLECT_BATCH=<YYYYMMDD>_<name>_<NN> (default: today UTC, batch 01).
"""
import csv
import os
import sys
from datetime import date
from pathlib import Path

from datetime import datetime, timezone

INTAKE = Path(__file__).resolve().parents[1]
AGENT = os.environ.get("COLLECT_AGENT", "").strip()
if not AGENT:
    sys.exit("set COLLECT_AGENT=<your name> first (dot or duet)")
BATCH = os.environ.get("COLLECT_BATCH", "").strip() or f"{datetime.now(timezone.utc):%Y%m%d}_{AGENT}_01"
(INTAKE / "batches" / BATCH).mkdir(parents=True, exist_ok=True)
PATH = INTAKE / "batches" / BATCH / "screening.csv"
FIELDS = ["key", "url", "decision", "tier", "hits", "reason", "js_policy", "evidence", "notes", "decided_on"]

args = sys.argv[1:]
key, decision, tier, hits, reason, evidence = args[:6]
if AGENT:
    owner = None
    if (INTAKE / "ledger" / "claims.csv").exists():
        for claimed in csv.DictReader((INTAKE / "ledger" / "claims.csv").open(encoding="utf-8-sig", newline="")):
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
