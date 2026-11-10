"""Claim candidates for one collector so two agents never judge the same pen (first come, first served).

claim.py AGENT CANDIDATES.csv   append unclaimed pens from the file to claims.csv, report the rest
claim.py --owned AGENT          print a CSV (url column) of pens AGENT owns; feed it to fetch_cdpn.py
claim.py --check                list pens claimed more than once and who keeps them

claims.csv is append-only. The earliest line for a pen wins; later lines for the same pen are ignored.
"""
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLAIMS = ROOT / "claims.csv"
CASES = ROOT.parents[1] / "cases"
FIELDS = ["key", "url", "agent", "claimed_at", "source_file"]
PEN_RE = re.compile(r"codepen\.io/([A-Za-z0-9_-]+)/(?:pen|full|details|debug|embed)/([A-Za-z0-9]+)", re.I)


def key_of(url: str) -> str | None:
    match = PEN_RE.search(url or "")
    return f"{match.group(1)}__{match.group(2)}" if match else None


def read_claims() -> list[dict]:
    if not CLAIMS.exists():
        return []
    with CLAIMS.open(encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.DictReader(handle) if row.get("key") and row["key"] != "key"]


def owners(rows: list[dict]) -> dict[str, dict]:
    first: dict[str, dict] = {}
    for row in rows:
        first.setdefault(row["key"].lower(), row)
    return first


def already_judged() -> dict[str, str]:
    seen: dict[str, str] = {}
    for path in sorted(ROOT.glob("screening*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                seen.setdefault(row["key"].lower(), f"{path.name}:{row['decision']}")
    for meta in CASES.glob("case-*/metadata.json"):
        try:
            key = key_of(json.loads(meta.read_text(encoding="utf-8")).get("url") or "")
        except (OSError, json.JSONDecodeError):
            continue
        if key:
            seen[key.lower()] = f"in {meta.parent.name}"
    return seen


def claim(agent: str, source: Path) -> int:
    rows = read_claims()
    owned = owners(rows)
    judged = already_judged()
    with source.open(encoding="utf-8-sig", newline="") as handle:
        candidates = list(csv.DictReader(handle))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new, skipped = [], []
    for row in candidates:
        key = key_of(row.get("url", ""))
        if not key:
            skipped.append((row.get("url", ""), "not a pen url"))
        elif key.lower() in judged:
            skipped.append((key, judged[key.lower()]))
        elif key.lower() in owned:
            holder = owned[key.lower()]["agent"]
            skipped.append((key, "already yours" if holder == agent else f"claimed by {holder}"))
        else:
            entry = {"key": key, "url": f"https://codepen.io/{key.replace('__', '/pen/', 1)}", "agent": agent,
                     "claimed_at": now, "source_file": source.name}
            owned[key.lower()] = entry
            new.append(entry)
    write_header = not CLAIMS.exists() or CLAIMS.stat().st_size == 0
    with CLAIMS.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        if write_header:
            writer.writeheader()
        writer.writerows(new)
    for key, why in skipped:
        print(f"skip  {key}: {why}")
    print(f"claimed {len(new)} for {agent}; skipped {len(skipped)}")
    return 0


def owned_by(agent: str) -> int:
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["url"])
    for row in owners(read_claims()).values():
        if row["agent"] == agent:
            writer.writerow([row["url"]])
    return 0


def check() -> int:
    rows = read_claims()
    keep = owners(rows)
    lost = [row for row in rows if keep[row["key"].lower()] is not row and keep[row["key"].lower()]["agent"] != row["agent"]]
    for row in lost:
        print(f"{row['key']}: kept by {keep[row['key'].lower()]['agent']}, {row['agent']} must drop it")
    print(f"{len(keep)} pens claimed, {len(lost)} double claims")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if args == ["--check"]:
        return check()
    if len(args) == 2 and args[0] == "--owned":
        return owned_by(args[1])
    if len(args) == 2 and not args[0].startswith("-"):
        return claim(args[0], Path(args[1]))
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
