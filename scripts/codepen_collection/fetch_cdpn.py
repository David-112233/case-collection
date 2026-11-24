#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch public CodePen pens via cdpn.io fullpage into a staging pool (DEC-032).

Only acquires and annotates. It never rejects a pen for containing JavaScript
(DEC-034); screening is done by a human reviewer afterwards.

  python scripts/codepen_collection/fetch_cdpn.py --candidates data_intake/B1/candidates.csv --out data_intake/B1/raw
  python scripts/codepen_collection/fetch_cdpn.py --url https://codepen.io/argyleink/pen/gOzPYOj --out data_intake/B1/raw
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from collect_codepen import css_features, js_features  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parents[1]
CASES_DIR = REPO_ROOT / "cases"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) frontend-benchmark-research"
PEN_RE = re.compile(r"codepen\.io/([A-Za-z0-9_-]+)/(?:pen|full|details|debug|embed)/([A-Za-z0-9]+)", re.I)
SRCDOC_RE = re.compile(r'<iframe[^>]*\bid="result"[^>]*\bsrcdoc="(.*?)"', re.S)
CONSOLE_SHIM_RE = re.compile(
    r"<script>\s*window\.console\s*=\s*window\.console\s*\|\|\s*function\(t\)\s*\{\s*\};\s*</script>\s*", re.S
)
SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
INLINE_HANDLER_RE = re.compile(r"\son[a-z]+\s*=", re.I)

EXTRA_CSS_FEATURES = {
    "scroll_snap": r"\bscroll-snap-(?:type|align)\s*:",
    "scroll_state_query": r"scroll-state\s*\(",
    "scroll_marker": r"::scroll-(?:marker|button)",
    "container_query": r"@container\b",
    "subgrid": r"\bsubgrid\b",
    "anchor_positioning": r"\banchor-name\s*:|\bposition-anchor\s*:|\banchor\s*\(",
    "has_selector": r":has\(",
    "checked_selector": r":checked\b",
    "target_selector": r":target\b",
    "at_property": r"@property\b",
    "view_transition": r"view-transition-name\s*:|@view-transition",
    "transform_3d": r"preserve-3d|perspective\s*:|rotate3d|translateZ|rotate[XY]\s*\(",
    "clip_path": r"\bclip-path\s*:",
    "css_counter": r"counter-(?:reset|increment|set)\s*:",
    "media_query": r"@media\b",
}


def pen_key(url: str) -> tuple[str, str] | None:
    match = PEN_RE.search(url)
    return (match.group(1), match.group(2)) if match else None


def existing_case_pens() -> dict[str, str]:
    """Pens already in the project: main-repo index (reference/dedupe_index.csv) plus cases/ added in this repo."""
    seen: dict[str, str] = {}
    index = REPO_ROOT / "reference" / "dedupe_index.csv"
    if index.is_file():
        with index.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                key = pen_key(row.get("source_url") or "")
                if key:
                    seen[f"{key[0]}/{key[1]}".lower()] = row.get("case_id") or "indexed"
    for meta in CASES_DIR.glob("case-*/metadata.json"):
        try:
            url = json.loads(meta.read_text(encoding="utf-8")).get("url") or ""
        except (OSError, json.JSONDecodeError):
            continue
        key = pen_key(url)
        if key:
            seen[f"{key[0]}/{key[1]}".lower()] = meta.parent.name
    return seen


