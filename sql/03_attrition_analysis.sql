-- =====================================================================
-- 03 - ATTRITION BY SEGMENT
-- Pairs every percentage with its group size, because a rate calculated on
-- a tiny group is weak evidence.
-- =====================================================================

-- Attrition by department  (verified: Sales 20.6 | HR 19.0 | R&D 13.8)
SELECT
    Department,
    COUNT(*)                                        AS employees,
    SUM(AttritionFlag)                              AS leavers,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;

-- Attrition by job role, only where the group is big enough to trust
-- (verified: Sales Rep 39.8 | Lab Tech 23.9 | HR 23.1 | Sales Exec 17.5)
SELECT
    JobRole,
    COUNT(*)                                        AS employees,
    SUM(AttritionFlag)                              AS leavers,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY JobRole
HAVING COUNT(*) >= 50
ORDER BY attrition_rate_pct DESC;

-- Overtime vs attrition  (verified: Yes 30.5% on 416 | No 10.4% on 1054)
SELECT
    OverTime,
    COUNT(*)                                        AS employees,
    SUM(AttritionFlag)                              AS leavers,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY OverTime
ORDER BY attrition_rate_pct DESC;

-- Attrition by marital status  (verified: Single 25.5 | Married 12.5 | Divorced 10.1)
SELECT
    MaritalStatus,
    COUNT(*)                                        AS employees,
    ROUND(100.0 * SUM(AttritionFlag) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY MaritalStatus
ORDER BY attrition_rate_pct DESC;
