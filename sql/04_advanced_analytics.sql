-- =============================================================================
-- 04_ADVANCED_ANALYTICS.SQL
-- Credit Grade Risk Pricing, Sub-Grade Heatmaps & Loss Severity Analysis
-- =============================================================================

-- 1. Credit Grade Performance & Default Risk Profile (Grade A through G)
SELECT
    grade,
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Received_Amount,
    ROUND(AVG(int_rate) * 100, 2) AS Avg_Interest_Rate_Pct,
    ROUND(AVG(dti) * 100, 2) AS Avg_DTI_Pct,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) AS Default_Count,
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS Default_Rate_Pct,
    ROUND(SUM(total_payment) / NULLIF(SUM(loan_amount), 0) * 100, 2) AS Recovery_Rate_Pct
FROM bank_loan_data
GROUP BY grade
ORDER BY grade;

-- 2. Sub-Grade Granular Risk Heatmap
SELECT
    grade,
    sub_grade,
    COUNT(id) AS Total_Applications,
    ROUND(AVG(int_rate) * 100, 2) AS Avg_Interest_Rate,
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS Default_Rate_Pct
FROM bank_loan_data
GROUP BY grade, sub_grade
ORDER BY grade, sub_grade;

-- 3. Debt-to-Income (DTI) Tier vs. Default Risk Matrix
SELECT
    CASE
        WHEN dti < 0.10 THEN 'Tier 1: Low DTI (<10%)'
        WHEN dti BETWEEN 0.10 AND 0.20 THEN 'Tier 2: Moderate DTI (10%-20%)'
        WHEN dti BETWEEN 0.20 AND 0.30 THEN 'Tier 3: Elevated DTI (20%-30%)'
        ELSE 'Tier 4: High Risk DTI (>30%)'
    END AS DTI_Risk_Tier,
    COUNT(id) AS Total_Loans,
    SUM(loan_amount) AS Total_Funded_Amount,
    ROUND((COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / COUNT(id), 2) AS Default_Rate_Pct
FROM bank_loan_data
GROUP BY 
    CASE
        WHEN dti < 0.10 THEN 'Tier 1: Low DTI (<10%)'
        WHEN dti BETWEEN 0.10 AND 0.20 THEN 'Tier 2: Moderate DTI (10%-20%)'
        WHEN dti BETWEEN 0.20 AND 0.30 THEN 'Tier 3: Elevated DTI (20%-30%)'
        ELSE 'Tier 4: High Risk DTI (>30%)'
    END
ORDER BY DTI_Risk_Tier;
