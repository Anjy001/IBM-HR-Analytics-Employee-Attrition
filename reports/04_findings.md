# Findings

All figures were computed on the 1,470-row dataset in this repository.

## Headline KPIs

| KPI | Value |
|---|---|
| Total employees | 1,470 |
| Employees who left | 237 |
| Attrition rate | 16.1% |
| Retention rate | 83.9% |
| Average age | 36.9 |
| Average monthly income | 6,503 (median 4,919) |
| Average tenure | 7.0 years |
| Overtime rate | 28.3% |
| Average job satisfaction | 2.73 / 4 |
| Average work-life balance | 2.76 / 4 |
| Average job involvement | 2.73 / 4 |

## 1. Attrition by job role

| Job role | Employees | Leavers | Attrition rate |
|---|---|---|---|
| Sales Representative | 83 | 33 | 39.8% |
| Laboratory Technician | 259 | 62 | 23.9% |
| Human Resources | 52 | 12 | 23.1% |
| Sales Executive | 326 | 57 | 17.5% |
| Research Scientist | 292 | 47 | 16.1% |
| Healthcare Representative | 131 | 9 | 6.9% |
| Manufacturing Director | 145 | 10 | 6.9% |
| Manager | 102 | 5 | 4.9% |
| Research Director | 80 | 2 | 2.5% |

## 2. Attrition by department

| Department | Employees | Leavers | Attrition rate |
|---|---|---|---|
| Sales | 446 | 92 | 20.6% |
| Human Resources | 63 | 12 | 19.0% |
| Research & Development | 961 | 133 | 13.8% |

## 3. Overtime - the single clearest driver

| OverTime | Employees | Leavers | Attrition rate |
|---|---|---|---|
| Yes | 416 | 127 | 30.5% |
| No | 1,054 | 110 | 10.4% |

## 4. Overtime x job role interaction

| Job role | Without OT | With OT | N (No / Yes) |
|---|---|---|---|
| Sales Representative | 28.8% | 66.7% | 59 / 24 |
| Laboratory Technician | 15.7% | 50.0% | 197 / 62 |
| Human Resources | 17.9% | 38.5% | 39 / 13 |
| Research Scientist | 7.2% | 34.0% | 195 / 97 |
| Sales Executive | 11.2% | 33.0% | 232 / 94 |
| Manager | 1.3% | 14.8% | 75 / 27 |
| Manufacturing Director | 5.7% | 10.3% | 106 / 39 |
| Healthcare Representative | 7.4% | 5.4% | 94 / 37 |
| Research Director | 1.8% | 4.3% | 57 / 23 |

Overtime is associated with higher attrition in 8 of 9 roles.

## 5. Tenure - attrition is an early-tenure phenomenon

| Tenure band | Employees | Leavers | Attrition rate |
|---|---|---|---|
| 0-1 yrs | 215 | 75 | 34.9% |
| 2-3 yrs | 255 | 47 | 18.4% |
| 4-5 yrs | 306 | 40 | 13.1% |
| 6-10 yrs | 448 | 55 | 12.3% |
| 11+ yrs | 246 | 20 | 8.1% |

## 6. Age band

| Age band | Employees | Leavers | Attrition rate |
|---|---|---|---|
| 18-25 | 123 | 44 | 35.8% |
| 26-35 | 606 | 116 | 19.1% |
| 56+ | 47 | 8 | 17.0% |
| 46-55 | 226 | 26 | 11.5% |
| 36-45 | 468 | 43 | 9.2% |

## 7. Compensation

| Income band | Employees | Leavers | Attrition rate |
|---|---|---|---|
| < 3k | 395 | 113 | 28.6% |
| 3k-6k | 519 | 66 | 12.7% |
| 6k-10k | 275 | 33 | 12.0% |
| 10k+ | 281 | 25 | 8.9% |

| StockOptionLevel | Employees | Leavers | Attrition rate |
|---|---|---|---|
| 0 | 631 | 154 | 24.4% |
| 3 | 85 | 15 | 17.6% |
| 1 | 596 | 56 | 9.4% |
| 2 | 158 | 12 | 7.6% |

## 8. The two cuts the dataset page explicitly asks for

### Mean distance from home by job role x attrition

| Job role | Stayed | Left | N stayed / left |
|---|---|---|---|
| Healthcare Representative | 9.2 | 17.7 | 122 / 9 |
| Human Resources | 6.6 | 13.4 | 40 / 12 |
| Sales Executive | 9.0 | 12.6 | 269 / 57 |
| Manager | 7.9 | 10.0 | 97 / 5 |
| Research Scientist | 8.9 | 9.8 | 245 / 47 |
| Laboratory Technician | 9.3 | 9.7 | 197 / 62 |
| Manufacturing Director | 9.5 | 8.8 | 135 / 10 |
| Sales Representative | 9.0 | 8.2 | 50 / 33 |
| Research Director | 8.5 | 7.0 | 78 / 2 |

Leavers commute farther in 6 of 9 roles, but several cells are very small
(Research Director = 2 leavers), so the pattern is directional rather than uniform.

### Mean monthly income by education x attrition

| Education | Stayed | Left | Difference |
|---|---|---|---|
| Below College | 5,926 | 4,360 | -1,566 |
| College | 6,586 | 4,283 | -2,303 |
| Bachelor | 6,883 | 4,770 | -2,113 |
| Master | 7,088 | 5,335 | -1,753 |
| Doctor | 8,560 | 5,850 | -2,710 |

At **every** education level, leavers earned less on average - a consistent
monotonic pattern rather than a single-group artefact.

## 9. Experience and satisfaction scales

