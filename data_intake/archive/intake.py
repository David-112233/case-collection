"""Materialise screened B1 pens into cases/ (DEC-032/033/034). Run once per approved batch.

Writes per case: source_original.html (cdpn srcdoc minus CodePen console shim), source.html (JS removed or
replaced by Claude, see js_changes), metadata.json, classification.json. input.json / ground_truth.html are
written later by hand and are NOT derived from source.html.
"""
import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT.parents[1] / "cases"
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>\s*", re.S | re.I)

CONFIRMATION = "batch 2 selection, 2026-10-18"
APPROVED = [  # (key, case number, tier). Done earlier: 211-213 (checkpoint A, raw deleted afterwards)
    ("una__myJOjQx", 214, "T4"),
    ("utilitybend__ZYOKRXV", 215, "T4"),
    ("letsbleachthis__zewKYE", 216, "T1"),
    ("xdesro__dVxpgN", 217, "T1"),
]


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def strip_scripts(html: str) -> str:
    return SCRIPT_RE.sub("", html)


def allanwhite(html: str) -> str:
    html = strip_scripts(html)
    button = re.search(r'<button class="toggle-me[^"]*"[^>]*>(.*?)</button>', html, re.S)
    html = html.replace(
        button.group(0),
        '<input type="checkbox" id="menu-toggle" class="menu-toggle" aria-controls="menu">\n'
        '    <label for="menu-toggle" class="toggle-me flex items-center px-3 py-2 rounded text-blue-400 '
        'hover:border hover:text-black cursor-pointer">' + button.group(1) + "</label>",
    )
    html = re.sub(r"<noscript>(.*?)</noscript>", r"\1", html, flags=re.S)
    html = html.replace("project-list opacity-0", "project-list")
    html = html.replace(
        "</style>",
        "/* B1 JS replacement: checkbox menu state; images shown without lazy-loading */\n"
        ".menu-toggle { position: absolute; opacity: 0; pointer-events: none; }\n"
        ".menu-toggle:checked + .toggle-me { color: black; }\n"
        ".menu-toggle:checked + .toggle-me .icon-default { display: none; }\n"
        ".menu-toggle:checked + .toggle-me .icon-active { display: block; }\n"
        "nav:has(.menu-toggle:checked) .toggle-target { display: block; }\n"
        "nav:has(.menu-toggle:checked) .toggle-target .nav-items a.nav-item { transform: translate3D(0, 0, 0); opacity: 1; }\n"
        ".lozad { opacity: 1; }\n</style>",
        1,
    )
    return html


def letsbleachthis(html: str) -> str:
    html = strip_scripts(html)
    html = re.sub(r"<link[^>]*aos\.css[^>]*>\s*", "", html)
    return re.sub(r'\sdata-aos(?:-[a-z-]+)?="[^"]*"', "", html)


TRANSFORMS = {
    "una__myJOjQx": (strip_scripts, "removed: CodePen loop-guard script and a comment-only pen script"),
    "utilitybend__ZYOKRXV": (strip_scripts, "removed: nothing functional (no scripts present)"),
    "letsbleachthis__zewKYE": (letsbleachthis, "removed: AOS scroll-reveal library, its init call, aos.css link and data-aos attributes (T1 static case; reveal animations are not part of the requirement)"),
    "xdesro__dVxpgN": (strip_scripts, "removed: evil-icons library that only drew three social icons in the credit links, CodePen loop-guard script, comment-only pen script"),
    "HejChristian__azzWVWL": (strip_scripts, "removed: CodePen loop-guard script; click handler that only dismissed the author's lab-notes dialog (not part of the demo)"),
    "allanwhite__oNNbpqx": (allanwhite, "replaced: menu toggle click handler -> hidden checkbox + label with :checked/:has() rules; removed: lozad lazy-loading (noscript <img> unwrapped, hidden-until-loaded opacity removed), CodePen loop-guard script"),
    "thebabydino__gOdPzEK": (strip_scripts, "removed: CodePen loop-guard script and a comment-only pen script"),
}


def main() -> None:
    screening = {r["key"]: r for r in csv.DictReader((ROOT / "screening.csv").open(encoding="utf-8"))}
    for key, number, tier in APPROVED:
        row = screening[key]
        assert row["decision"] == "accept" and row["tier"] == tier, (key, row["decision"], row["tier"])
        target = CASES / f"case-{number:03d}-{tier}"
        assert not any(CASES.glob(f"case-{number:03d}*")) or target.exists(), f"case-{number:03d} taken"
        target.mkdir(exist_ok=True)
        raw = ROOT / "raw" / key
        fetched = json.loads((raw / "metadata.json").read_text(encoding="utf-8"))
        original = (raw / "source.html").read_text(encoding="utf-8")
        transform, change_note = TRANSFORMS[key]
        derived = transform(original)
        (target / "source_original.html").write_text(original, encoding="utf-8")
        (target / "source.html").write_text(derived, encoding="utf-8")
        analysis = fetched["analysis"]
        metadata = {
            "case_id": target.name,
            "batch_id": "DATA-002-B1",
            "source_id": fetched["source_id"],
            "title": fetched["title"],
            "author": fetched["author"],
            "url": fetched["url"],
            "license": fetched["license"],
            "acquisition": fetched["acquisition"],
            "acquisition_url": fetched["acquisition_url"],
            "retrieved_at": fetched["retrieved_at"],
            "original_srcdoc_sha256": fetched["original_srcdoc_sha256"],
            "source_original_sha256": sha(original),
            "source_html_sha256": sha(derived),
            "provenance": "derived" if row["js_policy"] == "replace" else "original_minus_nonfunctional_js",
            "js_policy": row["js_policy"] if row["js_policy"] != "none" else "remove",
            "js_changes": change_note,
            "external_dependencies": {
                "stylesheets": analysis["external_stylesheets"],
                "css_imports": analysis["css_imports"],
                "note": "Reference material only; input.json/ground_truth.html must not load external resources.",
            },
            "intake_date": date.today().isoformat(),
            "decisions": ["DEC-031", "DEC-032", "DEC-033", "DEC-034", "DEC-035"],
        }
        classification = {
            "case_id": target.name,
            "tier": tier,
            "difficulty_features": row["hits"].split(","),
            "evidence": row["evidence"],
            "classifier": "Claude (claude-opus-5-5), manual source reading + browser render; no API",
            "screening_notes": row["notes"],
            "user_confirmation": CONFIRMATION,
            "rules": "difficulty_model_v2_1 T1-T6; DEC-033 thresholds as amended by DEC-035",
        }
        (target / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        (target / "classification.json").write_text(json.dumps(classification, ensure_ascii=False, indent=2), encoding="utf-8")
        print(target.name, metadata["js_policy"], len(derived), "scripts left:", len(SCRIPT_RE.findall(derived)))


if __name__ == "__main__":
    main()

