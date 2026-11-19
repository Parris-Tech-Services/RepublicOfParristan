#!/usr/bin/env python3
"""Generate docs/data/dashboard-metadata.json from repository records.

Reads:
  - gazette/INDEX.md  → Gazette notice list
  - institutions/DECISION_REGISTER.md → Decisions table
  - NATIONAL_OPERATIONS_TODO.md → operations completion counter
  - institutions/ROADMAP.md → roadmap steps
Outputs JSON to docs/data/dashboard-metadata.json.

Usage:
    python scripts/build_metadata.py          # regenerate in place
    python scripts/build_metadata.py --check  # exit non-zero if file is stale
"""
import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "docs" / "data" / "dashboard-metadata.json"

_MONTHS = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
    "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
    "Nov": "11", "Dec": "12",
}


def _to_iso(raw):
    """Convert human-readable dates to ISO-8601 (YYYY-MM-DD).

    Handles formats like '19 Nov 2026', '19 November 2026', '2026-11-19'.
    Returns the original string on failure rather than raising.
    """
    raw = raw.strip()
    # Already ISO?
    try:
        date.fromisoformat(raw)
        return raw
    except ValueError:
        pass
    # Try strptime for common markdown formats
    for fmt in ("%d %b %Y", "%d %B %Y", "%Y-%m-%d"):
        try:
            parsed = datetime.strptime(raw, fmt).date()
            return parsed.isoformat()
        except ValueError:
            continue
    # Fallback: keep original
    return raw


def parse_gazette_index():
    """Extract Gazette notices from gazette/INDEX.md."""
    path = REPO_ROOT / "gazette" / "INDEX.md"
    text = path.read_text(encoding="utf-8")
    notices = []
    # Match rows like: | [2026-001](...) | 19 November 2026 | Title | Status |
    for m in re.finditer(
        r'\|\s*\[([^\]]+)\]\([^)]+\)\s*\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|',
        text,
    ):
        nid, raw_date, title, status = m.group(1), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
        # Parse date
        iso = _to_iso(raw_date)
        notices.append({
            "id": nid,
            "date": iso,
            "title": title,
            "category": _categorise_notice(title),
            "tag": status,
            "description": "",  # populated from HTML content if available
        })
    return notices


def _categorise_notice(title):
    t = title.lower()
    if "symbol" in t or "flag" in t or "anthem" in t:
        return "symbols"
    if "constituent" in t or "assembly" in t or "matrix" in t or "election" in t or "returning" in t:
        return "assembly"
    return "constitution"


def parse_decision_register():
    """Parse decision register table from institutions/DECISION_REGISTER.md.

    Table has 5 columns: ID | Date | Resolution | Vote / consent | Effect and source.
    We join all pipe-delimited content between FA-XXXX-IDs.
    """
    path = REPO_ROOT / "institutions" / "DECISION_REGISTER.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    decisions = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("| "):
            if in_table and stripped:
                # End of table on next non-empty non-pipe line
                in_table = False
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if "Date" in stripped and "Resolution" in stripped:
            in_table = True
            continue
        if stripped.startswith("|---"):
            continue
        if not in_table:
            continue
        # Only keep rows that start with a decision ID
        if not any(c.startswith("FA-") for c in cells):
            continue
        # Exactly 5 columns expected; pad if needed
        while len(cells) < 5:
            cells.append("")
        did, ddate, resolution, vote = cells[0], cells[1], cells[2], cells[3]
        iso = _to_iso(ddate)
        # Clean markdown bold from resolution
        resolution = re.sub(r"\*\*", "", resolution)
        vote = re.sub(r"\*\*", "", vote)
        decisions.append({"id": did, "date": iso, "text": resolution, "vote": vote})
    return decisions


def count_operations():
    """Count [x] and total items in NATIONAL_OPERATIONS_TODO.md."""
    path = REPO_ROOT / "NATIONAL_OPERATIONS_TODO.md"
    text = path.read_text(encoding="utf-8")
    done = len(re.findall(r'(?m)^\d+\.\s*\[x\]', text))
    total = len(re.findall(r'(?m)^\d+\.\s*\[[ x]\]', text))
    return done, total


