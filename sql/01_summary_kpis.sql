-- =============================================================================
-- 01_SUMMARY_KPIS.SQL
-- Executive Key Performance Indicators for Retail Bank Loan Portfolio
-- Calculates Total Volume, Month-To-Date (MTD), Prior-MTD (PMTD), MoM Growth
-- =============================================================================

-- 1. Total Loan Applications
SELECT 
    COUNT(id) AS Total_Loan_Applications
FROM bank_loan_data;

-- 2. Month-to-Date (MTD) Total Loan Applications (December 2021)
SELECT 
    COUNT(id) AS MTD_Total_Applications
FROM bank_loan_data
WHERE MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021;

-- 3. Prior Month-to-Date (PMTD) Total Loan Applications (November 2021)
SELECT 
    COUNT(id) AS PMTD_Total_Applications
FROM bank_loan_data
WHERE MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021;

-- 4. Total Funded Capital (Disbursed Principal)
SELECT 
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN loan_amount ELSE 0 END) AS MTD_Funded_Amount,
    SUM(CASE WHEN MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021 THEN loan_amount ELSE 0 END) AS PMTD_Funded_Amount
FROM bank_loan_data;

-- 5. Total Cash Received (Repayments + Interest Collected)
SELECT 
    SUM(total_payment) AS Total_Amount_Received,
    SUM(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN total_payment ELSE 0 END) AS MTD_Amount_Received,
    SUM(CASE WHEN MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021 THEN total_payment ELSE 0 END) AS PMTD_Amount_Received
FROM bank_loan_data;

-- 6. Average Weighted Interest Rate & MoM Delta
SELECT 
    ROUND(AVG(int_rate) * 100, 2) AS Avg_Interest_Rate_Pct,
    ROUND(AVG(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN int_rate END) * 100, 2) AS MTD_Avg_Interest_Rate,
    ROUND(AVG(CASE WHEN MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021 THEN int_rate END) * 100, 2) AS PMTD_Avg_Interest_Rate
FROM bank_loan_data;

-- 7. Average Debt-to-Income (DTI) Ratio & Financial Leverage
SELECT 
    ROUND(AVG(dti) * 100, 2) AS Avg_DTI_Pct,
    ROUND(AVG(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN dti END) * 100, 2) AS MTD_Avg_DTI,
    ROUND(AVG(CASE WHEN MONTH(issue_date) = 11 AND YEAR(issue_date) = 2021 THEN dti END) * 100, 2) AS PMTD_Avg_DTI
FROM bank_loan_data;
