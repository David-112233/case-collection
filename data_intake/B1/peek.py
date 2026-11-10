"""Print a compact view of candidates: CSS without comments + body tag outline. Usage: peek.py KEY [KEY...] [--css N] [--body N]"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "raw"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
css_limit = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--css=")), 2500))
body_limit = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--body=")), 800))
for key in args:
    src = (ROOT / key / "source.html").read_text(encoding="utf-8")
    css = "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", src, re.S))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\n\s*\n+", "\n", css)
    css = re.sub(r"[ \t]+", " ", css)
    body = src.split("<body", 1)[-1]
    body = re.sub(r"<style\b.*?</style>|<script\b.*?</script>", "", body, flags=re.S)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    tags = re.findall(r"<([a-z][a-z0-9-]*)", body)
    print(f"===== {key}  css={len(css)} tags={len(tags)}")
    print(css[:css_limit])
    print("--- text:", text[:body_limit])
    if "--js" in sys.argv:
        for attrs, code in re.findall(r"<script\b([^>]*)>(.*?)</script>", src, re.S):
            print("--- script", attrs.strip(), "\n", code.strip()[:1500])
        print("--- controls:", re.findall(r"<input[^>]*>|<label[^>]*>|href=\"#[^\"]*\"", src)[:12])
