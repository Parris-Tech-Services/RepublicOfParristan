#!/usr/bin/env python3
"""Minimal offline Parristan membership register. Use ONLY with a database outside the repo.

No network activity, no automatic sign-up, no legal nationality creation.
SQLite is NOT encrypted. Secure the containing directory/device independently.
"""
import argparse
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
        con.execute("INSERT INTO members VALUES (?, ?, ?, ?, ?)", (
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
    except (ValueError, sqlite3.DatabaseError) as e:
        parser.error(str(e))

if __name__ == "__main__":
    main()
