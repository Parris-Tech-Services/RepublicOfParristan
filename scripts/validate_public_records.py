#!/usr/bin/env python3
"""Read-only integrity checks for Parristan's public decision export/pages."""
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
errors = []
FOUNDING = date(2026, 11, 19)
MEMBERS = len(json.loads((ROOT / "assembly/roster.json").read_text(encoding="utf-8"))["members"])
data_path = ROOT / "docs/data/decisions.json"
payload = json.loads(data_path.read_text(encoding="utf-8"))
records = payload["decisions"]
ids = [d["id"] for d in records]
expected = [f"FA-2026-{i:03d}" for i in range(1, len(records) + 1)]
if payload.get("schema_version") != 1 or ids != expected or len(ids) != len(set(ids)):
    errors.append("Decision IDs must be ordered, unique and match the export schema")
register = (ROOT / "institutions/DECISION_REGISTER.md").read_text(encoding="utf-8")
gazette_index = (ROOT / "gazette/INDEX.md").read_text(encoding="utf-8")
registered = re.findall(r"^\| (FA-\d{4}-\d{3}) \|", register, flags=re.MULTILINE)
if registered != ids:
    errors.append("Machine-readable decisions differ from the authoritative Markdown register")

for record in records:
    try:
        when = date.fromisoformat(record["date"])
    except (TypeError, ValueError):
        when = None
    if when is None or when < FOUNDING or when > date.fromisoformat(payload["recorded_as_of"]):
        errors.append(f"Decision date for {record['id']} must fall between founding and recorded_as_of")
    votes = [record[k] for k in ("yes", "no", "abstain")]
    if not all(v is None for v in votes):
        if not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in votes):
            errors.append(f"Partial or invalid vote counts for {record['id']}")
        elif not 1 <= sum(votes) <= MEMBERS:
            errors.append(f"Vote count for {record['id']} must be between 1 and {MEMBERS} voters")
    if record["id"] in ("FA-2026-003", "FA-2026-004") and votes != [None, None, None]:
        errors.append(f"Do not invent exact counts for {record['id']}")
    path = (ROOT / record["source"]).resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        errors.append(f"Missing or unsafe source path for {record['id']}")
    if record["notice"] not in gazette_index:
        errors.append(f"Missing notice in Gazette index: {record['notice']}")
    if not (ROOT / "docs/notices" / (record["notice"] + ".html")).is_file():
        errors.append(f"Missing notice HTML: {record['notice']}")
    if not record.get("result") or not record.get("title"):
        errors.append(f"Missing public explanation for {record['id']}")

for page in ("docs/administration.html", "docs/decisions.html"):
    content = (ROOT / page).read_text(encoding="utf-8")
    listed = re.findall(r'data-decision-id="(FA-\d{4}-\d{3})"', content)
    if listed != ids:
        errors.append(f"{page} must list every decision exactly once, in ID order")
    if "data/decisions.json" not in content:
        errors.append(f"{page} must link the machine-readable public export")
for page in ("docs/administration.html", "docs/status.html"):
    content = (ROOT / page).read_text(encoding="utf-8")
    if not re.search(r"President(</th><td>|: )<strong>(Joshua Parris|Vacant|none yet)", content) and "No President" not in content:
        errors.append(f"{page} must not leave presidential status ambiguous")

if errors:
    print("PUBLIC RECORD VALIDATION FAILED")
    for item in errors:
        print(" -", item)
    sys.exit(1)
print(f"PUBLIC RECORD VALIDATION PASSED — {len(ids)} decisions and two linked HTML views")
