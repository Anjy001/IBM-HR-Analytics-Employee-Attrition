# Data Quality Report

Every check below was executed on the actual file. Nothing is assumed.

| # | Check | Method | Result | Verdict |
|---|---|---|---|---|
| 1 | Completeness | `df.isnull().sum().sum()` | 0 missing values in 35 columns | PASS |
| 2 | Uniqueness | `df.duplicated().sum()` | 0 duplicate rows | PASS |
| 3 | Primary key | `df["EmployeeNumber"].nunique()` | 1,470 unique values for 1,470 rows | PASS |
| 4 | Constant columns | `nunique() == 1` | `EmployeeCount`, `Over18`, `StandardHours` | ACTION: drop |
| 5 | Identifier columns | all values unique | `EmployeeNumber` | ACTION: drop |
| 6 | Target validity | `value_counts()` | 1,233 No / 237 Yes, no nulls | PASS (imbalanced) |
| 7 | Ordinal range checks | min / max per scale | all inside documented 1-5 / 1-4 bounds | PASS |
| 8 | Impossible values | negative age / income / tenure | none found | PASS |
| 9 | Categorical consistency | `unique()` on text columns | no variant spellings ("Yes"/"yes") | PASS |
| 10 | Leakage check | manual column review | no post-exit or attrition-derived variables | PASS |
| 11 | Outlier scan | descriptive statistics | extreme `MonthlyIncome` values are senior roles, not errors | KEEP |

## Conclusion

This is a **pre-cleaned teaching dataset**. The only cleaning needed was structural: I dropped 3 constant columns and
1 identifier column, and changed nothing else.

## Why I kept the outliers

`MonthlyIncome` is right-skewed (mean 6,503 vs median 4,919). The high values are
Director and Manager salaries - genuine business facts. Deleting them would bias
the compensation analysis downward and would remove the very senior group that
shows the *lowest* attrition. I kept them and analysed them explicitly instead of removing them quietly.

## Known limitations of the dataset itself

* Synthetic - it describes no real workforce.
* No dates, so no true trend, seasonality or survival analysis is possible.
* No exit reason, no exit date and no termination cost column.
* 1,470 rows is small for the number of variables (35) - overfitting risk is real.
* Several scales are discrete 1-4 / 1-5 ratings, which compress variance.
