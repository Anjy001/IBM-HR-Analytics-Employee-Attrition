"""Test whether the patterns I saw are real, and how large they are.

Two questions:
  1. Is a categorical variable independent of attrition?   -> chi-square
  2. Do leavers and stayers differ on a numeric variable?  -> Welch t-test

I report an effect size next to every p-value. With 1,470 rows a trivial
difference can still be "significant", and a p-value alone will not tell you
whether a difference is big enough to act on.
"""

import numpy as np
import pandas as pd
from scipy import stats

CLEAN_FILE = "data/processed/hr_cleaned.csv"
hr = pd.read_csv(CLEAN_FILE)


def chi_square_test(data, group_column):
    """Chi-square test of independence, plus Cramer's V as the effect size."""
    crosstab = pd.crosstab(data[group_column], data["AttritionFlag"])
    chi2, p_value, dof, expected = stats.chi2_contingency(crosstab)
    n = crosstab.values.sum()
    k = min(crosstab.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * k)) if k > 0 else np.nan
    return {"chi2": round(chi2, 2), "p_value": round(p_value, 6),
            "dof": int(dof), "cramers_v": round(cramers_v, 3)}


def ttest_numeric(data, numeric_column):
    """Welch t-test on leavers vs stayers, plus Cohen's d as the effect size."""
    leavers = data.loc[data["AttritionFlag"] == 1, numeric_column]
    stayers = data.loc[data["AttritionFlag"] == 0, numeric_column]
    t_stat, p_value = stats.ttest_ind(leavers, stayers, equal_var=False)
    pooled_sd = np.sqrt(((leavers.var(ddof=1) * (len(leavers) - 1)) +
                         (stayers.var(ddof=1) * (len(stayers) - 1))) /
                        (len(leavers) + len(stayers) - 2))
    cohens_d = (leavers.mean() - stayers.mean()) / pooled_sd
    return {"leaver_mean": round(leavers.mean(), 2),
            "stayer_mean": round(stayers.mean(), 2),
            "t": round(t_stat, 2), "p_value": round(p_value, 6),
            "cohens_d": round(cohens_d, 3)}


categorical_columns = ["Department", "JobRole", "OverTime", "MaritalStatus",
                       "BusinessTravel", "JobLevel", "Gender", "Education",
                       "EducationField", "JobSatisfaction", "EnvironmentSatisfaction",
                       "RelationshipSatisfaction", "WorkLifeBalance", "JobInvolvement",
                       "StockOptionLevel", "PerformanceRating"]

print("=== CHI-SQUARE TESTS ===")
for column in categorical_columns:
    print(column, chi_square_test(hr, column))

numeric_columns = ["Age", "DailyRate", "DistanceFromHome", "HourlyRate",
                   "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked",
                   "PercentSalaryHike", "TotalWorkingYears", "TrainingTimesLastYear",
                   "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion",
                   "YearsWithCurrManager"]

print("\n=== T-TESTS (leavers vs stayers) ===")
for column in numeric_columns:
    print(column, ttest_numeric(hr, column))

# Correlation with a 0/1 variable is the point-biserial correlation, which is
# just Pearson's r, so pandas gives it to me directly.
print("\n=== CORRELATION WITH ATTRITION ===")
correlation = hr[numeric_columns + ["AttritionFlag"]].corr()["AttritionFlag"]
print(correlation.drop("AttritionFlag").sort_values().to_string())
