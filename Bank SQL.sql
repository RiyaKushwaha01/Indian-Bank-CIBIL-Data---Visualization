CREATE DATABASE BANK_DB

USE BANK_DB

-----------------------------------TABLES-----------------------------------------------

SELECT count(*) FROM Internal_Data 

SELECT * FROM External_CIBIL_Data

---------------------------------------------------------------------DATA CLEANING------------------------------------------------------------------------------------

-- INTERNAL DATA

-- Missing Values in Internal Data
SELECT * FROM Internal_Data
WHERE Age_Newest_TL = -99999

-- Make a copy of original data
SELECT * INTO Internal_Bank_Data
FROM Internal_Data

-- Replace -99999 as NAN
UPDATE INTERNAL_BANK_DATA
SET
Age_Newest_TL = CASE WHEN Age_Newest_TL = -99999 THEN NULL ELSE Age_Newest_TL END,
Age_Oldest_TL = CASE WHEN Age_Oldest_TL = -99999 THEN NULL ELSE Age_Oldest_TL END
 
-- EXTERNAL CIBIL DATA

-- Missing Values in External Data
SELECT * FROM External_CIBIL_Data
WHERE time_since_first_deliquency = -99999


-- Make a copy of External_CIBIL_Data for cleaning as External_Data
SELECT * INTO External_Data
FROM External_CIBIL_Data

-- Replace -99999 as NAN

UPDATE External_Data
SET 
	time_since_recent_payment = CASE WHEN time_since_recent_payment = -99999 THEN NULL ELSE time_since_recent_payment END,
    time_since_first_deliquency = CASE WHEN time_since_first_deliquency = -99999 THEN NULL ELSE time_since_first_deliquency END,
    time_since_recent_deliquency = CASE WHEN time_since_recent_deliquency = -99999 THEN NULL ELSE time_since_recent_deliquency END,
    max_delinquency_level = CASE WHEN max_delinquency_level = -99999 THEN NULL ELSE max_delinquency_level END,
	max_deliq_6mts = CASE WHEN max_deliq_6mts = -99999 THEN NULL ELSE max_deliq_6mts END,
	max_deliq_12mts = CASE WHEN max_deliq_12mts = -99999 THEN NULL ELSE max_deliq_12mts END,
	tot_enq = CASE WHEN tot_enq = -99999 THEN NULL ELSE tot_enq END,
	CC_enq = CASE WHEN CC_enq = -99999 THEN NULL ELSE CC_enq END,
	CC_enq_L6m = CASE WHEN CC_enq_L6m = -99999 THEN NULL ELSE CC_enq_L6m END,
	CC_enq_L12m = CASE WHEN CC_enq_L12m = -99999 THEN NULL ELSE CC_enq_L12m END,
	PL_enq = CASE WHEN PL_enq = -99999 THEN NULL ELSE PL_enq END,
	PL_enq_L6m = CASE WHEN PL_enq_L6m = -99999 THEN NULL ELSE PL_enq_L6m END,
	PL_enq_L12m = CASE WHEN PL_enq_L12m = -99999 THEN NULL ELSE PL_enq_L12m END,
	time_since_recent_enq = CASE WHEN time_since_recent_enq = -99999 THEN NULL ELSE time_since_recent_enq END,
	enq_L12m = CASE WHEN enq_L12m = -99999 THEN NULL ELSE enq_L12m END,
	enq_L6m = CASE WHEN enq_L6m = -99999 THEN NULL ELSE enq_L6m END,
	enq_L3m = CASE WHEN enq_L3m = -99999 THEN NULL ELSE enq_L3m END,
	pct_currentBal_all_TL = CASE WHEN pct_currentBal_all_TL = -99999 THEN NULL ELSE pct_currentBal_all_TL END,
	CC_utilization = CASE WHEN CC_utilization = -99999 THEN NULL ELSE CC_utilization END,
	PL_utilization = CASE WHEN PL_utilization = -99999 THEN NULL ELSE PL_utilization END,
	max_unsec_exposure_inPct = CASE WHEN max_unsec_exposure_inPct = -99999 THEN NULL ELSE max_unsec_exposure_inPct END

