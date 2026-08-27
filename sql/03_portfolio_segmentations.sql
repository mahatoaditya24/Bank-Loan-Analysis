-- =============================================================================
-- 03_PORTFOLIO_SEGMENTATIONS.SQL
-- Multi-Dimensional Slicing: Temporal, Geographic, Terms, Purpose, & Employment
-- =============================================================================

-- 1. Monthly Issuance & Cash Flow Trend (Seasonality)
SELECT
    MONTH(issue_date) AS Month_Number,
    DATENAME(MONTH, issue_date) AS Month_Name,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND(AVG(int_rate) * 100, 2) AS Avg_Interest_Rate_Pct
FROM bank_loan_data
GROUP BY MONTH(issue_date), DATENAME(MONTH, issue_date)
ORDER BY Month_Number;

-- 2. Regional & State-Level Credit Distribution
SELECT
    address_state,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND(AVG(dti) * 100, 2) AS Avg_DTI_Pct,
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS State_Default_Rate_Pct
FROM bank_loan_data
GROUP BY address_state
ORDER BY Total_Funded_Amount DESC;

-- 3. Loan Term Breakdown (36 Months vs. 60 Months)
SELECT
    term,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND(AVG(int_rate) * 100, 2) AS Avg_Interest_Rate_Pct,
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS Default_Rate_Pct
FROM bank_loan_data
GROUP BY term
ORDER BY term;

-- 4. Borrower Employment Length Stability Analysis
SELECT
    emp_length,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND(AVG(annual_income), 2) AS Avg_Annual_Income,
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS Default_Rate_Pct
FROM bank_loan_data
GROUP BY emp_length
ORDER BY Total_Loan_Applications DESC;

-- 5. Loan Purpose Breakdown (Debt Consolidation, Credit Card, etc.)
SELECT
    purpose,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND(AVG(int_rate) * 100, 2) AS Avg_Interest_Rate_Pct
FROM bank_loan_data
GROUP BY purpose
ORDER BY Total_Funded_Amount DESC;

-- 6. Home Ownership Impact on Default Risk
SELECT
    home_ownership,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS Default_Rate_Pct
FROM bank_loan_data
GROUP BY home_ownership
ORDER BY Total_Loan_Applications DESC;
