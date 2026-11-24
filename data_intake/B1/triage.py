"""Summarise fetched B1 candidates into triage.csv (read-only helper; no decisions)."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
tiers = {}
for path in sorted(ROOT.glob("candidates*.csv")):
    if path.exists():
        for row in csv.DictReader(path.open(encoding="utf-8-sig")):
            m = re.search(r"codepen\.io/([^/]+)/pen/([^/?#]+)", row["url"])
            if m:
                tiers[f"{m.group(1)}__{m.group(2)}"] = row.get("target_tier") or "?"

FLAGS = ["scroll_snap", "scroll_state_query", "scroll_marker", "container_query", "subgrid", "anchor_positioning",
         "has_selector", "checked_selector", "target_selector", "at_property", "view_transition", "transform_3d",
         "clip_path", "css_counter", "media_query", "has_animation_timeline"]
rows = []
for meta_path in sorted((ROOT / "raw").glob("*/metadata.json")):
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    src = (meta_path.parent / "source.html").read_text(encoding="utf-8")
    a = meta["analysis"]
    rows.append({
        "key": meta_path.parent.name,
        "target": tiers.get(meta_path.parent.name, "?"),
        "title": (meta.get("title") or "")[:60],
        "js_chars": a["js"]["inline_js_chars"],
        "ext_js": len(a["js"]["external_scripts"]),
        "css_chars": a["css_chars"],
        "elements": a["element_count"],
        "keyframes": a["css"]["keyframes_count"],
        "hover": len(re.findall(r":hover", src)),
        "ext_css": len(a["external_stylesheets"]) + len(a["css_imports"]),
        "features": " ".join(f for f in FLAGS if a["css"].get(f)),
    })
with (ROOT / "triage.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
for r in rows:
    print("|".join(str(v) for v in r.values()))

