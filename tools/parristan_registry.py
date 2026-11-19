#!/usr/bin/env python3
"""Minimal offline Parristan membership register. Use ONLY with a database outside the repo.

No network activity, no automatic sign-up, no legal nationality creation.
SQLite is NOT encrypted. Secure the containing directory/device independently.
"""
import argparse
import csv
import io
from datetime import date, datetime, timezone
import os
from pathlib import Path
import sqlite3
import uuid

REPO_ROOT = Path(__file__).resolve().parent.parent

def safe_db_path(raw):
    path = Path(raw).expanduser()
    if not path.is_absolute():
        raise ValueError("The --db path must be absolute.")
    path = path.resolve()
    if path == REPO_ROOT or REPO_ROOT in path.parents:
        raise ValueError("Refusing to put a membership database in the Git repository.")
    if path.suffix != ".sqlite3":
        raise ValueError("Database must use the .sqlite3 extension.")
    return path

def init_db(path):
    path = safe_db_path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY,
            public_name TEXT NOT NULL,
            consent_date TEXT NOT NULL,
            recorded_utc TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('active', 'withdrawn'))
        )""")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path

def require_existing(path):
    path = safe_db_path(str(path))
    if not path.is_file():
        raise ValueError("Database does not exist. Run 'init' first.")
    return path

def add_member(path, name, consent_date):
    path = require_existing(path)
    name = name.strip()
    if not name or len(name) > 160:
        raise ValueError("A non-empty member name (up to 160 characters) is required.")
    try:
        when = date.fromisoformat(consent_date)
    except ValueError:
        raise ValueError("Use a valid ISO consent date, YYYY-MM-DD.") from None
    if when > date.today():
        raise ValueError("Consent cannot be recorded as occurring in the future.")
    member_id = str(uuid.uuid4())
    with sqlite3.connect(path) as con:
        con.execute("INSERT INTO members (id, public_name, consent_date, recorded_utc, status) VALUES (?, ?, ?, ?, ?)", (
            member_id, name, when.isoformat(), datetime.now(timezone.utc).isoformat(), "active"
        ))
    return member_id

def withdraw_member(path, member_id):
    path = require_existing(path)
    with sqlite3.connect(path) as con:
        changed = con.execute(
            "UPDATE members SET status = 'withdrawn' WHERE id = ? AND status = 'active'",
            (member_id,)
        ).rowcount
    return changed == 1

def remove_member(path, member_id):
    """Delete identifiable record; coordinate backup deletion under actual policy."""
    path = require_existing(path)
    with sqlite3.connect(path) as con:
        changed = con.execute("DELETE FROM members WHERE id = ?", (member_id,)).rowcount
    return changed == 1

def migrate(con):
    cols = {r[1] for r in con.execute("PRAGMA table_info(members)")}
    if "member_number" not in cols:
        con.execute("ALTER TABLE members ADD COLUMN member_number INTEGER")
    if "withdrawn_date" not in cols:
        con.execute("ALTER TABLE members ADD COLUMN withdrawn_date TEXT")

def assign_number(path, member_id):
    """Issue the next sequential member number (P-0001...). Numbers are never reused."""
    path = require_existing(path)
    with sqlite3.connect(path) as con:
        migrate(con)
        row = con.execute("SELECT member_number FROM members WHERE id = ?", (member_id,)).fetchone()
        if row is None:
            raise ValueError("No member with that ID.")
        if row[0] is not None:
            return format_number(row[0])
        nxt = con.execute("SELECT coalesce(max(member_number), 0) + 1 FROM members").fetchone()[0]
        con.execute("UPDATE members SET member_number = ? WHERE id = ?", (nxt, member_id))
    return format_number(nxt)

def format_number(n):
    return f"P-{n:04d}"

def resign_member(path, member_id, on_date):
    """Record a resignation with its effective date (keeps the record; see remove for erasure)."""
    path = require_existing(path)
    when = date.fromisoformat(on_date)
    with sqlite3.connect(path) as con:
        migrate(con)
        changed = con.execute(
            "UPDATE members SET status='withdrawn', withdrawn_date=? WHERE id=? AND status='active'",
            (when.isoformat(), member_id)).rowcount
    return changed == 1

def electoral_roll(path, as_of):
    """One row per member eligible on as_of: consented on or before, and not withdrawn by then."""
    path = require_existing(path)
    cutoff = date.fromisoformat(as_of).isoformat()
    with sqlite3.connect(path) as con:
        migrate(con)
        rows = con.execute(
            "SELECT member_number, public_name FROM members WHERE consent_date <= ? "
            "AND (status='active' OR (withdrawn_date IS NOT NULL AND withdrawn_date > ?)) "
            "ORDER BY coalesce(member_number, 999999), public_name", (cutoff, cutoff)).fetchall()
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["member_number", "public_name"])
    for number, name in rows:
        w.writerow([format_number(number) if number else "", name])
    return out.getvalue()

def aggregate_report(path):
    """Counts only, safe for publication: no names or IDs."""
    s = summary(path)
    with sqlite3.connect(require_existing(path)) as con:
        migrate(con)
        numbered = con.execute("SELECT count(*) FROM members WHERE member_number IS NOT NULL").fetchone()[0]
    s["numbered"] = numbered
    s["generated"] = date.today().isoformat()
    return s

def import_founders(path, csv_path):
    """Add and number members from a private CSV (columns: name, consent_date), in file order.

    The CSV must live outside the repository. Names already on the register are skipped.
    Returns a list of (member_number, name, status) tuples.
    """
    src = Path(csv_path).expanduser().resolve()
    if src == REPO_ROOT or REPO_ROOT in src.parents:
        raise ValueError("Refusing to read member data from inside the Git repository.")
    path = require_existing(path)
    with sqlite3.connect(path) as con:
        existing = {r[0] for r in con.execute("SELECT public_name FROM members")}
    results = []
    with open(src, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            name = (row.get("name") or "").strip()
            if not name:
                continue
            if name in existing:
                results.append(("", name, "skipped (already registered)"))
                continue
            member_id = add_member(path, name, (row.get("consent_date") or "").strip())
            results.append((assign_number(path, member_id), name, "added"))
            existing.add(name)
    return results

def summary(path):
    path = require_existing(path)
    with sqlite3.connect(path) as con:
        total, active = con.execute(
            "SELECT count(*), sum(CASE WHEN status='active' THEN 1 ELSE 0 END) FROM members"
        ).fetchone()
    return {"total": total, "active": active or 0, "withdrawn": total - (active or 0)}

def list_members(path):
    path = require_existing(path)
    with sqlite3.connect(path) as con:
        return con.execute(
            "SELECT id, public_name, consent_date, status FROM members ORDER BY recorded_utc, id"
        ).fetchall()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="Absolute path OUTSIDE the Git repository")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    add = sub.add_parser("add")
    add.add_argument("--name", required=True)
    add.add_argument("--consent-date", required=True)
    change = sub.add_parser("withdraw")
    change.add_argument("--id", required=True)
    remove = sub.add_parser("remove")
    remove.add_argument("--id", required=True)
    sub.add_parser("summary")
    sub.add_parser("list")
    num = sub.add_parser("number", help="issue a member number")
    num.add_argument("--id", required=True)
    res = sub.add_parser("resign")
    res.add_argument("--id", required=True)
    res.add_argument("--date", required=True)
    roll = sub.add_parser("roll", help="CSV electoral roll as of a date")
    roll.add_argument("--as-of", required=True)
    sub.add_parser("report", help="aggregate counts, safe to publish")
    imp = sub.add_parser("import", help="add and number members from a private CSV (name,consent_date)")
    imp.add_argument("--csv", required=True)
    args = parser.parse_args()
    try:
        if args.cmd == "init":
            print("Database initialised:", init_db(args.db))
        elif args.cmd == "add":
            print("Member ID:", add_member(args.db, args.name, args.consent_date))
        elif args.cmd == "withdraw":
            print("Withdrawn:", withdraw_member(args.db, args.id))
        elif args.cmd == "remove":
            print("Deleted:", remove_member(args.db, args.id))
        elif args.cmd == "summary":
            print(summary(args.db))
        elif args.cmd == "list":
            for row in list_members(args.db):
                print("\t".join(row))
        elif args.cmd == "number":
            print("Member number:", assign_number(args.db, args.id))
        elif args.cmd == "resign":
            print("Resigned:", resign_member(args.db, args.id, args.date))
        elif args.cmd == "roll":
            print(electoral_roll(args.db, args.as_of), end="")
        elif args.cmd == "report":
            print(aggregate_report(args.db))
        elif args.cmd == "import":
            for number, name, status in import_founders(args.db, args.csv):
                print(f"{number or '-'}\t{name}\t{status}")
    except (ValueError, sqlite3.DatabaseError) as e:
        parser.error(str(e))

if __name__ == "__main__":
    main()