| Variable | Lowest level | Highest level |
|---|---|---|
| JobInvolvement | Low 33.7% (83 / 28) | Very High 9.0% (144 / 13) |
| WorkLifeBalance | Bad 31.2% (80 / 25) | Better 14.2% (893 / 127) |
| EnvironmentSatisfaction | Low 25.4% (284 / 72) | Very High 13.5% (446 / 60) |
| JobSatisfaction | Low 22.8% (289 / 66) | Very High 11.3% (459 / 52) |
| RelationshipSatisfaction | Low 20.7% (276 / 57) | Very High 14.8% (432 / 64) |
| PerformanceRating | Excellent 16.1% (1,244 / 200) | Outstanding 16.4% (226 / 37) |

## 10. Other segments

* **Marital status:** Single 25.5% (470 / 120) - Married 12.5% (673 / 84) - Divorced 10.1% (327 / 33)
* **Business travel:** Frequently 24.9% (277 / 69) - Rarely 15.0% (1,043 / 156) - Non-Travel 8.0% (150 / 12)
* **Job level:** L1 26.3% (543 / 143) - L3 14.7% - L2 9.7% - L5 7.2% - L4 4.7%
* **Distance band:** 20+ 21.4% - 10-19 18.3% - 3-9 15.2% - 0-2 12.9%
* **Gender:** Male 17.0% (882 / 150) - Female 14.8% (588 / 87)
* **Education:** Below College 18.2% - Bachelor 17.3% - College 15.6% - Master 14.6% - Doctor 10.4%
* **Education field:** Human Resources 25.9% - Technical Degree 24.2% - Marketing 22.0% - Life Sciences 14.7% - Medical 13.6% - Other 13.4%

## 11. Statistical tests

### Chi-square (with Cramer's V effect size)

| Variable | Chi2 | p-value | Cramer's V | Verdict |
|---|---|---|---|---|
| OverTime | 87.56 | 8.2e-21 | 0.244 | Significant, strongest |
| JobRole | 86.19 | 2.8e-15 | 0.242 | Significant |
| JobLevel | 72.53 | 6.6e-15 | 0.222 | Significant |
| StockOptionLevel | 60.60 | 4.4e-13 | 0.203 | Significant |
| MaritalStatus | 46.16 | 9.5e-11 | 0.177 | Significant |
| JobInvolvement | 28.49 | 2.9e-06 | 0.139 | Significant |
| BusinessTravel | 24.18 | 5.6e-06 | 0.128 | Significant |
| EnvironmentSatisfaction | 22.50 | 5.1e-05 | 0.124 | Significant |
| JobSatisfaction | 17.51 | 0.00056 | 0.109 | Significant |
| WorkLifeBalance | 16.33 | 0.00097 | 0.105 | Significant |
| EducationField | 16.02 | 0.0068 | 0.104 | Significant (weak) |
| Department | 10.80 | 0.0045 | 0.086 | Significant (weak) |
| RelationshipSatisfaction | 5.24 | 0.155 | 0.060 | Not significant |
| Education | 3.07 | 0.546 | 0.046 | Not significant |
| Gender | 1.12 | 0.291 | 0.028 | Not significant |
| PerformanceRating | 0.00 | 0.990 | 0.000 | No association |

### Welch t-tests (leavers vs stayers)

| Variable | Leavers | Stayers | Cohen's d | p-value |
|---|---|---|---|---|
| TotalWorkingYears | 8.24 | 11.86 | -0.472 | 1.2e-11 |
| YearsInCurrentRole | 2.90 | 4.48 | -0.442 | 3.2e-11 |
| MonthlyIncome | 4,787 | 6,833 | -0.440 | 4.4e-13 |
| Age | 33.61 | 37.56 | -0.438 | 1.4e-08 |
| YearsWithCurrManager | 2.85 | 4.37 | -0.430 | 1.2e-10 |
| YearsAtCompany | 5.13 | 7.37 | -0.369 | 2.3e-07 |
| DistanceFromHome | 10.63 | 8.92 | +0.212 | 0.0041 |
| TrainingTimesLastYear | 2.62 | 2.83 | -0.162 | 0.0204 |
| DailyRate | 750.36 | 812.50 | -0.154 | 0.0300 |
| NumCompaniesWorked | 2.94 | 2.65 | +0.118 | 0.1163 (ns) |
| YearsSinceLastPromotion | 1.95 | 2.23 | -0.090 | 0.1987 (ns) |
| PercentSalaryHike | 15.10 | 15.23 | -0.037 | 0.6144 (ns) |
| MonthlyRate | 14,559 | 14,266 | +0.041 | 0.5653 (ns) |
| HourlyRate | 65.57 | 65.95 | -0.019 | 0.7914 (ns) |

### Correlation with attrition (point-biserial)

TotalWorkingYears -0.171 - YearsInCurrentRole -0.161 - MonthlyIncome -0.160 -
Age -0.159 - YearsWithCurrManager -0.156 - YearsAtCompany -0.134 -
TrainingTimesLastYear -0.059 - DailyRate -0.057 - YearsSinceLastPromotion -0.033 -
PercentSalaryHike -0.013 - HourlyRate -0.007 - MonthlyRate +0.015 -
NumCompaniesWorked +0.043 - **DistanceFromHome +0.078**

## 12. How I read all of this

Effect sizes are **small to moderate** (maximum Cohen's d ~ 0.47, maximum
Cramer's V ~ 0.24). These are real but not deterministic patterns. Attrition in
this dataset clusters around **early tenure, junior level, lower pay and high
workload** - a "start-of-career" pattern, not a single-cause problem.
