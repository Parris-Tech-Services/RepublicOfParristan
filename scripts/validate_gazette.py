#!/usr/bin/env python3
"""Read-only checks for the public Parristan Gazette. Standard library only."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
 "README.md", "gazette/INDEX.md",
 "gazette/2026/2026-001-founding-consultation.md",
 "gazette/2026/2026-002-assembly-invitation.md",
 "gazette/2026/2026-003-symbols-consultation.md",
 "institutions/CONSTITUTION_DRAFT.md", "institutions/FOUNDING_ASSEMBLY.md",
 "institutions/RATIFICATION_PROCEDURE.md", "institutions/DECISION_REGISTER.md",
 "docs/index.html", "docs/about.html", "docs/participate.html", "docs/site.css",
 "docs/site.js", "docs/notices/2026-001.html",
 "docs/notices/2026-002.html", "docs/notices/2026-003.html",
 "docs/assets/flag-proposal.svg", "docs/assets/arms-proposal.svg"
]
errors = []
for name in REQUIRED:
    if not (ROOT / name).is_file():
        errors.append("Missing required file: " + name)

class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("src", "href") and v:
                self.targets.append(v)

def verify_link(base, href):
    if href.startswith(("https://", "http://", "mailto:", "#", "javascript:", "data:")):
        return
    rel = href.split("#", 1)[0].split("?", 1)[0]
    if not rel:
        return
    dest = (base.parent / rel).resolve()
    if not dest.is_relative_to(ROOT.resolve()):
        errors.append("Link escapes repository: " + str(base.relative_to(ROOT)) + " -> " + href)
    elif not dest.exists():
        errors.append("Broken relative link: " + str(base.relative_to(ROOT)) + " -> " + href)

for page in (ROOT / "docs").rglob("*.html"):
    parser = HTMLLinks()
    text = page.read_text(encoding="utf-8")
    try:
        parser.feed(text)
    except Exception as exc:
        errors.append(f"Malformed HTML {page.relative_to(ROOT)}: {exc}")
    if "<main" not in text or "<title>" not in text or 'lang="en-AU"' not in text:
        errors.append("Missing HTML semantic essentials: " + str(page.relative_to(ROOT)))
    for href in parser.targets:
        verify_link(page, href)

for md in ROOT.rglob("*.md"):
    if ".git" in md.parts:
        continue
    text = md.read_text(encoding="utf-8")
    for href in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]+\")?\)", text):
        verify_link(md, href)

for svg in (ROOT / "docs/assets").glob("*.svg"):
    try:
        root = ET.parse(svg).getroot()
        if not root.tag.endswith("svg"):
            errors.append("Invalid SVG root: " + str(svg.relative_to(ROOT)))
    except Exception as exc:
        errors.append("Invalid SVG XML: " + str(svg.relative_to(ROOT)) + ": " + str(exc))

notices = sorted((ROOT / "gazette").glob("20??/*.md"))
ids = [p.name[:8] for p in notices]
if len(ids) != len(set(ids)):
    errors.append("Duplicate Gazette IDs")
for path in notices:
    notice_id = path.name[:8]
    if not re.fullmatch(r"\d{4}-\d{3}", notice_id):
        errors.append("Unexpected Gazette notice filename: " + path.name)
    head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:15])
    if not re.search(r"\b\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) 20\d{2}\b", head):
        errors.append("Missing publication date near the top of " + path.name)
    if notice_id not in (ROOT / "gazette/INDEX.md").read_text(encoding="utf-8"):
        errors.append("Gazette index missing " + notice_id)
    if not (ROOT / ("docs/notices/" + notice_id + ".html")).is_file():
        errors.append("No HTML notice for " + notice_id)


# Cross-check the published Gazette against its two human-facing indexes.
index_text = (ROOT / "gazette/INDEX.md").read_text(encoding="utf-8")
indexed = re.findall(r'^\| \[(\d{4}-\d{3})\]\(', index_text, flags=re.MULTILINE)
home_text = (ROOT / "docs/index.html").read_text(encoding="utf-8")
linked = re.findall(r'href="notices/(\d{4}-\d{3})\.html" data-notice', home_text)
expected = sorted(ids)
if sorted(indexed) != expected:
    errors.append("Gazette Markdown index IDs do not exactly match published notices")
if sorted(linked) != expected:
    errors.append("Website notice listing IDs do not exactly match published notices")
visible_count = re.search(r'<strong>(\d+)</strong><span>Published notices</span>', home_text)
if visible_count is None or int(visible_count.group(1)) != len(ids):
    errors.append("Homepage published notice count is stale")

if errors:
    print("GAZETTE VALIDATION FAILED")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print("GAZETTE VALIDATION PASSED —", len(notices), "notices and", len(list((ROOT / "docs").rglob("*.html"))), "HTML pages")
