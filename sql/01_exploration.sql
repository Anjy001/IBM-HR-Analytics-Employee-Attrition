-- =====================================================================
-- 01 - FIRST LOOK AT THE DATA
-- =====================================================================

-- How many rows and columns do we have?
SELECT COUNT(*) AS total_rows
FROM employees;

-- What does the data actually look like?
SELECT *
FROM employees
LIMIT 10;

-- Are there any NULL values in the key columns?
SELECT
    SUM(CASE WHEN MonthlyIncome IS NULL THEN 1 ELSE 0 END) AS null_income,
    SUM(CASE WHEN Department    IS NULL THEN 1 ELSE 0 END) AS null_department,
    SUM(CASE WHEN OverTime      IS NULL THEN 1 ELSE 0 END) AS null_overtime
FROM employees;

-- What distinct values exist in the low-cardinality columns?
SELECT DISTINCT Department FROM employees;
SELECT DISTINCT JobRole FROM employees ORDER BY JobRole;
SELECT DISTINCT OverTime FROM employees;
