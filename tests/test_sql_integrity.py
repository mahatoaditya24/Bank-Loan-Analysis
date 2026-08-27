"""
Unit tests for SQL query files integrity.
Validates file presence, encoding, and core financial SQL syntax tokens.
"""

import os
import unittest


class TestSQLIntegrity(unittest.TestCase):
    """Test suite for modular SQL query files."""

    @classmethod
    def setUpClass(cls):
        cls.sql_dir = os.path.join(os.path.dirname(__file__), "..", "sql")

    def test_sql_files_exist(self):
        """Verify all modular SQL files exist."""
        expected_files = [
            "01_summary_kpis.sql",
            "02_good_vs_bad_loan_analysis.sql",
            "03_portfolio_segmentations.sql",
            "04_advanced_analytics.sql"
        ]
        for fname in expected_files:
            fpath = os.path.join(self.sql_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing SQL file: {fname}")

    def test_sql_keywords_presence(self):
        """Verify SQL files contain valid aggregation keywords."""
        for fname in os.listdir(self.sql_dir):
            if fname.endswith(".sql"):
                fpath = os.path.join(self.sql_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read().upper()
                self.assertIn("SELECT", content)
                self.assertIn("FROM", content)
                self.assertIn("BANK_LOAN_DATA", content)


if __name__ == "__main__":
    unittest.main()
