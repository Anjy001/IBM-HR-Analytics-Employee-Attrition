# SQL

Plain SQL, written to be readable. All queries in `02_kpis.sql`,
`03_attrition_analysis.sql` and `04_advanced_analysis.sql` were **run and
verified** (SQLite) against the cleaned table and reconciled with the Python
results - see `05_reconciliation.sql` and `reports/03_methodology.md`.

## How to load the data

The scripts assume a table called `employees` built from
`data/processed/hr_cleaned.csv`:

```sql
-- PostgreSQL
CREATE TABLE employees (
    Age INT, Attrition TEXT, BusinessTravel TEXT, DailyRate INT,
    Department TEXT, DistanceFromHome INT, Education INT, EducationField TEXT,
    EnvironmentSatisfaction INT, Gender TEXT, HourlyRate INT, JobInvolvement INT,
    JobLevel INT, JobRole TEXT, JobSatisfaction INT, MaritalStatus TEXT,
    MonthlyIncome INT, MonthlyRate INT, NumCompaniesWorked INT, OverTime TEXT,
    PercentSalaryHike INT, PerformanceRating INT, RelationshipSatisfaction INT,
    StockOptionLevel INT, TotalWorkingYears INT, TrainingTimesLastYear INT,
    WorkLifeBalance INT, YearsAtCompany INT, YearsInCurrentRole INT,
    YearsSinceLastPromotion INT, YearsWithCurrManager INT,
    AttritionFlag INT, AgeBand TEXT, TenureBand TEXT,
    DistanceBand TEXT, IncomeBand TEXT
);

-- MySQL: LOAD DATA INFILE 'data/processed/hr_cleaned.csv' INTO TABLE employees
--   FIELDS TERMINATED BY ',' IGNORE 1 LINES;
-- SQLite: sqlite3 hr.db ".import --csv data/processed/hr_cleaned.csv employees"
```
