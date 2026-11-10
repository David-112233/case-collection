#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert locally exported CodePen ZIP files into benchmark case folders."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_EXPORTS = SCRIPT_DIR / "exports"
DEFAULT_CASES = REPO_ROOT / "cases"
DEFAULT_SUMMARY = DEFAULT_CASES / "codepen_cases_summary.csv"

CODEPEN_URL_RE = re.compile(
    r"https?://(?:www\.)?codepen\.io/(?:editor/)?([^/\s?#]+)/pen/([^/\s?#)\]>'\"]+)",
    re.I,
)
STYLE_EXTENSIONS = ("css", "scss", "sass", "less", "styl", "stylus", "pcss", "postcss")
JS_EXTENSIONS = ("js", "jsx", "ts", "tsx", "coffee", "coffeescript", "babel")
HTML_EXTENSIONS = ("html", "htm", "pug", "slim", "haml", "md", "markdown")
PREPROCESSORS = {
    "css": "css", "scss": "scss", "sass": "sass", "less": "less",
    "styl": "stylus", "stylus": "stylus", "pcss": "postcss",
    "postcss": "postcss", "js": "none", "jsx": "babel", "babel": "babel",
    "ts": "typescript", "tsx": "typescript", "coffee": "coffeescript",
    "coffeescript": "coffeescript", "html": "none", "htm": "none",
    "pug": "pug", "slim": "slim", "haml": "haml", "md": "markdown",
    "markdown": "markdown",
}
SUMMARY_FIELDS = [
    "case_id", "archive_file", "title", "author", "url",
    "style_preprocessor", "js_preprocessor", "has_js",
    "has_animation_timeline", "has_animation_range", "has_view_timeline",
    "has_scroll_timeline", "has_scroll_function", "has_view_function",
    "has_sticky", "keyframes_count", "has_gsap", "has_scroll_trigger",
    "has_intersection_observer", "collection_status", "error_message",
]


@dataclass
class ArchiveResult:
    archive_file: str
    title: str | None = None
    author: str | None = None
    url: str | None = None
    html_source: str | None = None
    html_extension: str = "html"
    compiled_html: str | None = None
    style_source: str | None = None
    style_extension: str = "css"
    compiled_css: str | None = None
    js_source: str | None = None
    js_extension: str = "js"
    compiled_js: str | None = None
    readme_file: str | None = None
    source_members: dict[str, str | None] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("必须是大于 0 的整数")
    return number


def read_member(archive: zipfile.ZipFile, name: str | None) -> str | None:
    if name is None:
        return None
    return archive.read(name).decode("utf-8", errors="replace")


def member_extension(name: str | None, default: str) -> str:
    return Path(name).suffix.lstrip(".").lower() if name else default


def members_in_folder(names: Iterable[str], folder: str, extensions: tuple[str, ...]) -> list[str]:
    marker = f"/{folder.lower()}/"
    found: list[str] = []
    for name in names:
        normalized = "/" + name.replace("\\", "/").lower().lstrip("/")
        if marker in normalized and not normalized.endswith("/"):
            if Path(normalized).suffix.lstrip(".") in extensions:
                found.append(name)
    return found


def choose_member(
    names: Iterable[str], folder: str, extensions: tuple[str, ...], preferred: tuple[str, ...]
) -> str | None:
    candidates = members_in_folder(names, folder, extensions)
    if not candidates:
        return None
    preferred_names = {name.lower(): index for index, name in enumerate(preferred)}
    candidates.sort(
        key=lambda name: (
            preferred_names.get(Path(name).name.lower(), len(preferred_names)),
            len(Path(name).parts),
            name.casefold(),
        )
    )
    return candidates[0]


def choose_readme(names: Iterable[str]) -> str | None:
    candidates = [
        name for name in names
        if Path(name).name.lower() in {"readme.md", "readme.markdown", "readme.txt", "readme"}
    ]
    return min(candidates, key=lambda name: (len(Path(name).parts), name.casefold()), default=None)


def extract_readme_metadata(text: str) -> tuple[str | None, str | None, str | None]:
    match = CODEPEN_URL_RE.search(text)
    url = author = None
    if match:
        author, slug = match.groups()
        slug = slug.rstrip(".,;:")
        url = f"https://codepen.io/{author}/pen/{slug}"

    title = None
    for line in text.splitlines():
        heading = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if heading and heading.group(1).strip().lower() not in {"readme", "codepen"}:
            title = heading.group(1).strip()
            break
    if title is None:
        title_match = re.search(r"(?:Title|Pen Title)\s*:\s*(.+)", text, re.I)
        if title_match:
            title = title_match.group(1).strip()
    return title, author, url


