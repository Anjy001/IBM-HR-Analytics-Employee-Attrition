"""Load the raw CSV and report what is actually inside it.

Nothing here changes the data. I only look first, so that every later decision
is based on what the file contains rather than on an assumption about it.
"""

import pandas as pd

RAW_FILE = "data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"

employees = pd.read_csv(RAW_FILE)

print("Rows   :", employees.shape[0])
print("Columns:", employees.shape[1])

# Column names and types for the fields I lean on most.
print("\n--- Columns and data types ---")
print(employees[["Age", "Attrition", "MonthlyIncome", "YearsAtCompany"]].dtypes)

print("\n--- First 5 rows ---")
print(employees.head())

# A quick quality radar before anything else.
print("\nTotal missing values:", employees.isnull().sum().sum())
print("Duplicate rows      :", employees.duplicated().sum())

# A column holding one value cannot explain any variation, so I look for them now.
constant_columns = [column for column in employees.columns
                    if employees[column].nunique() == 1]
print("\nConstant (useless) columns:", constant_columns)

print("\n--- Attrition distribution ---")
print(employees["Attrition"].value_counts())
