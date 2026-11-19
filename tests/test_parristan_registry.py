import tempfile
from pathlib import Path
import unittest
from datetime import date

from tools.parristan_registry import (
    REPO_ROOT, safe_db_path, init_db, add_member, summary,
    list_members, withdraw_member, remove_member,
    assign_number, resign_member, electoral_roll, aggregate_report, import_founders,
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

class RollTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = init_db(Path(self.temp.name) / "m.sqlite3")

    def test_numbers_sequential_and_stable(self):
        a = add_member(self.path, "Alpha", "2026-11-01")
        b = add_member(self.path, "Beta", "2026-11-01")
        self.assertEqual(assign_number(self.path, a), "P-0001")
        self.assertEqual(assign_number(self.path, b), "P-0002")
        self.assertEqual(assign_number(self.path, a), "P-0001")
        with self.assertRaises(ValueError):
            assign_number(self.path, "missing")

    def test_roll_respects_dates_and_resignation(self):
        a = add_member(self.path, "Alpha", "2026-11-01")
        b = add_member(self.path, "Beta", "2026-11-10")
        c = add_member(self.path, "Gamma", "2026-11-01")
        assign_number(self.path, a)
        self.assertTrue(resign_member(self.path, c, "2026-11-05"))
        roll = electoral_roll(self.path, "2026-11-03")
        self.assertIn("P-0001,Alpha", roll)
        self.assertIn("Gamma", roll)
        self.assertNotIn("Beta", roll)
        later = electoral_roll(self.path, "2026-11-12")
        self.assertIn("Beta", later)
        self.assertNotIn("Gamma", later)

    def test_import_numbers_in_order_and_skips_duplicates(self):
        csv_path = Path(self.temp.name) / "consents.csv"
        csv_path.write_text("name,consent_date\nAlpha,2026-11-19\nBeta,2026-11-19\nAlpha,2026-11-19\n", encoding="utf-8")
        result = import_founders(self.path, csv_path)
        self.assertEqual(result[0][:2], ("P-0001", "Alpha"))
        self.assertEqual(result[1][:2], ("P-0002", "Beta"))
        self.assertIn("skipped", result[2][2])

    def test_import_refuses_csv_in_repository(self):
        with self.assertRaises(ValueError):
            import_founders(self.path, REPO_ROOT / "consents.csv")

    def test_report_has_no_names(self):
        add_member(self.path, "Alpha", "2026-11-01")
        r = aggregate_report(self.path)
        self.assertEqual(r["active"], 1)
        self.assertNotIn("Alpha", str(r))

if __name__ == "__main__":
    unittest.main()