def collect_archive(path: Path) -> ArchiveResult:
    result = ArchiveResult(archive_file=path.name)
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            readme_name = choose_readme(names)
            result.readme_file = readme_name
            if readme_name:
                readme = read_member(archive, readme_name) or ""
                result.title, result.author, result.url = extract_readme_metadata(readme)
            else:
                result.errors.append("Export ZIP 中没有找到 README")

            html_name = choose_member(
                names, "src", HTML_EXTENSIONS,
                ("index.html", "index.htm", "index.pug", "index.haml", "index.slim"),
            )
            style_name = choose_member(
                names, "src", STYLE_EXTENSIONS,
                ("style.css", "style.scss", "style.sass", "style.less", "style.stylus"),
            )
            js_name = choose_member(
                names, "src", JS_EXTENSIONS,
                ("script.js", "index.js", "script.ts", "index.ts", "script.jsx", "index.jsx"),
            )
            dist_html_name = choose_member(names, "dist", ("html", "htm"), ("index.html",))
            dist_css_name = choose_member(names, "dist", ("css",), ("style.css", "index.css"))
            dist_js_name = choose_member(names, "dist", ("js",), ("script.js", "index.js"))

            result.source_members = {
                "html": html_name, "style": style_name, "javascript": js_name,
                "compiled_html": dist_html_name, "compiled_css": dist_css_name,
                "compiled_javascript": dist_js_name,
            }
            result.html_source = read_member(archive, html_name)
            result.html_extension = member_extension(html_name, "html")
            result.compiled_html = read_member(archive, dist_html_name)
            result.style_source = read_member(archive, style_name)
            result.style_extension = member_extension(style_name, "css")
            result.compiled_css = read_member(archive, dist_css_name)
            result.js_source = read_member(archive, js_name)
            result.js_extension = member_extension(js_name, "js")
            result.compiled_js = read_member(archive, dist_js_name)

            if result.html_source is None and result.compiled_html is None:
                result.errors.append("ZIP 的 src/ 和 dist/ 中都没有找到 HTML")
            if result.url is None:
                result.errors.append("README 中没有找到原始 CodePen URL")
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        result.errors.append(f"无法读取 Export ZIP：{exc}")
    return result


def css_features(css: str) -> dict[str, Any]:
    return {
        "has_animation_timeline": bool(re.search(r"\banimation-timeline\s*:", css, re.I)),
        "has_animation_range": bool(re.search(r"\banimation-range(?:-start|-end)?\s*:", css, re.I)),
        "has_view_timeline": bool(re.search(r"\bview-timeline(?:-name|-axis)?\s*:", css, re.I)),
        "has_scroll_timeline": bool(re.search(r"\bscroll-timeline(?:-name|-axis)?\s*:", css, re.I)),
        "has_scroll_function": bool(re.search(r"\bscroll\s*\(", css, re.I)),
        "has_view_function": bool(re.search(r"\bview\s*\(", css, re.I)),
        "has_sticky": bool(re.search(r"\bposition\s*:\s*sticky\b", css, re.I)),
        "keyframes_count": len(re.findall(r"@(?:-webkit-)?keyframes\b", css, re.I)),
    }


def js_features(js: str) -> dict[str, bool]:
    return {
        "has_gsap": bool(re.search(r"\bgsap\b", js, re.I)),
        "has_scroll_trigger": bool(re.search(r"\bScrollTrigger\b", js)),
        "has_intersection_observer": bool(re.search(r"\bIntersectionObserver\b", js)),
    }


def result_status(result: ArchiveResult) -> str:
    if result.html_source is None and result.compiled_html is None:
        return "failed"
    if result.url is None or result.html_source is None:
        return "partial"
    return "complete"


def metadata_document(case_id: str, result: ArchiveResult) -> dict[str, Any]:
    css = "\n".join(value for value in (result.style_source, result.compiled_css) if value)
    js = result.js_source if result.js_source is not None else (result.compiled_js or "")
    return {
        "case_id": case_id,
        "archive_file": result.archive_file,
        "title": result.title,
        "author": result.author,
        "url": result.url,
        "style_preprocessor": PREPROCESSORS.get(result.style_extension, result.style_extension),
        "js_preprocessor": PREPROCESSORS.get(result.js_extension, result.js_extension),
        "html_preprocessor": PREPROCESSORS.get(result.html_extension, result.html_extension),
        "has_js": bool(js.strip()),
        **css_features(css),
        **js_features(js),
        "readme_file": result.readme_file,
        "source_members": result.source_members,
        "collection_status": result_status(result),
        "error_message": "; ".join(dict.fromkeys(result.errors)) if result.errors else None,
    }


