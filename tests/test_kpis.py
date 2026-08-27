"""
Unit tests for Bank Loan Portfolio & Credit Risk Analytics Engine.
Validates metric accuracy, Good vs. Bad loan splits, DTI thresholds, and EMI calculations.
Compatible with standard unittest and pytest.
"""

import os
import unittest
import pandas as pd


class TestBankLoanAnalytics(unittest.TestCase):
    """Test suite for Bank Loan financial and risk analytics."""

    @classmethod
    def setUpClass(cls):
        """Load dataset once for all tests."""
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        parquet_path = os.path.join(data_dir, "bank_loan_data.parquet")
        csv_path = os.path.join(data_dir, "bank_loan_data.csv.gz")

        if os.path.exists(parquet_path):
            cls.df = pd.read_parquet(parquet_path)
        elif os.path.exists(csv_path):
            cls.df = pd.read_csv(csv_path, compression="gzip")
        else:
            raise FileNotFoundError("Dataset file not found in data/ directory.")

        cls.df["issue_date"] = pd.to_datetime(cls.df["issue_date"])
        cls.df["is_good_loan"] = cls.df["loan_status"].apply(lambda s: 1 if s in ["Fully Paid", "Current"] else 0)
        cls.df["is_bad_loan"] = cls.df["loan_status"].apply(lambda s: 1 if s == "Charged Off" else 0)

    def test_dataset_record_count(self):
        """Verify total record count matches portfolio baseline (38,576 records)."""
        self.assertEqual(len(self.df), 38576, f"Expected 38,576 records, found {len(self.df)}")

    def test_good_vs_bad_loan_partition(self):
        """Verify Good and Bad loan statuses form a mutually exclusive partition of the portfolio."""
        good_count = self.df["is_good_loan"].sum()
        bad_count = self.df["is_bad_loan"].sum()
        total_count = len(self.df)

        self.assertEqual(good_count + bad_count, total_count, "Good loans and Bad loans must sum up to total records")
        good_pct = (good_count / total_count) * 100
        bad_pct = (bad_count / total_count) * 100

        # Good loan percentage should be ~86.2% and Bad loan percentage ~13.8%
        self.assertTrue(80.0 <= good_pct <= 90.0, f"Expected Good Loan % between 80-90%, got {good_pct:.2f}%")
        self.assertTrue(10.0 <= bad_pct <= 20.0, f"Expected Bad Loan % between 10-20%, got {bad_pct:.2f}%")

    def test_positive_financial_values(self):
        """Verify all loan amounts, payments, and interest rates are strictly positive numbers."""
        self.assertTrue((self.df["loan_amount"] > 0).all(), "Found non-positive loan amounts")
        self.assertTrue((self.df["total_payment"] >= 0).all(), "Found negative payment amounts")
        self.assertTrue((self.df["int_rate"] > 0).all(), "Found non-positive interest rates")
        self.assertTrue((self.df["dti"] >= 0).all(), "Found negative DTI values")

    def test_credit_grades_domain(self):
        """Verify valid standard credit grade assignments (A through G)."""
        expected_grades = {"A", "B", "C", "D", "E", "F", "G"}
        unique_grades = set(self.df["grade"].unique())
        self.assertTrue(unique_grades.issubset(expected_grades), f"Unexpected credit grades: {unique_grades - expected_grades}")

    def test_emi_amortization_formula(self):
        """Verify standard monthly EMI amortization formula mathematics."""
        principal = 10000.0
        annual_rate = 12.0  # 12% APR
        term_months = 36    # 3 years

        monthly_r = (annual_rate / 100.0) / 12.0  # 0.01 per month
        numerator = principal * monthly_r * ((1 + monthly_r) ** term_months)
        denominator = ((1 + monthly_r) ** term_months) - 1
        emi = numerator / denominator

        # Standard known EMI for $10,000 at 12% for 36 months is ~$332.14
        self.assertEqual(round(emi, 2), 332.14, f"Expected EMI $332.14, got {emi:.2f}")
        self.assertTrue(emi * term_months > principal, "Total repayment must exceed principal")


if __name__ == "__main__":
    unittest.main()
