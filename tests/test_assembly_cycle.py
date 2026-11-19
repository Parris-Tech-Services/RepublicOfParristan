"""End-to-end tests for tools/assembly_cycle.py.

Each test copies the repository into a temporary directory, runs a meeting
cycle there and, for the publishing tests, runs the real validators against
the result. The real repository is never modified.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import assembly_cycle as ac  # noqa: E402

ALL = ["Joshua Parris", "Glenn Peterson", "Matthew Walker", "Fred Carbunkle", "Jane Carbunkle"]


def copy_repo(dest):
    def ignore(_dir, names):
        return [n for n in names if n in (".git", "node_modules", "__pycache__")]
    shutil.copytree(REPO, dest, ignore=ignore)
    for p in (dest / "assembly" / "meetings").glob("*.json"):
        p.unlink()  # start each test with no meetings


class CycleTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        copy_repo(self.root)

    def held_meeting(self, present=ALL[:4], apologies=ALL[4:], acting_secretary="Glenn Peterson"):
        ac.schedule(self.root, "2026-12-08 19:30", "by video call")
        ac.record_notice(self.root, "2026-12-08", "2026-12-01 09:00", ["Matrix", "assembly@parristan.org"])
        ac.record_attendance(self.root, "2026-12-08", present, apologies, acting_secretary=acting_secretary)
        return "2026-12-08"

    def full_cycle(self):
        mid = self.held_meeting()
        ac.add_note(self.root, mid, 4, "The President reported progress on the five first-year goals.")
        ac.record_motion(self.root, mid, 5, "That the 2026-27 budget of A$114 be adopted.",
                         "2026-27 budget adopted", 4, 0, 0, "Fred Carbunkle", "Glenn Peterson")
        ac.record_motion(self.root, mid, 8, "That the Assembly buy a printed flag now.",
                         "Printed flag purchase", 1, 2, 1)
        ac.add_action(self.root, mid, "Jane Carbunkle", "Circulate symbols ballot", "2027-01-05")
        ac.add_action(self.root, mid, "Glenn Peterson", "Number founding members", "2026-12-20")
        ac.close_meeting(self.root, mid, "2026-12-08 20:40")
        ac.approve_minutes(self.root, mid, "2026-12-10", "written vote in the official channel", 5, 0, 0)
        return mid

    def validate(self):
        for script in ("validate_gazette.py", "validate_public_records.py"):
            r = subprocess.run([sys.executable, str(self.root / "scripts" / script)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{script} failed:\n{r.stdout}{r.stderr}")


class RulesTests(unittest.TestCase):
    def test_motion_results(self):
        self.assertEqual(ac.motion_result(3, 1, 0, 4), "Carried")
        self.assertEqual(ac.motion_result(2, 2, 1, 5), "Lost")          # tie fails
        self.assertEqual(ac.motion_result(2, 1, 2, 5), "Carried")       # abstentions not counted
        self.assertTrue(ac.motion_result(2, 0, 0, 5).startswith("Lost — fewer than three"))
        with self.assertRaises(ac.CycleError):
            ac.motion_result(3, 2, 0, 4)                                 # more votes than present
        with self.assertRaises(ac.CycleError):
            ac.motion_result(-1, 0, 0, 4)


class StepOrderTests(CycleTestBase):
    def test_notice_must_be_24_hours(self):
        ac.schedule(self.root, "2026-12-08 19:30", "by video call")
        with self.assertRaisesRegex(ac.CycleError, "24 hours"):
            ac.record_notice(self.root, "2026-12-08", "2026-12-07 20:00", ["Matrix"])
        ac.record_notice(self.root, "2026-12-08", "2026-12-07 19:30", ["Matrix"])  # exactly 24h is fine

    def test_cannot_skip_notice(self):
        ac.schedule(self.root, "2026-12-08 19:30", "by video call")
        with self.assertRaisesRegex(ac.CycleError, "stage 'scheduled'"):
            ac.record_attendance(self.root, "2026-12-08", ALL)

    def test_no_decisions_without_quorum(self):
        mid = self.held_meeting(present=ALL[:2], apologies=ALL[2:], acting_secretary="Glenn Peterson")
        with self.assertRaisesRegex(ac.CycleError, "quorum"):
            ac.record_motion(self.root, mid, 5, "x", "x", 2, 0, 0)

    def test_unknown_people_rejected(self):
        ac.schedule(self.root, "2026-12-08 19:30", "by video call")
        ac.record_notice(self.root, "2026-12-08", "2026-12-01 09:00", ["Matrix"])
        with self.assertRaisesRegex(ac.CycleError, "roster"):
            ac.record_attendance(self.root, "2026-12-08", ["Joshua Parris", "Someone Else", "Jane Carbunkle"])

    def test_absent_officer_needs_present_stand_in(self):
        ac.schedule(self.root, "2026-12-08 19:30", "by video call")
        ac.record_notice(self.root, "2026-12-08", "2026-12-01 09:00", ["Matrix"])
        with self.assertRaisesRegex(ac.CycleError, "acting secretary"):
            ac.record_attendance(self.root, "2026-12-08", ALL[:4], ALL[4:])
        with self.assertRaisesRegex(ac.CycleError, "must be present"):
            ac.record_attendance(self.root, "2026-12-08", ALL[:4], ALL[4:], acting_secretary="Jane Carbunkle")
        m = ac.record_attendance(self.root, "2026-12-08", ALL[:4], ALL[4:], acting_secretary="Fred Carbunkle")
        self.assertEqual(m["secretary"], "Fred Carbunkle")

    def test_mover_must_be_present(self):
        mid = self.held_meeting()
        with self.assertRaisesRegex(ac.CycleError, "not recorded as present"):
            ac.record_motion(self.root, mid, 5, "x", "x", 3, 0, 0, mover="Jane Carbunkle")

    def test_cannot_publish_unapproved_minutes(self):
        mid = self.held_meeting()
        ac.close_meeting(self.root, mid, "2026-12-08 20:30")
        with self.assertRaisesRegex(ac.CycleError, "minutes_approved"):
            ac.publish(self.root, mid, "2026-12-10")

    def test_minutes_approval_must_carry_and_follow_meeting(self):
        mid = self.held_meeting()
        ac.close_meeting(self.root, mid, "2026-12-08 20:30")
        with self.assertRaisesRegex(ac.CycleError, "before the meeting closed"):
            ac.approve_minutes(self.root, mid, "2026-12-07", "written vote", 5, 0, 0)
        with self.assertRaisesRegex(ac.CycleError, "Lost"):
            ac.approve_minutes(self.root, mid, "2026-12-10", "written vote", 1, 3, 0)

    def test_open_actions_carry_to_next_meeting(self):
        mid = self.held_meeting()
        ac.add_action(self.root, mid, "Fred Carbunkle", "Start ledger", "2026-12-15")
        ac.add_action(self.root, mid, "Jane Carbunkle", "Book room", "2026-12-15")
        ac.complete_action(self.root, f"A-{mid}-2", "2026-12-09")
        nxt = ac.schedule(self.root, "2027-01-12 19:30", "by video call")
        self.assertEqual(nxt["carried_actions"], [f"A-{mid}-1"])
        self.assertIn(f"A-{mid}-1", ac.render_notice(self.root, "2027-01-12"))


class PublishTests(CycleTestBase):
    def test_full_cycle_publishes_consistent_valid_records(self):
        mid = self.full_cycle()
        before = json.loads((self.root / "docs/data/decisions.json").read_text())["decisions"]
        number, ids = ac.publish(self.root, mid, "2026-12-10")

        self.assertEqual(number, "2026-016")
        self.assertEqual(ids, [f"FA-2026-{len(before) + 1:03d}", f"FA-2026-{len(before) + 2:03d}"])
        data = json.loads((self.root / "docs/data/decisions.json").read_text())
        self.assertEqual([d["id"] for d in data["decisions"][-2:]], ids)
        self.assertEqual(data["decisions"][-2]["result"], "4 YES / 0 NO / 0 ABSTAIN — Carried")
        self.assertEqual(data["decisions"][-1]["result"], "1 YES / 2 NO / 1 ABSTAIN — Lost")

        notice = (self.root / f"gazette/2026/{number}-assembly-meeting-{mid}.md").read_text()
        self.assertIn("**Status:** CONFIRMED", notice)
        self.assertIn("Quorum (at least 3):** met", notice)
        page = (self.root / f"docs/notices/{number}.html").read_text()
        self.assertIn("A-2026-12-08-1", page)
        self.assertIn('href="notices/2026-016.html" data-notice', (self.root / "docs/index.html").read_text())
        self.assertIn("Number founding members", (self.root / "docs/actions.html").read_text())
        self.assertEqual(ac.load(self.root, mid)["stage"], "published")
        self.validate()

    def test_cannot_publish_twice(self):
        mid = self.full_cycle()
        ac.publish(self.root, mid, "2026-12-10")
        with self.assertRaisesRegex(ac.CycleError, "stage 'published'"):
            ac.publish(self.root, mid, "2026-12-11")

    def test_action_completion_updates_public_page(self):
        mid = self.full_cycle()
        ac.publish(self.root, mid, "2026-12-10")
        ac.complete_action(self.root, f"A-{mid}-2", "2026-12-18")
        ac.write_actions_page(self.root)
        self.assertIn("Done 2026-12-18", (self.root / "docs/actions.html").read_text())
        self.validate()

    def test_records_contain_no_contact_details(self):
        mid = self.full_cycle()
        ac.publish(self.root, mid, "2026-12-10")
        record = (self.root / f"assembly/meetings/{mid}.json").read_text()
        for marker in ("@gmail", "phone", "address\"", "password"):
            self.assertNotIn(marker, record.lower())


if __name__ == "__main__":
    unittest.main()