def write_case(case_dir: Path, result: ArchiveResult, metadata: dict[str, Any]) -> None:
    temp_dir = case_dir.with_name(f".{case_dir.name}.collecting")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=False)

    if result.html_source is not None:
        (temp_dir / f"source.{result.html_extension}").write_text(result.html_source, encoding="utf-8")
    elif result.compiled_html is not None:
        (temp_dir / "source.html").write_text(result.compiled_html, encoding="utf-8")
    if result.compiled_html is not None and result.html_extension not in {"html", "htm"}:
        (temp_dir / "compiled.html").write_text(result.compiled_html, encoding="utf-8")

    style_source = result.style_source if result.style_source is not None else ""
    (temp_dir / f"source.{result.style_extension}").write_text(style_source, encoding="utf-8")
    if result.compiled_css is not None and result.style_extension != "css":
        (temp_dir / "compiled.css").write_text(result.compiled_css, encoding="utf-8")

    js_source = result.js_source if result.js_source is not None else ""
    (temp_dir / f"source.{result.js_extension}").write_text(js_source, encoding="utf-8")
    if result.compiled_js is not None and result.js_extension != "js":
        (temp_dir / "compiled.js").write_text(result.compiled_js, encoding="utf-8")

    (temp_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if case_dir.exists():
        shutil.rmtree(case_dir)
    temp_dir.replace(case_dir)


def load_metadata(case_dir: Path) -> dict[str, Any] | None:
    path = case_dir / "metadata.json"
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="将 CodePen Export ZIP 批量转换为 benchmark 案例")
    parser.add_argument("--exports-dir", type=Path, default=DEFAULT_EXPORTS)
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--start-case", type=positive_int, required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    exports_dir = args.exports_dir.resolve()
    cases_dir = args.cases_dir.resolve()
    summary_path = args.summary.resolve()
    if not exports_dir.is_dir():
        raise SystemExit(f"Export ZIP 目录不存在：{exports_dir}")
    if not cases_dir.is_dir():
        raise SystemExit(f"cases 目录不存在：{cases_dir}")

    archives = sorted(exports_dir.glob("*.zip"), key=lambda path: path.name.casefold())
    if not archives:
        raise SystemExit(f"Export ZIP 目录中没有 .zip 文件：{exports_dir}")
    targets = [cases_dir / f"case-{args.start_case + index:03d}" for index in range(len(archives))]

    for archive, target in zip(archives, targets):
        tiered = sorted(cases_dir.glob(f"{target.name}-T[1-6]"))
        if tiered:
            raise SystemExit(f"案例编号已被占用：{', '.join(path.name for path in tiered)}")
        existing = load_metadata(target)
        if target.exists() and existing is None:
            raise SystemExit(f"目标目录已存在且不是可识别的 CodePen 案例：{target}")
        existing_archive = existing.get("archive_file") if existing else None
        if existing_archive and existing_archive != archive.name and not args.overwrite:
            raise SystemExit(
                f"{target.name} 原来对应 {existing_archive!r}，现在将对应 {archive.name!r}；"
                "ZIP 排序已经变化，请确认后使用 --overwrite"
            )

    rows: list[dict[str, Any]] = []
    failures = 0
    for index, (archive, target) in enumerate(zip(archives, targets), 1):
        existing = load_metadata(target)
        if (
            existing
            and existing.get("archive_file") == archive.name
            and existing.get("collection_status") == "complete"
            and not args.overwrite
        ):
            print(f"[{index}/{len(archives)}] SKIPPED  {target.name}: {archive.name}")
            rows.append(existing)
            continue
        print(f"[{index}/{len(archives)}] CONVERT  {target.name}: {archive.name}")
        result = collect_archive(archive)
        metadata = metadata_document(target.name, result)
        write_case(target, result, metadata)
        rows.append(metadata)
        status = metadata["collection_status"].upper()
        print(f"[{index}/{len(archives)}] {status:<8} {target.name}")
        if status == "FAILED":
            failures += 1

    write_summary(summary_path, rows)
    print(f"完成：{len(rows)} 个 ZIP，{failures} 个失败；汇总：{summary_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
