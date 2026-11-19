import tempfile
from pathlib import Path
import unittest
from datetime import date

from tools.parristan_registry import (
    REPO_ROOT, safe_db_path, init_db, add_member, summary,
    list_members, withdraw_member, remove_member,
)

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "members.sqlite3"

    def test_refuses_repository_database(self):
        with self.assertRaises(ValueError):
            safe_db_path(str(REPO_ROOT / "test.sqlite3"))

    def test_refuses_relative_database(self):
        with self.assertRaises(ValueError):
            safe_db_path("test.sqlite3")

    def test_init_and_membership_lifecycle(self):
        init_db(self.path)
        self.assertEqual(summary(self.path), {"total": 0, "active": 0, "withdrawn": 0})
        ref = add_member(self.path, "Sample Member", date.today().isoformat())
        self.assertEqual(len(ref), 36)
        self.assertEqual(len(list_members(self.path)), 1)
        self.assertEqual(summary(self.path), {"total": 1, "active": 1, "withdrawn": 0})
        self.assertTrue(withdraw_member(self.path, ref))
        self.assertFalse(withdraw_member(self.path, ref))
        self.assertEqual(summary(self.path)["withdrawn"], 1)
        self.assertTrue(remove_member(self.path, ref))
        self.assertEqual(summary(self.path)["total"], 0)

    def test_rejects_invalid_inputs(self):
        init_db(self.path)
        for name, consent in [("", "2026-11-19"), ("Sample", "not-a-date"), ("Sample", "2999-01-01")]:
            with self.assertRaises(ValueError):
                add_member(self.path, name, consent)

    def test_must_init_before_adding(self):
        with self.assertRaises(ValueError):
            add_member(self.path, "Sample", date.today().isoformat())

if __name__ == "__main__":
    unittest.main()