def parse_roadmap_from_md():
    """Extract five-step roadmap from README.md about panel."""
    # We hard-code the five standard steps since they're documented in multiple places
    return [
        {"step": 1, "label": "Publish honest founding documents", "status": "complete", "note": "Completed"},
        {"step": 2, "label": "Form constituent assembly", "status": "complete", "note": "Completed: all five founders attended on 19 November 2026."},
        {"step": 3, "label": "Ratify the constitution", "status": "complete", "note": "5 YES / 0 NO / 0 ABSTAIN; effective 19 November 2026."},
        {"step": 4, "label": "Elect accountable officeholders", "status": "in_progress", "note": "Interim roles appointed; Presidential election pending 28 Nov – 1 Dec."},
        {"step": 5, "label": "Develop civic community", "status": "future", "note": "Membership, lawful premises and external relationships."},
    ]


def main(check_only=False):
    notices = parse_gazette_index()
    decisions = parse_decision_register()
    ops_done, ops_total = count_operations()

    metadata = {
        "meta": {
            "title": "Republic of Parristan · Public Administration Dashboard",
            "description": "Live view of constitutional progress, Gazette notices, operations tracking and institutional health.",
            "updated": date.today().isoformat(),
            "source": "https://github.com/Parris-Tech-Services/RepublicOfParristan",
        },
        "kpi": {
            "gazette_notices_published": len(notices),
            "constitutional_instruments_ratified": 1,
            "recorded_decisions": len(decisions),
            "elected_president": 0,
            "interim_appointees": 4,
            "operations_done": ops_done,
            "operations_total": ops_total,
            "founding_members": 5,
        },
        "roadmap": parse_roadmap_from_md(),
        "decisions": decisions,
        "officeholders": [
            {"role": "Chief Digital Officer / OSPO", "name": "Glenn Peterson", "appointed_by": "FA-2026-004 (unanimous)", "started": "2026-11-19", "term": "until reassignment"},
            {"role": "Secretary (interim)", "name": "Jane Carbunkle", "appointed_by": "FA-2026-007 (5–0)", "started": "2026-11-19", "term": "until first election"},
            {"role": "Treasurer (interim)", "name": "Fred Carbunkle", "appointed_by": "FA-2026-007 (5–0)", "started": "2026-11-19", "term": "until first election"},
            {"role": "Registrar (interim)", "name": "Glenn Peterson", "appointed_by": "FA-2026-007 (5–0)", "started": "2026-11-19", "term": "until first election"},
            {"role": "Returning Officer", "name": "Matthew John Lucas Walker", "appointed_by": "FA-2026-006 (5–0)", "started": "2026-11-19", "term": "until first election result certified"},
            {"role": "President", "name": "Not elected", "appointed_by": None, "started": None, "term": "N/A — election pending 28 Nov – 1 Dec"},
        ],
        "election_timetable": {
            "nominations_open": "2026-11-20",
            "nominations_close": "2026-11-27",
            "voting_start": "2026-11-28",
            "voting_end": "2026-12-01",
            "returning_officer": "Matthew John Lucas Walker",
            "candidates": ["Joshua Parris (intention shared)"],
            "status": "nominations_pending",
        },
        "operations_status": {},  # placeholder for future detailed ops mapping
        "symbols": [
            {
                "name": "Flag — Founding Star",
                "type": "flag",
                "status": "consultation",
                "colors": ["navy #142b42", "teal #0e675f", "ivory #fffdf8", "gold #e3b366"],
                "description": "Gold eight-point star on navy field, ivory stripe and teal band",
                "image": "../assets/flag-proposal.svg",
            },
            {
                "name": "Civic Arms — Liberty Service Truth",
                "type": "arms",
                "status": "consultation",
                "description": "Navy-and-teal shield, golden star and branches with motto",
                "image": "../assets/arms-proposal.svg",
            },
        ],
        "tech_stack": {
            "gendarmerie": {
                "name": "French National Gendarmerie (GendBuntu) — proposed pilot",
                "items": [
                    {"name": "UCS (Univention Corporate Server)", "status": "proposed", "progress": 0},
                    {"name": "LibreOffice", "status": "proposed", "progress": 0},
                    {"name": "Thobys email", "status": "proposed", "progress": 0},
                    {"name": "Nextcloud collaboration", "status": "proposed", "progress": 0},
                    {"name": "ParriBuntu desktop image", "status": "proposal_only", "progress": 0},
                ],
            },
            "schleswig_holstein": {
                "name": "Schleswig-Holstein (Germany) migration — evidence model",
                "items": [
                    {"name": "Müller-MSP office suite", "status": "completed", "progress": 100},
                    {"name": "Messaging (Matrix/Dendrite)", "status": "completed", "progress": 100},
                    {"name": "Collaboration infrastructure", "status": "completed", "progress": 100},
                    {"name": "Linux endpoint deployment", "status": "ongoing", "progress": 65},
                ],
            },
        },
        "institution_health": [
            {"institution": "Constitution", "status": "ratified_adopted_v0.1", "file": "CONSTITUTION.md"},
            {"institution": "Decision Register", "status": "active_8_decisions", "file": "DECISION_REGISTER.md"},
            {"institution": "Founding Declaration", "status": "published_for_consultation", "file": "FOUNDING_DECLARATION.md"},
            {"institution": "Ratification Procedure", "status": "proposal", "file": "RATIFICATION_PROCEDURE.md"},
            {"institution": "Election Rules", "status": "proposal", "file": "ELECTION_RULES.md"},
            {"institution": "Citizenship & Privacy Policy", "status": "policy_proposal", "file": "CITIZENSHIP.md"},
            {"institution": "Governance Framework", "status": "proposal", "file": "GOVERNANCE.md"},
            {"institution": "National Symbols Policy", "status": "design_proposals", "file": "NATIONAL_SYMBOLS.md"},
            {"institution": "Legal Status Position", "status": "published", "file": "LEGAL_STATUS.md"},
            {"institution": "OS Charter", "status": "activated_unanimous", "file": "OSPO_CHARTER_2026-11-19.md"},
        ],
    }

    # Add notices with descriptions from HTML notices
    notices_dir = REPO_ROOT / "docs" / "notices"
    for n in notices:
        html_path = notices_dir / f"{n['id']}.html"
        if html_path.exists():
            desc_match = re.search(r'<p class="copy"[^>]*>([^<]*)</p>', html_path.read_text(encoding="utf-8"))
            if desc_match:
                n["description"] = desc_match.group(1).strip()
            # Determine tag style
            if any(kw in n.get("tag","").lower() for kw in ["ratified", "adopted", "applied", "reported"]):
                pass  # green (default)
            else:
                n["tag_class"] = "amber"
        else:
            n["tag_class"] = "amber"

    output = json.dumps(metadata, indent=2, ensure_ascii=False) + "\n"

    if check_only:
        if DATA_FILE.exists():
            existing = DATA_FILE.read_text(encoding="utf-8")
            if existing != output:
                print(f"STALE: {DATA_FILE} needs regeneration", file=sys.stderr)
                print(f"  Old KPI:  notices={json.loads(existing)['kpi']['gazette_notices_published']}, "
                      f"ops={json.loads(existing)['kpi']['operations_done']}/{json.loads(existing)['kpi']['operations_total']}",
                      file=sys.stderr)
                print(f"  New KPI:  notices={metadata['kpi']['gazette_notices_published']}, "
                      f"ops={metadata['kpi']['operations_done']}/{metadata['kpi']['operations_total']}",
                      file=sys.stderr)
                return 1
            else:
                print(f"OK: {DATA_FILE} is up to date")
                return 0
        else:
            print(f"MISSING: {DATA_FILE} does not exist yet", file=sys.stderr)
            return 1
    else:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(output, encoding="utf-8")
        print(f"Wrote {DATA_FILE}")
        print(f"  Notices: {len(notices)}, Decisions: {len(decisions)}, Operations: {ops_done}/{ops_total}")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Only check whether file is up-to-date")
    args = parser.parse_args()
    sys.exit(main(check_only=args.check))