-- Check the percentage of missing values
SELECT 
    COUNT(*) AS TotalRows,
    CAST(SUM(CASE WHEN time_since_recent_payment IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [time_since_recent_payment_PCT],
    CAST(SUM(CASE WHEN time_since_first_deliquency IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [time_since_first_deliquency_PCT],
    CAST(SUM(CASE WHEN time_since_recent_deliquency IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [time_since_recent_deliquency_PCT],
    CAST(SUM(CASE WHEN max_delinquency_level IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [max_delinquency_level_PCT],
    CAST(SUM(CASE WHEN max_deliq_6mts IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [max_deliq_6mts_PCT],
    CAST(SUM(CASE WHEN max_deliq_12mts IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [max_deliq_12mts_PCT],
    CAST(SUM(CASE WHEN tot_enq IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [tot_enq_PCT],
    CAST(SUM(CASE WHEN CC_enq IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [CC_enq_PCT],
    CAST(SUM(CASE WHEN CC_enq_L6m IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [CC_enq_L6m_PCT],
    CAST(SUM(CASE WHEN CC_enq_L12m IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [CC_enq_L12m_PCT],
    CAST(SUM(CASE WHEN PL_enq IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [PL_enq_PCT],
    CAST(SUM(CASE WHEN PL_enq_L6m IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [PL_enq_L6m_PCT],
    CAST(SUM(CASE WHEN PL_enq_L12m IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [PL_enq_L12m_PCT],
    CAST(SUM(CASE WHEN time_since_recent_enq IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [time_since_recent_enq_PCT],
    CAST(SUM(CASE WHEN enq_L12m IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [enq_L12m_PCT],
    CAST(SUM(CASE WHEN enq_L6m IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [enq_L6m_PCT],
    CAST(SUM(CASE WHEN enq_L3m IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [enq_L3m_PCT],
    CAST(SUM(CASE WHEN pct_currentBal_all_TL IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [pct_currentBal_all_TL_PCT],
    CAST(SUM(CASE WHEN CC_utilization IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [CC_utilization_PCT],
    CAST(SUM(CASE WHEN PL_utilization IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [PL_utilization_PCT],
    CAST(SUM(CASE WHEN max_unsec_exposure_inPct IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS [max_unsec_exposure_inPct_PCT]
FROM 
    External_Data


-- Remove the columns having missing greater then 40 percent
ALTER TABLE External_Data
DROP COLUMN 
    time_since_first_deliquency, 
    time_since_recent_deliquency,
    max_delinquency_level,
    CC_utilization,
    PL_utilization,
    max_unsec_exposure_inPct


------------------------------------------------------------------------------EDA OF INTERNAL DATA-----------------------------------------------------------------------

-- Exploratory Data Analysis

-- 1. No. of Rows in Internal Data Table

SELECT COUNT(*) AS NO_OF_ROWS FROM Internal_Data

-- 2. No. of Columns in Internal Data Table

SELECT COUNT(*) AS ColumnCount
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Internal_Data'

-- 3. Data types of all the columns

SELECT COLUMN_NAME,
DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Internal_Data'

-- 4. Number of Customers

SELECT COUNT(DISTINCT PROSPECTID) AS CUST_COUNT
FROM Internal_Data

-- 5. Average Trade line(credit accounts) per applicant
SELECT AVG(AVG_TL) AVG_ACCOUTS FROM 
(
	SELECT PROSPECTID, AVG(Total_TL)AS AVG_TL
	FROM Internal_Data
	GROUP BY PROSPECTID
) AS X

-- 6. Average number of TRADE LINES, Active accounts,Closed Accounts, TL_opened_L6M, TL_closed_L6M, TL_open_L12M, TL_closed_L12M
SELECT AVG(Total_TL) AS AVG_TRADE_LINE,
AVG(Tot_Active_TL) AS AVG_ACTIVE_TL,
AVG(Tot_Closed_TL) AS AVG_CLOSED_TL,
AVG(Total_TL_opened_L6M) AS AVG_OPEN_L6M_TL,
AVG(Tot_TL_closed_L6M) AS AVG_CLOSED_L6M_TL,
AVG(Total_TL_opened_L12M) AS AVG_OPEN_L12M,
AVG(Tot_TL_closed_L12M) AS AVG_CLOSED_L12M_TL
FROM Internal_Data


-- 7. Average active accounts per applicant
SELECT AVG(AVG_ACTIVE_TL) AS AVG_ACTIVE_ACCOUNTS FROM 
	(SELECT PROSPECTID, AVG(Tot_Active_TL)AS AVG_ACTIVE_TL
	FROM Internal_Data
	GROUP BY PROSPECTID) AS X

-- 8. Average closed/open accounts per applicant
SELECT AVG(CLOSED_TL) AS AVG_CLOSED_ACC FROM (
	SELECT PROSPECTID, AVG(Tot_Closed_TL) CLOSED_TL
	FROM Internal_Data
	GROUP BY PROSPECTID
	) AS X

-- 9. Average TL opened/closed in last 6 months per applicant
SELECT AVG(OPEN_TL_L6M) AS AVG_OPEN_ACC_L6M ,
	AVG(CLOSED_TL_L6M) AS AVG_CLOSED_ACC_L6M
	FROM (
	SELECT PROSPECTID, AVG(Total_TL_opened_L6M) OPEN_TL_L6M, AVG(Tot_TL_closed_L6M) CLOSED_TL_L6M
	FROM Internal_Data
	GROUP BY PROSPECTID
	) AS X
 
-- 10. Average TL open/CLOSED in last 12 months/ 1 year per applicants
SELECT AVG(OPEN_TL_L12M) AS AVG_OPEN_ACC_L12M,
	AVG(CLOSED_TL_L12M) AS AVG_CLOSED_ACC_L12M 
	FROM (
	SELECT PROSPECTID, AVG(Total_TL_opened_L12M) OPEN_TL_L12M,
	 AVG(Tot_TL_closed_L12M) CLOSED_TL_L12M
	FROM Internal_Data
	GROUP BY PROSPECTID
	) AS X

-- 11. Average missed payments per customer
SELECT AVG(AVG_MISSED_PMNT) AS AVG_MISSED_PAYMENT FROM (
	SELECT PROSPECTID, AVG(Tot_Missed_Pmnt) AVG_MISSED_PMNT
	FROM Internal_Data
	GROUP BY PROSPECTID
	) AS X

-- 12. Max missed payments
SELECT TOP 5 PROSPECTID, AVG(Tot_Missed_Pmnt) AVG_MISSED_PMNT
FROM Internal_Data
GROUP BY PROSPECTID
ORDER BY AVG_MISSED_PMNT DESC


-- 13. Average  Auto, CC(credit card) ,Consumer_TL, GOLD_TL, SECURED, UNSECURED, HOME, OTHER per customer
SELECT AVG(AVG_Consumer_TL) AS AVG_Consumer_TL ,
	AVG(AVG_AUTO_TL) AS AVG_AUTO_TL,
	AVG(AVG_CC)AS AVG_CC_TL,
	AVG(AVG_GOLD) AS AVG_GOLD_TL,
	AVG(AVG_PL) AS AVG_PL_TL,
	AVG(AVG_SECURED) AS AVG_SECURED_TL,
	AVG(AVG_UNSECURED_TL) AS AVG_UNSECURED_TL,
	AVG(AVG_HOME_TL) AS AVG_HOME_TL,
	AVG(AVG_OTHER_TL) AS AVG_OTHER_TL
	FROM 
	(
	SELECT PROSPECTID, AVG(Auto_TL) AS AVG_AUTO_TL,
	AVG(CC_TL) AS AVG_CC,
	AVG(Consumer_TL) AVG_Consumer_TL,
	AVG(Gold_TL) AS AVG_GOLD,
	AVG(PL_TL) AS AVG_PL,
	AVG(Secured_TL) AS AVG_SECURED,
	AVG(Unsecured_TL) AS AVG_UNSECURED_TL,
	AVG(Home_TL) AS AVG_HOME_TL,
	AVG(Other_TL) AS AVG_OTHER_TL
	FROM Internal_Data
	GROUP BY PROSPECTID
	) AS X 
 
--  14. 
SELECT AVG(AVG_AGE_NEWEST) FROM 
(
SELECT PROSPECTID, AVG(Age_Newest_TL) AVG_AGE_NEWEST
FROM Internal_Data
GROUP BY PROSPECTID
) AS X 

 
-----------------------------------------------------EDA FOR EXTERNAL CIBIL DATA---------------------------------------------------------------
-- 1. No. of Rows in External_CIBIL_data/ Total records

SELECT COUNT(*) AS NO_OF_ROWS 
FROM External_CIBIL_Data

-- 2. No. of Columns in External CIBIL Data

SELECT COUNT(*) AS ColumnCount
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'External_CIBIL_Data'
 
 -- 3. Data types of all the columns

SELECT COLUMN_NAME,
DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'External_CIBIL_Data'
 

-- 4. Max Credit Score
SELECT TOP 5 PROSPECTID, Credit_Score  
FROM External_CIBIL_Data
ORDER BY Credit_Score DESC

-- 5. Min Credit Score
SELECT TOP 5 PROSPECTID, Credit_Score  
FROM External_CIBIL_Data
ORDER BY Credit_Score 

-- 6. Average Credit Score
SELECT AVG(Credit_Score) AS AVG_SCORE
FROM External_CIBIL_Data
 
-- 7. Count Credit Score
SELECT COUNT(Credit_Score) AS COUNT_SCORE
FROM External_CIBIL_Data

-- 8. Max,Min, Average number of times the person was delinquent
SELECT MAX(num_times_delinquent) AS MAX_DELINQUENT,
	MIN(num_times_delinquent) AS MIN_DELINQUENT,
	AVG(num_times_delinquent) AS AVG_DELINQUENT
FROM External_CIBIL_Data

-- 9. Max,Min, Average number of times the person was delinquent in last 6 months
SELECT MAX(num_deliq_6mts) AS MAX_DELIQ_6M,
	MIN(num_deliq_6mts) AS MIN_DELIQ_6M,
	AVG(num_deliq_6mts) AS AVG_DELIQ_6M
FROM External_CIBIL_Data

-- 10. Max,Min, Average number of times the person was delinquent in last 12 months
SELECT MAX(num_deliq_12mts) AS MAX_DELIQ_12M,
	MIN(num_deliq_12mts) AS MIN_DELIQ_12M,
	AVG(num_deliq_12mts) AS AVG_DELIQ_12M
FROM External_CIBIL_Data

-- 11. Max,Min, Average Number of times payment was delayed BY 30 DAYS
SELECT MAX(num_times_30p_dpd) AS MAX_DPD,
	MIN(num_times_30p_dpd) AS MIN_DPD,
	AVG(num_times_30p_dpd) AS AVG_DPD
FROM External_CIBIL_Data

-- 12.  Max,Min, Average Number of times payment was delayed BY 60 DAYS
SELECT MAX(num_times_60p_dpd) AS MAX_DPD,
	MIN(num_times_60p_dpd) AS MIN_DPD,
	AVG(num_times_60p_dpd) AS AVG_DPD
FROM External_CIBIL_Data

-----------------------------------------RISK ANALYTICS----------------------------------------------------------------------------------

-----------------------Credit Risk Profiling

--1. Identify customers with a high percentage of missed payments
SELECT PROSPECTID, Tot_Missed_Pmnt
FROM Internal_Data
WHERE Tot_Missed_Pmnt > 3
ORDER BY Tot_Missed_Pmnt DESC

-- 2. Calculate risk score components (simple example)
SELECT PROSPECTID,  pct_active_tl,  pct_closed_tl,  Tot_Missed_Pmnt,
       CASE
         WHEN Tot_Missed_Pmnt > 5 THEN 'High Risk'
         WHEN Tot_Missed_Pmnt BETWEEN 2 AND 5 THEN 'Medium Risk'
         ELSE 'Low Risk'
       END AS Risk_Category
FROM Internal_Data
ORDER BY Risk_Category

-- 3. Customers who opened multiple new accounts in the last 6 months
SELECT PROSPECTID, Total_TL_opened_L6M
FROM Internal_Data
WHERE Total_TL_opened_L6M > 3

-- 4.Customers who closed multiple accounts recently
SELECT PROSPECTID, Tot_TL_closed_L6M
FROM Internal_Data
WHERE Tot_TL_closed_L6M > 2

-- 5. Customers with high number of unsecured loans
SELECT PROSPECTID, Unsecured_TL, Total_TL
FROM Internal_Data	
WHERE Unsecured_TL >= 3

-- 6. Ratio of secured vs unsecured
SELECT PROSPECTID,
       Secured_TL,
       Unsecured_TL,
       CAST(Unsecured_TL AS FLOAT) / NULLIF(Secured_TL, 0) AS Unsecured_to_Secured_Ratio
FROM Internal_Data

-- 7. Customers with old accounts but still missing payments
SELECT PROSPECTID, Age_Oldest_TL, Tot_Missed_Pmnt
FROM Internal_Data
WHERE Age_Oldest_TL > 24 AND Tot_Missed_Pmnt > 2



----------------- DESCRIPTIVE ANALYSIS

-- 1. Demographic profile:
-- Average age, income, and employment duration of applicants.

SELECT AVG(AGE) AS AVG_AGE,
	AVG(NETMONTHLYINCOME) AS AVG_INCOME,
	AVG(Time_With_Curr_Empr) AS AVG_EMPLOYMENT_DURATION
FROM External_CIBIL_Data

-- 2. Distribution of education levels, gender, and marital status, Loan Type.
--  Total Marital status
SELECT MARITALSTATUS, COUNT(PROSPECTID)
FROM External_CIBIL_Data
GROUP BY MARITALSTATUS

--  Total Education Value counts
SELECT Education, COUNT(PROSPECTID) AS VALUE_COUNTS
FROM External_CIBIL_Data 
GROUP BY EDUCATION

--  Total Gender
SELECT GENDER, COUNT(PROSPECTID) AS VALUE_COUNTS
FROM External_CIBIL_Data
GROUP BY GENDER

-- Distribution of Loan Type
SELECT first_prod_enq2, COUNT(PROSPECTID) AS VALUE_COUNTS
FROM External_CIBIL_Data	
GROUP BY first_prod_enq2


-- 3. Average number of credit enquires
SELECT AVG(tot_enq) AS AVG_ENQ,
	AVG(CC_enq)AS AVG_CC_ENQ,
	AVG(PL_enq) AS AVG_PL_ENQ
FROM External_CIBIL_Data

-- 4. Utilization rates (credit card, personal loans)
SELECT MAX(CC_utilization) AS MAX_CC_UTILIZATION,
	MIN(CC_utilization) AS MIN_CC_UTILIZATION,
	AVG(CC_utilization) AS AVG_CC_UTILIZATION,
	 MAX(PL_utilization) AS MAX_PL_UTILIZATION,
	MIN(PL_utilization) AS MIN_PL_UTILIZATION,
	AVG(PL_utilization) AS AVG_PL_UTILIZATION
FROM External_CIBIL_Data

-- 5. Count of customers with each type of loan (CC_Flag, PL_Flag, HL_Flag)
SELECT COUNT(DISTINCT PROSPECTID) Cust_with_each_type_loan
FROM External_CIBIL_Data
WHERE HL_Flag = 1 
  AND CC_Flag = 1 
  AND PL_Flag = 1

-- 6. Count/percentage of customers in each Approved_Flag category
SELECT Approved_Flag, COUNT(DISTINCT PROSPECTID) AS CUST ,
	COUNT(DISTINCT PROSPECTID) *100.0 / (SELECT COUNT(DISTINCT PROSPECTID) FROM External_CIBIL_Data) AS PERCENTAGE
FROM External_CIBIL_Data
GROUP BY Approved_Flag

-- 7. Distribution of Credit_Score by segment
SELECT 
    CASE 
        WHEN Credit_Score < 580 THEN 'Poor (<580)'
        WHEN Credit_Score BETWEEN 580 AND 669 THEN 'Fair (580-669)'
        WHEN Credit_Score BETWEEN 670 AND 739 THEN 'Good (670-739)'
        WHEN Credit_Score BETWEEN 740 AND 799 THEN 'Very Good (740-799)'
        ELSE 'Excellent (800+)' 
    END AS Credit_Score_Category,
    COUNT(*) AS Customer_Count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM External_CIBIL_Data), 2
    ) AS Percentage
FROM External_CIBIL_Data
GROUP BY CASE 
        WHEN Credit_Score < 580 THEN 'Poor (<580)'
        WHEN Credit_Score BETWEEN 580 AND 669 THEN 'Fair (580-669)'
        WHEN Credit_Score BETWEEN 670 AND 739 THEN 'Good (670-739)'
        WHEN Credit_Score BETWEEN 740 AND 799 THEN 'Very Good (740-799)'
        ELSE 'Excellent (800+)' 
    END
ORDER BY Customer_Count DESC

---------------------DIAGNOSTIC ANALYSIS

-- 1. Compare P1 vs P2 across: Income levels, Delinquency history, Enquiry frequency, Utilization levels

-- COMPARE INCOME LEVELS

-- Use a CTE to calculate median using PERCENTILE_CONT
WITH IncomeStats AS (
    SELECT Approved_Flag, NETMONTHLYINCOME,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY NETMONTHLYINCOME)
            OVER (PARTITION BY Approved_Flag) AS Median_Income
    FROM External_CIBIL_Data
    WHERE Approved_Flag IN ('P1', 'P2')
)

-- Final output: average + median per group
SELECT 
    Approved_Flag,
    COUNT(*) AS Customer_Count,
    AVG(NETMONTHLYINCOME) AS Avg_Income,
    MAX(Median_Income) AS Median_Income
FROM IncomeStats
GROUP BY Approved_Flag

-- Top 8 Applicants by NetIncome

SELECT TOP 8 PROSPECTID, SUM(NETMONTHLYINCOME) AS NETINCOME
FROM External_CIBIL_Data
GROUP BY PROSPECTID
ORDER BY NETINCOME DESC

-- BOTTOM 8 Applicants by NetIncome
SELECT TOP 8 PROSPECTID, SUM(NETMONTHLYINCOME) AS NETINCOME
FROM External_CIBIL_Data
GROUP BY PROSPECTID
HAVING SUM(NETMONTHLYINCOME) > 0
ORDER BY NETINCOME ASC

-- Top 10 Credit Scores

SELECT TOP 10 COUNT(PROSPECTID) AS Applicant_Count, Credit_Score 
FROM External_CIBIL_Data
GROUP BY Credit_Score
ORDER BY COUNT(PROSPECTID) DESC

--  Bottom	 10 Credit Scores

SELECT TOP 10 COUNT(PROSPECTID) AS Applicant_Count, Credit_Score 
FROM External_CIBIL_Data
GROUP BY Credit_Score
ORDER BY COUNT(PROSPECTID) ASC