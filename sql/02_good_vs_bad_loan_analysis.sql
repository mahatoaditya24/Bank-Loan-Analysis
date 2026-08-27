-- =============================================================================
-- 02_GOOD_VS_BAD_LOAN_ANALYSIS.SQL
-- Credit Risk Profiling: Performing (Good) vs. Non-Performing (Bad) Loans
-- Good Loans = 'Fully Paid' + 'Current'
-- Bad Loans  = 'Charged Off' (Defaulted)
-- =============================================================================

-- 1. Good Loan KPIs
SELECT
    -- Good Loan Application Percentage (~86.2%)
    ROUND((COUNT(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN id END) * 100.0) / COUNT(id), 2) AS Good_Loan_Pct,
    -- Good Loan Applications Count
    COUNT(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN id END) AS Good_Loan_Applications,
    -- Good Loan Total Funded Principal
    SUM(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN loan_amount ELSE 0 END) AS Good_Loan_Funded_Amount,
    -- Good Loan Total Cash Recovered
    SUM(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN total_payment ELSE 0 END) AS Good_Loan_Received_Amount,
    -- Good Loan Net Recovery Profit Margin
    SUM(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN total_payment - loan_amount ELSE 0 END) AS Good_Loan_Net_Profit
FROM bank_loan_data;

-- 2. Bad Loan KPIs (Credit Defaults)
SELECT
    -- Bad Loan Default Rate (~13.8%)
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS Bad_Loan_Default_Rate_Pct,
    -- Bad Loan Total Defaulted Applications
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) AS Bad_Loan_Applications,
    -- Bad Loan Total Disbursed at Risk
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS Bad_Loan_Funded_Amount,
    -- Bad Loan Total Amount Recovered Prior to Default
    SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) AS Bad_Loan_Received_Amount,
    -- Bad Loan Net Capital Loss / Charge-Off Severity
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount - total_payment ELSE 0 END) AS Bad_Loan_Net_Capital_Loss
FROM bank_loan_data;

-- 3. Detailed Status Grid View (Fully Paid vs. Charged Off vs. Current)
SELECT
    loan_status,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND(AVG(int_rate) * 100, 2) AS Avg_Interest_Rate_Pct,
    ROUND(AVG(dti) * 100, 2) AS Avg_DTI_Pct,
    ROUND(SUM(total_payment) / NULLIF(SUM(loan_amount), 0) * 100, 2) AS Capital_Recovery_Rate_Pct
FROM bank_loan_data
GROUP BY loan_status
ORDER BY Total_Funded_Amount DESC;
