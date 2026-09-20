-- =====================================================================
-- 02 - HEADLINE KPIs
-- Verified result: 1470 | 237 | 16.1 | 83.9
-- =====================================================================

-- Overall attrition
SELECT
    COUNT(*)                                        AS total_employees,
    SUM(AttritionFlag)                              AS leavers,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct,
    ROUND(100.0 * (COUNT(*) - SUM(AttritionFlag)) / COUNT(*), 1) AS retention_rate_pct
FROM employees;

-- Average salary, age and tenure
SELECT
    ROUND(AVG(MonthlyIncome), 0) AS avg_monthly_income,
    ROUND(AVG(Age), 1)           AS avg_age,
    ROUND(AVG(YearsAtCompany), 1) AS avg_tenure_years,
    ROUND(100.0 * SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                 AS overtime_rate_pct
FROM employees;

-- Average satisfaction scores (1-4 scales)
SELECT
    ROUND(AVG(JobSatisfaction), 2)         AS avg_job_satisfaction,
    ROUND(AVG(EnvironmentSatisfaction), 2) AS avg_environment_satisfaction,
    ROUND(AVG(WorkLifeBalance), 2)         AS avg_work_life_balance,
    ROUND(AVG(JobInvolvement), 2)          AS avg_job_involvement
FROM employees;
