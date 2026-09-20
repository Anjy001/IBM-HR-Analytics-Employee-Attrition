# Data Dictionary

**Dataset:** IBM HR Analytics Employee Attrition & Performance
**Rows:** 1,470  **Columns:** 35  **Missing values:** 0  **Duplicate rows:** 0
**Nature:** fictional / synthetic dataset created by IBM data scientists.

| # | Column | Meaning | Type | Values / Range | Use in model | Use in dashboard |
|---|---|---|---|---|---|---|
| 1 | Age | Employee age | Numeric | 18-60 | Yes | Yes |
| 2 | Attrition | Left the company | Binary (target) | Yes / No (237 Yes) | Target | Yes |
| 3 | BusinessTravel | Travel frequency | Nominal | Non-Travel, Travel_Rarely, Travel_Frequently | Yes | Yes |
| 4 | DailyRate | Daily pay rate | Numeric | 102-1,499 | Weak | Rarely |
| 5 | Department | Business function | Nominal | Sales, R&D, Human Resources | Yes | Yes |
| 6 | DistanceFromHome | Commute distance | Numeric | 1-29 | Yes | Yes |
| 7 | Education | Education level | Ordinal | 1-5 (Below College -> Doctor) | Yes | Yes |
| 8 | EducationField | Field of study | Nominal | 6 values | Yes | Yes |
| 9 | EmployeeCount | Constant value 1 | Constant | 1 | Dropped | Dropped |
| 10 | EmployeeNumber | Unique employee key | Identifier | 1-2068 | Dropped | Dropped |
| 11 | EnvironmentSatisfaction | Environment satisfaction | Ordinal | 1-4 (Low -> Very High) | Yes | Yes |
| 12 | Gender | Gender | Nominal | Male, Female | Yes (fairness audit) | Yes |
| 13 | HourlyRate | Hourly pay | Numeric | 30-100 | Weak | No |
| 14 | JobInvolvement | Job involvement | Ordinal | 1-4 (Low -> Very High) | Yes | Yes |
| 15 | JobLevel | Seniority level | Ordinal | 1-5 | Yes | Yes |
| 16 | JobRole | Role title | Nominal | 9 values | Yes | Yes |
| 17 | JobSatisfaction | Job satisfaction | Ordinal | 1-4 | Yes | Yes |
| 18 | MaritalStatus | Marital status | Nominal | Single, Married, Divorced | Yes (with care) | Yes |
| 19 | MonthlyIncome | Monthly salary | Numeric | 1,009-19,999 | Yes | Yes |
| 20 | MonthlyRate | Monthly rate | Numeric | 2,094-26,999 | Weak | No |
| 21 | NumCompaniesWorked | Previous employers | Numeric | 0-9 | Yes | Yes |
| 22 | Over18 | Constant value Y | Constant | Y | Dropped | Dropped |
| 23 | OverTime | Works overtime | Binary | Yes / No | Yes | Yes |
| 24 | PercentSalaryHike | Last salary increase % | Numeric | 11-25 | Weak | No |
| 25 | PerformanceRating | Performance score | Ordinal | 3 / 4 only | Weak | Yes |
| 26 | RelationshipSatisfaction | Relationship satisfaction | Ordinal | 1-4 | Yes | Yes |
| 27 | StandardHours | Constant value 80 | Constant | 80 | Dropped | Dropped |
| 28 | StockOptionLevel | Stock option level | Ordinal | 0-3 | Yes | Yes |
| 29 | TotalWorkingYears | Total experience | Numeric | 0-40 | Yes | Yes |
| 30 | TrainingTimesLastYear | Trainings attended | Numeric | 0-6 | Yes | Yes |
| 31 | WorkLifeBalance | Work-life balance rating | Ordinal | 1-4 (Bad -> Best) | Yes | Yes |
| 32 | YearsAtCompany | Tenure | Numeric | 0-40 | Yes | Yes |
| 33 | YearsInCurrentRole | Time in current role | Numeric | 0-18 | Yes | Yes |
| 34 | YearsSinceLastPromotion | Time since promotion | Numeric | 0-15 | Yes | Yes |
| 35 | YearsWithCurrManager | Time with current manager | Numeric | 0-17 | Yes | Yes |

## Columns I added

| Column | How it was built | Purpose |
|---|---|---|
| `AttritionFlag` | 1 if `Attrition == "Yes"` else 0 | Numeric target variable |
| `AgeBand` | `pd.cut(Age, [17,25,35,45,55,65])` | Readable age groups |
| `TenureBand` | `pd.cut(YearsAtCompany, [-1,1,3,5,10,40])` | Career-lifecycle view |
| `DistanceBand` | `pd.cut(DistanceFromHome, [-1,2,9,19,29])` | Commute tiers |
| `IncomeBand` | `pd.cut(MonthlyIncome, [0,3000,6000,10000,20000])` | Pay brackets |

## Documented value labels (from the dataset documentation)

| Scale | Values |
|---|---|
| Education | 1 Below College, 2 College, 3 Bachelor, 4 Master, 5 Doctor |
| EnvironmentSatisfaction | 1 Low, 2 Medium, 3 High, 4 Very High |
| JobInvolvement | 1 Low, 2 Medium, 3 High, 4 Very High |
| JobSatisfaction | 1 Low, 2 Medium, 3 High, 4 Very High |
| PerformanceRating | 1 Low, 2 Good, 3 Excellent, 4 Outstanding |
| RelationshipSatisfaction | 1 Low, 2 Medium, 3 High, 4 Very High |
| WorkLifeBalance | 1 Bad, 2 Good, 3 Better, 4 Best |
