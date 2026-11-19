"""Tests for docs/data/dashboard-metadata.json structure, consistency and PII safety."""
import json
import re
import unittest
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
METADATA_PATH = REPO_ROOT / "docs" / "data" / "dashboard-metadata.json"


class DashboardMetadataTests(unittest.TestCase):
    """Validate the dashboard metadata file format and invariants."""

    @classmethod
    def setUpClass(cls):
        with open(METADATA_PATH, encoding="utf-8") as f:
            cls.data = json.load(f)

    # ------------------------------------------------------------------ #
    #  Meta                                                              #
    # ------------------------------------------------------------------ #

    def test_meta_has_required_keys(self):
        meta = self.data["meta"]
        for key in ("title", "description", "updated", "source"):
            self.assertIn(key, meta, f"Missing meta key: {key}")
            self.assertTrue(len(meta[key]) > 0, f"meta.{key} is empty")

    def test_source_is_github_url(self):
        self.assertTrue(
            self.data["meta"]["source"].startswith("https://github.com/"),
            "meta.source should be a GitHub URL",
        )

    # ------------------------------------------------------------------ #
    #  KPI                                                               #
    # ------------------------------------------------------------------ #

    def test_kpi_has_all_counters(self):
        kpi = self.data["kpi"]
        expected = {
            "gazette_notices_published",
            "constitutional_instruments_ratified",
            "recorded_decisions",
            "elected_president",
            "interim_appointees",
            "operations_done",
            "operations_total",
            "founding_members",
        }
        self.assertEqual(set(kpi.keys()), expected,
                         "KPI must contain exactly these counters; got: " + str(kpi.keys()))

    def test_kpi_values_are_non_negative_ints(self):
        for key, val in self.data["kpi"].items():
            self.assertIsInstance(val, int, f"kpi.{key} should be an int")
            self.assertGreaterEqual(val, 0, f"kpi.{key} should be non-negative")

    def test_notice_count_matches_index(self):
        """Real index lists 9 Gazette notices (2026-001 through 2026-009)."""
        idx_path = REPO_ROOT / "gazette" / "INDEX.md"
        lines = idx_path.read_text(encoding="utf-8").splitlines()
        noticed_ids = []
        for line in lines:
            m = re.search(r'\[(\d{4}-\d+)\]', line)
            if m:
                noticed_ids.append(m.group(1))
        unique = list(dict.fromkeys(noticed_ids))  # preserve order, dedup
        self.assertEqual(
            len(unique),
            self.data["kpi"]["gazette_notices_published"],
            f"Gazette count mismatch: index has {len(unique)} notices but kpi says "
            f"{self.data['kpi']['gazette_notices_published']}",
        )

    def test_constitution_ratified_flag(self):
        """Constitution was unanimously ratified; this must not show zero."""
        self.assertGreater(
            self.data["kpi"]["constitutional_instruments_ratified"], 0,
            "Dashboard must reflect constitution ratification",
        )

    def test_no_false_election_claim(self):
        """No President has been elected yet."""
        self.assertEqual(
            self.data["kpi"]["elected_president"], 0,
            "Dashboard must not claim a President until actual election completes",
        )

    def test_operations_counts_consistent(self):
        self.assertEqual(
            self.data["kpi"]["operations_done"],
            20,  # verified via grep against NATIONAL_OPERATIONS_TODO.md
        )
        self.assertEqual(
            self.data["kpi"]["operations_total"],
            41,
        )
        self.assertLessEqual(len(self.data.get("operations", [])),
                             self.data["kpi"]["operations_total"] -
                             self.data["kpi"]["operations_done"],
                             "Displayed pending ops should not exceed remaining total")

    # ------------------------------------------------------------------ #
    #  Roadmap                                                           #
    # ------------------------------------------------------------------ #

    def test_roadmap_steps_ordered(self):
        steps = self.data["roadmap"]
        for i, step in enumerate(steps):
            self.assertEqual(step["step"], i + 1,
                             f"Roadmap steps must be sequential; step {i+1} has step={step['step']}")

    def test_roadmap_valid_statuses(self):
        valid = {"complete", "in_progress", "pending", "future"}
        for step in self.data["roadmap"]:
            self.assertIn(
                step["status"], valid,
                f'Roadmap step {step["step"]} has invalid status "{step["status"]}"',
            )

    def test_roadmap_step3_reflects_ratification(self):
        """Step 3 (ratify constitution) must be complete after FA adoption."""
        step3 = [s for s in self.data["roadmap"] if s["step"] == 3][0]
        self.assertEqual(step3["status"], "complete",
                         "Constitutional ratification (step 3) must be marked complete")

    # ------------------------------------------------------------------ #
    #  Decisions                                                         #
    # ------------------------------------------------------------------ #

    def test_decisions_match_decision_register(self):
        """Decision Register lists 8 resolutions (FA-2026-001 through FA-2026-008)."""
        self.assertEqual(len(self.data["decisions"]), 8)
        for i, d in enumerate(self.data["decisions"]):
            expected_id = f"FA-2026-{i+1:03d}"
            self.assertEqual(d["id"], expected_id,
                             f'Decision ID mismatch: expected {expected_id}, got {d["id"]}')
            self.assertIn("text", d)
            self.assertIn("vote", d)

    def test_decisions_dates_are_iso(self):
        from datetime import date
        for d in self.data["decisions"]:
            date.fromisoformat(d["date"])

    # ------------------------------------------------------------------ #
    #  Officeholders                                                     #
    # ------------------------------------------------------------------ #

    def test_officeholders_list(self):
        holders = self.data["officeholders"]
        roles = {h["role"] for h in holders}
        self.assertIn("President", roles)
        self.assertIn("Returning Officer", roles)
        pres = [h for h in holders if h["role"] == "President"][0]
        self.assertEqual(pres["name"], "Not elected")

    def test_returning_officer_identified(self):
        ro = [h for h in self.data["officeholders"] if h["role"] == "Returning Officer"][0]
        self.assertIn("matthew", ro["name"].lower())
        self.assertIsNotNone(ro["started"])

    # ------------------------------------------------------------------ #
    #  Election timetable                                                #
    # ------------------------------------------------------------------ #

    def test_election_timetable_fields(self):
        et = self.data["election_timetable"]
        required = ["nominations_open", "nominations_close", "voting_start",
                     "voting_end", "returning_officer", "status"]
        for field in required:
            self.assertIn(field, et, f"Election timetable missing field: {field}")

    def test_election_nomination_before_voting(self):
        et = self.data["election_timetable"]
        nom_close = date.fromisoformat(et["nominations_close"])
        vote_start = date.fromisoformat(et["voting_start"])
        self.assertLess(nom_close, vote_start,
                        "Nominations should close before voting starts")

    # ------------------------------------------------------------------ #
    #  Symbols                                                           #
    # ------------------------------------------------------------------ #

    def test_symbols_have_names_and_images(self):
        for s in self.data["symbols"]:
            self.assertTrue(len(s["name"]) > 0, "Each symbol needs a name")
            self.assertIn("image", s)
            self.assertTrue(len(s["image"]) > 0, "Symbol image path is empty")

    # ------------------------------------------------------------------ #
    #  Tech stack                                                        #
    # ------------------------------------------------------------------ #

    def test_tech_stack_has_both_reference_models(self):
        ts = self.data["tech_stack"]
        self.assertIn("gendarmerie", ts)
        self.assertIn("schleswig_holstein", ts)

    def test_tech_items_have_progress(self):
        for region in self.data["tech_stack"].values():
            for item in region["items"]:
                self.assertIn("progress", item)
                self.assertIsInstance(item["progress"], int)
                self.assertLessEqual(item["progress"], 100)
                self.assertGreaterEqual(item["progress"], 0)

    # ------------------------------------------------------------------ #
    #  Institution health                                                #
    # ------------------------------------------------------------------ #

    def test_health_entries_reference_real_files(self):
        inst_dir = REPO_ROOT / "institutions"
        docs_dir = REPO_ROOT / "docs"
        for inst in self.data["institution_health"]:
            target = inst_dir / inst["file"]
            if not target.exists():
                target = docs_dir / inst["file"]
            self.assertTrue(target.exists(),
                            f"Institution references missing file: {inst['file']}")

    def test_health_contains_ratified_constitution(self):
        names = {inst["institution"].lower() for inst in self.data["institution_health"]}
        self.assertTrue(any("constitution" in n for n in names),
                        "Health register must include Constitution entry")

    # ------------------------------------------------------------------ #
    #  PII safety                                                        #
    # ------------------------------------------------------------------ #

    def test_no_sensitive_data_exposed(self):
        """Dashboard must never expose personal/member data patterns.

        Checks for phone-number and email-address patterns plus common PII terms.
        Allows known tool/software names like 'Thobys Email' without false positives.
        """
        raw = METADATA_PATH.read_text(encoding="utf-8")
        # Phone number pattern
        self.assertIsNone(re.search(r"\b\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b", raw),
                          "Contains phone number pattern")
        # Email address pattern (real addresses only, not software names)
        self.assertIsNone(re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", raw),
                          "Contains email address pattern")
        # Common PII terms (word-bounded, case-insensitive)
        pii_terms = [r"\bhome\s+address\b", r"\bbirth\s+date\b", r"\bssn\b",
                     r"\bid\s+document\b", r"\bprivate\s+contact\b"]
        for pat in pii_terms:
            self.assertIsNone(
                re.search(pat, raw, re.IGNORECASE),
                f"Dashboard metadata contains PII reference: '{pat}'",
            )

    # ------------------------------------------------------------------ #
    #  JSON validity                                                      #
    # ------------------------------------------------------------------ #

    def test_file_is_parseable_json(self):
        text = METADATA_PATH.read_text(encoding="utf-8")
        json.loads(text)  # raises if invalid

    def test_file_under_docs_directory(self):
        self.assertTrue(str(REPO_ROOT / "docs") in str(METADATA_PATH),
                        "Metadata should be under docs/")


if __name__ == "__main__":
    unittest.main()
