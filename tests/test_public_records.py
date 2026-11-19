"""Standard-library tests for public decisions without sensitive member data."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "docs/data/decisions.json").read_text(encoding="utf-8"))

class PublicRecordTests(unittest.TestCase):
    def test_eleven_documented_fa_decisions(self):
        self.assertEqual([r["id"] for r in DATA["decisions"]],
                         [f"FA-2026-{i:03d}" for i in range(1, 12)])

    def test_no_fabricated_counts_for_unquantified_unanimity(self):
        for record in DATA["decisions"]:
            if record["id"] in ("FA-2026-003", "FA-2026-004"):
                self.assertEqual([record[k] for k in ("yes", "no", "abstain")],
                                 [None, None, None])

    def test_fully_reported_votes_have_consistent_count(self):
        for record in DATA["decisions"]:
            if record["yes"] is not None:
                self.assertEqual(sum(record[k] for k in ("yes", "no", "abstain")), 5)

    def test_public_sources_exist(self):
        for record in DATA["decisions"]:
            self.assertTrue((ROOT / record["source"]).is_file())

    def test_export_does_not_contain_member_credential_fields(self):
        serialized = json.dumps(DATA).lower()
        for secret in ('password', 'access_token', 'room_id', 'ballot_choice',
                       'private_email', 'residential_address'):
            self.assertNotIn('"' + secret + '"', serialized)

if __name__ == "__main__":
    unittest.main()
