-- =====================================================================
-- 05 - CROSS-CHECK: SQL vs PYTHON
-- Purpose: prove that two independent tools produce the SAME headline
-- numbers. If they disagreed, one pipeline would have a bug.
-- =====================================================================

-- Python reported: total=1470, leavers=237, attrition_rate=16.1
-- SQL result must match exactly.
SELECT
    COUNT(*)                                        AS total_employees,
    SUM(AttritionFlag)                              AS leavers,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees;

-- Python reported by department: Sales 20.6, Human Resources 19.0, R&D 13.8
SELECT
    Department,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;

-- Python reported by overtime: Yes 30.5, No 10.4
SELECT
    OverTime,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY OverTime
ORDER BY attrition_rate_pct DESC;
