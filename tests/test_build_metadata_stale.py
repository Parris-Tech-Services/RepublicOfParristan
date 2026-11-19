"""Test that docs/data/dashboard-metadata.json is not stale.

This test runs the build_metadata.py script in --check mode and expects it
to return exit code 0 (file is up to date). It will fail if any source file
has changed but the JSON has not been regenerated.

Run: python -m unittest tests.test_build_metadata_stale
"""
import subprocess
import sys
import unittest


class MetadataStalenessTests(unittest.TestCase):
    """Verify build_metadata.py reports no staleness."""

    def test_json_not_stale(self):
        """build_metadata.py --check must exit 0 when JSON is current."""
        result = subprocess.run(
            [sys.executable, "scripts/build_metadata.py", "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode, 0,
            f"metadata.json is STALE.\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )
        # Confirm helpful message was printed
        self.assertIn("up to date", result.stdout)


if __name__ == "__main__":
    unittest.main()
