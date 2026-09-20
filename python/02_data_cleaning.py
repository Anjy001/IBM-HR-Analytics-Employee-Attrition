"""Clean the data and write the analysis-ready file.

I never edit the raw file: it is read, cleaned in memory, and the result is
written to data/processed/ so the original stays recoverable.
"""

import pandas as pd

RAW_FILE = "data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"
CLEAN_FILE = "data/processed/hr_cleaned.csv"

employees = pd.read_csv(RAW_FILE)


def find_constant_columns(data):
    """Return the columns that hold only one unique value.

    I test this with nunique() instead of trusting documentation, so the result
    is measured rather than assumed.
    """
    constant_columns = []
    for column in data.columns:
        if data[column].nunique() == 1:
            constant_columns.append(column)
    return constant_columns


constant_columns = find_constant_columns(employees)
print("Constant columns found:", constant_columns)

# EmployeeNumber is unique per row, so it identifies a person but predicts nothing.
identifier_columns = ["EmployeeNumber"]

# .copy() gives me a separate table to work on, leaving the raw one untouched.
columns_to_drop = constant_columns + identifier_columns
hr = employees.drop(columns=columns_to_drop).copy()
print("Columns before:", employees.shape[1], "-> after:", hr.shape[1])

# Turn the Yes/No target into 1/0. The mean of a 0/1 column is the share of 1s,
# which is exactly the attrition rate, and models need numbers rather than words.
hr["AttritionFlag"] = (hr["Attrition"] == "Yes").astype(int)
print("Overall attrition rate: %.1f%%" % (hr["AttritionFlag"].mean() * 100))

# Bands for grouped analysis. The original numeric columns stay as they are;
# these are added alongside them.
age_bins = [17, 25, 35, 45, 55, 65]
age_labels = ["18-25", "26-35", "36-45", "46-55", "56+"]
hr["AgeBand"] = pd.cut(hr["Age"], bins=age_bins, labels=age_labels)

tenure_bins = [-1, 1, 3, 5, 10, 40]
tenure_labels = ["0-1 yrs", "2-3 yrs", "4-5 yrs", "6-10 yrs", "11+ yrs"]
hr["TenureBand"] = pd.cut(hr["YearsAtCompany"], bins=tenure_bins, labels=tenure_labels)

distance_bins = [-1, 2, 9, 19, 29]
distance_labels = ["0-2", "3-9", "10-19", "20+"]
hr["DistanceBand"] = pd.cut(hr["DistanceFromHome"], bins=distance_bins,
                            labels=distance_labels)

income_bands = [0, 3000, 6000, 10000, 20000]
income_labels = ["<3k", "3k-6k", "6k-10k", "10k+"]
hr["IncomeBand"] = pd.cut(hr["MonthlyIncome"], bins=income_bands,
                          labels=income_labels)

hr.to_csv(CLEAN_FILE, index=False)
print("Saved:", CLEAN_FILE, hr.shape)