def fetch(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def analyse(doc: str) -> dict[str, Any]:
    scripts = SCRIPT_RE.findall(doc)
    external_scripts = [m.group(1) for m in re.finditer(r"<script\b[^>]*\bsrc=[\"']([^\"']+)", doc, re.I)]
    inline_js = "\n".join(body for attrs, body in scripts if "src=" not in attrs.lower())
    css = "\n".join(STYLE_RE.findall(doc))
    body = doc.split("<body", 1)[-1]
    features = css_features(css)
    features.update({name: bool(re.search(rx, css, re.I)) for name, rx in EXTRA_CSS_FEATURES.items()})
    features["keyframes_count"] = features.get("keyframes_count", 0)
    return {
        "js": {
            "has_js": bool(inline_js.strip() or external_scripts or INLINE_HANDLER_RE.search(body)),
            "inline_js_chars": len(inline_js.strip()),
            "external_scripts": external_scripts,
            "inline_event_handlers": len(INLINE_HANDLER_RE.findall(body)),
            **js_features(inline_js),
        },
        "css": features,
        "external_stylesheets": re.findall(r"<link\b[^>]*rel=[\"']stylesheet[\"'][^>]*href=[\"']([^\"']+)", doc, re.I),
        "css_imports": re.findall(r"@import\s+(?:url\()?[\"']?([^\"');\s]+)", css, re.I),
        "css_chars": len(css),
        "element_count": len(re.findall(r"<[a-zA-Z][a-zA-Z0-9-]*\b", body)),
        "html_chars": len(doc),
    }


def acquire(author: str, pen_id: str, out_dir: Path, extra: dict[str, str]) -> dict[str, Any]:
    fullpage = f"https://cdpn.io/{author}/fullpage/{pen_id}"
    record: dict[str, Any] = {
        "source_id": f"codepen:{author}/{pen_id}".lower(),
        "author": author,
        "pen_id": pen_id,
        "url": f"https://codepen.io/{author}/pen/{pen_id}",
        "acquisition": "cdpn_fullpage",
        "acquisition_url": fullpage,
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "license": "MIT (CodePen public pen default)",
        **{f"candidate_{k}": v for k, v in extra.items() if v},
    }
    page = fetch(fullpage)
    match = SRCDOC_RE.search(page)
    if not match:
        record["fetch_status"] = "no_srcdoc"
        return record
    original = html.unescape(match.group(1))
    cleaned, shim_count = CONSOLE_SHIM_RE.subn("", original)
    title = re.search(r"<title>(.*?)</title>", original, re.S)
    canonical = re.search(r'rel="canonical" href="([^"]+)"', original)
    record.update(
        {
            "fetch_status": "ok",
            "title": html.unescape(title.group(1).strip()) if title else None,
            "canonical_url": canonical.group(1) if canonical else None,
            "codepen_console_shim_removed": shim_count,
            "original_srcdoc_sha256": hashlib.sha256(original.encode("utf-8")).hexdigest(),
            "source_html_sha256": hashlib.sha256(cleaned.encode("utf-8")).hexdigest(),
            "analysis": analyse(cleaned),
        }
    )
    target = out_dir / f"{author}__{pen_id}"
    target.mkdir(parents=True, exist_ok=True)
    (target / "original_srcdoc.html").write_text(original, encoding="utf-8")
    (target / "source.html").write_text(cleaned, encoding="utf-8")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, help="CSV with a 'url' column; other columns are kept")
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--refetch", action="store_true")
    args = parser.parse_args()

    rows: list[dict[str, str]] = [{"url": u} for u in args.url]
    if args.candidates:
        with args.candidates.open(encoding="utf-8-sig", newline="") as handle:
            rows.extend(csv.DictReader(handle))

    args.out.mkdir(parents=True, exist_ok=True)
    log_path = args.out / "fetch_log.jsonl"
    in_cases = existing_case_pens()
    done: set[str] = set()
    summary = {"ok": 0, "skipped_in_cases": 0, "skipped_fetched": 0, "skipped_bad_url": 0, "failed": 0}

    for row in rows:
        key = pen_key(row.get("url", ""))
        if not key:
            summary["skipped_bad_url"] += 1
            continue
        author, pen_id = key
        norm = f"{author}/{pen_id}".lower()
        if norm in done:
            continue
        done.add(norm)
        if norm in in_cases:
            summary["skipped_in_cases"] += 1
            print(f"skip {norm}: already {in_cases[norm]}")
            continue
        target = args.out / f"{author}__{pen_id}"
        if (target / "metadata.json").exists() and not args.refetch:
            summary["skipped_fetched"] += 1
            continue
        extra = {k: v for k, v in row.items() if k != "url"}
        try:
            record = acquire(author, pen_id, args.out, extra)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            record = {"source_id": f"codepen:{norm}", "fetch_status": "error", "error": str(exc)}
        if record.get("fetch_status") == "ok":
            summary["ok"] += 1
            (target / "metadata.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
            js = record["analysis"]["js"]
            print(f"ok   {norm}: {record['title']!r} js={js['has_js']} ({js['inline_js_chars']} chars)")
        else:
            summary["failed"] += 1
            print(f"fail {norm}: {record.get('fetch_status')} {record.get('error', '')}")
        with log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps({k: v for k, v in record.items() if k != "analysis"}, ensure_ascii=False) + "\n")
        time.sleep(args.delay)

    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
