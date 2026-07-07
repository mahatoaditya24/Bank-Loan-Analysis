
--1st Dashboard queries

--(Total loan Application)
SELECT * FROM bank_loan_data

SELECT COUNT(id) AS TOTAL_Applications FROM bank_loan_data



SELECT COUNT(id) AS MTD_TOTAL_Applications FROM bank_loan_data
WHERE MONTH(issue_date) = 12 and YEAR(issue_date) = 2021



SELECT COUNT(id) AS PMTD_TOTAL_Applications FROM bank_loan_data
WHERE MONTH(issue_date) = 11 and YEAR(issue_date) = 2021

--(MTD-PMTD/PMTD = MOM)

--(Total funded Amount)

SELECT SUM(loan_amount) AS Total_Funded_Amount From  bank_loan_data

SELECT SUM(loan_amount) AS MTD_Total_Funded_Amount From  bank_loan_data
WHERE MONTH(issue_date) = 12 and YEAR(issue_date) = 2021

SELECT SUM(loan_amount) AS PMTD_Total_Funded_Amount From  bank_loan_data
WHERE MONTH(issue_date) = 11 and YEAR(issue_date) = 2021

--Total amount Received

SELECT SUM(total_payment) AS Total_Amount_Received FROM bank_loan_data

SELECT SUM(total_payment) AS MTD_Total_Amount_Received FROM bank_loan_data
WHERE MONTH(issue_date) = 12 and YEAR(issue_date) = 2021

SELECT SUM(total_payment) AS PMTD_Total_Amount_Received FROM bank_loan_data
WHERE MONTH(issue_date) = 11 and YEAR(issue_date) = 2021

--Average Interest Rate

SELECT ROUND(AVG(int_rate),4) *100 AS Avg_Interest_Rate FROM bank_loan_data

SELECT ROUND(AVG(int_rate),4) *100 AS MTD_Avg_Interest_Rate FROM bank_loan_data
WHERE MONTH(issue_date) = 12 and YEAR(issue_date) = 2021

SELECT ROUND(AVG(int_rate),4) *100 AS PMTD_Avg_Interest_Rate FROM bank_loan_data
WHERE MONTH(issue_date) = 11 and YEAR(issue_date) = 2021

--DTI

SELECT Round(AVG(dti),4) *100 AS Avg_DTI FROM bank_loan_data

SELECT Round(AVG(dti),4) *100 AS MTD_Avg_DTI FROM bank_loan_data
WHERE MONTH(issue_date) = 12 and YEAR(issue_date) = 2021


SELECT Round(AVG(dti),4) *100 AS MTD_Avg_DTI FROM bank_loan_data
WHERE MONTH(issue_date) = 11 and YEAR(issue_date) = 2021

--Good loan Application percentage
SELECT 
      (COUNT(CASE WHEN loan_status = 'Fully Paid' OR loan_status = 'Current'THEN id END )*100)
      /
      COUNT(id) AS Good_loan_percentage From bank_loan_data

--Good loan Application
SELECT COUNT(id) AS Good_Loan_Application From bank_loan_data
WHERE loan_status = 'Fully Paid' OR loan_status = 'Current'

--Good loan Funded Amount
SELECT SUM(loan_amount) AS Good_Loan_Funded_Amount From bank_loan_data
WHERE loan_status = 'Fully Paid' OR loan_status = 'Current'

--Good loan Total Received Amount
SELECT SUM(total_payment) AS Good_Loan_Total_Received_Amount From bank_loan_data
WHERE loan_status = 'Fully Paid' OR loan_status = 'Current'

--Bad loan Application percentage
SELECT 
      (COUNT(CASE WHEN loan_status = 'Charged off' THEN id END )*100)
      /
      COUNT(id) AS Bad_loan_percentage From bank_loan_data

--Bad loan Application
SELECT COUNT(id) AS Bad_Loan_Application From bank_loan_data
WHERE loan_status = 'Charged off'

--Bad loan Funded Amount
SELECT SUM(loan_amount) AS Bad_Loan_Funded_Amount From bank_loan_data
WHERE loan_status = 'Charged off'

--Bad loan Total Received Amount
SELECT SUM(total_payment) AS Bad_Loan_Total_Received_Amount From bank_loan_data
WHERE loan_status = 'Charged off'

--Loan Status Grade View
SELECT 
      loan_status,
      COUNT(id) AS Total_Applications_,
      SUM(total_payment) AS Total_Amount_Received,
      SUM(loan_amount) AS Total_Funded_Amount,
      AVG(int_rate*100) AS Interesr_Rate,
      AVG(dti *100) AS DTI
      FROM bank_loan_data GROUP BY loan_status

 SELECT 
      loan_status,
      SUM(total_payment) AS MTD_Total_Amount_Received,
      SUM(loan_amount) AS MTD_Total_Funded_Amount
 FROM bank_loan_data
 WHERE MONTH(issue_date)=12
 GROUP BY loan_status


 --2nd dashboard queries

SELECT
      MONTH(issue_date) AS Month_Number,
      DATENAME (MONTH, issue_date) AS Month_Name,
      COUNT(id) AS Total_Loan_Applications,
      SUM(loan_amount) AS Total_Funded_Amount,
      SUM(total_payment) AS Total_Received_Amount
FROM bank_loan_data
GROUP BY  MONTH(issue_date), DATENAME (MONTH, issue_date)
ORDER BY   MONTH(issue_date)




SELECT
      address_state,
      COUNT(id) AS Total_Loan_Applications,
      SUM(loan_amount) AS Total_Funded_Amount,
      SUM(total_payment) AS Total_Received_Amount
FROM bank_loan_data
GROUP BY address_state
ORDER BY address_state



SELECT
      term,
      COUNT(id) AS Total_Loan_Applications,
      SUM(loan_amount) AS Total_Funded_Amount,
      SUM(total_payment) AS Total_Received_Amount
FROM bank_loan_data
GROUP BY term
ORDER BY term



SELECT
      emp_length,
      COUNT(id) AS Total_Loan_Applications,
      SUM(loan_amount) AS Total_Funded_Amount,
      SUM(total_payment) AS Total_Received_Amount
FROM bank_loan_data
GROUP BY emp_length
ORDER BY emp_length


SELECT
      purpose,
      COUNT(id) AS Total_Loan_Applications,
      SUM(loan_amount) AS Total_Funded_Amount,
      SUM(total_payment) AS Total_Received_Amount
FROM bank_loan_data
GROUP BY purpose
ORDER BY purpose




