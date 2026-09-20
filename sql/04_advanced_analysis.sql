-- =====================================================================
-- 04 - ADVANCED ANALYSIS
-- CTEs, CASE, window functions, two-key grouping.
-- =====================================================================

-- ---- 1. The cut the dataset page asks for: income by education x attrition
-- (verified: Education 1 -> Yes 4360 / No 5926 ; Education 5 -> Yes 5850 / No 8560)
SELECT
    Education,
    Attrition,
    ROUND(AVG(MonthlyIncome), 0) AS avg_monthly_income,
    COUNT(*)                     AS employees
FROM employees
GROUP BY Education, Attrition
ORDER BY Education, Attrition DESC;

-- ---- 2. Education codes turned into readable labels with CASE
SELECT
    CASE Education
        WHEN 1 THEN 'Below College'
        WHEN 2 THEN 'College'
        WHEN 3 THEN 'Bachelor'
        WHEN 4 THEN 'Master'
        WHEN 5 THEN 'Doctor'
    END                                             AS education_level,
    COUNT(*)                                        AS employees,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY Education
ORDER BY attrition_rate_pct DESC;

-- ---- 3. Rank job roles by attrition rate (window function)
SELECT
    JobRole,
    COUNT(*)                                        AS employees,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct,
    RANK() OVER (ORDER BY 100.0 * SUM(AttritionFlag) / COUNT(*) DESC) AS attrition_rank
FROM employees
GROUP BY JobRole;

-- ---- 4. Overtime x job role interaction
-- (verified: Sales Rep 28.8% no OT vs 66.7% with OT)
SELECT
    JobRole,
    COUNT(*)                                                        AS employees,
    ROUND(100.0 * SUM(CASE WHEN OverTime = 'Yes' THEN AttritionFlag END)
          / NULLIF(SUM(CASE WHEN OverTime = 'Yes' THEN 1 END), 0), 1) AS attrition_with_overtime,
    ROUND(100.0 * SUM(CASE WHEN OverTime = 'No'  THEN AttritionFlag END)
          / NULLIF(SUM(CASE WHEN OverTime = 'No'  THEN 1 END), 0), 1) AS attrition_without_overtime
FROM employees
GROUP BY JobRole
ORDER BY attrition_with_overtime DESC;

-- ---- 5. Income band using CASE, then rate per band
SELECT
    CASE
        WHEN MonthlyIncome < 3000  THEN '<3k'
        WHEN MonthlyIncome < 6000  THEN '3k-6k'
        WHEN MonthlyIncome < 10000 THEN '6k-10k'
        ELSE '10k+'
    END                                             AS income_band,
    COUNT(*)                                        AS employees,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY income_band
ORDER BY attrition_rate_pct DESC;

-- ---- 6. Employees earning below their department average (CTE)
WITH department_average AS (
    SELECT Department, AVG(MonthlyIncome) AS dept_avg_income
    FROM employees
    GROUP BY Department
)
SELECT
    e.Department,
    COUNT(*)                AS employees_below_average,
    ROUND(AVG(e.MonthlyIncome), 0) AS avg_their_income,
    ROUND(d.dept_avg_income, 0)    AS dept_average_income
FROM employees e
JOIN department_average d ON e.Department = d.Department
WHERE e.MonthlyIncome < d.dept_avg_income
GROUP BY e.Department, d.dept_avg_income;
