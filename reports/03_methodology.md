# Methodology

## 1. Project question

> The organisation's overall attrition rate is 16.1%, but that average hides
> large differences between roles and working conditions. Which segments show
> the highest observed attrition, how strongly is each factor associated with
> leaving, and can attrition be predicted well enough to support - never
> automate - retention decisions?

## 2. Analysis workflow

```
RAW DATA -> DATA INVENTORY -> DATA QUALITY -> CLEANING -> FEATURE ENGINEERING
-> EXPLORATORY DATA ANALYSIS -> BUSINESS QUESTIONS -> STATISTICS -> SQL
-> PYTHON -> MACHINE LEARNING -> DASHBOARD -> INSIGHTS -> RECOMMENDATIONS
-> DOCUMENTATION -> GITHUB -> INTERVIEW DEFENSE
```

## 3. Cleaning rules applied

| Rule | Reason |
|---|---|
| Drop columns with a single unique value | They carry zero analytical information |
| Drop `EmployeeNumber` | It is an identifier, not a feature |
| Keep every row | No duplicates, no missing values, no invalid ranges |
| Keep extreme salary values | They are real senior roles, not data-entry errors |
| Never overwrite `data/raw/` | Reproducibility: the original is always recoverable |

## 4. Statistical approach

**Chi-square test of independence** for categorical variables.
H0: the variable and attrition are independent. Reported with Cramer's V, because
with 1,470 rows a tiny difference can still produce a small p-value.

**Welch t-test** for numeric variables (leavers vs stayers). Welch is used instead
of Student's t-test because the two groups have unequal sizes and unequal variances.

**Cohen's d** as the effect size, interpreted as small (~0.2), medium (~0.5),
large (~0.8). Every effect in this dataset is small-to-moderate.

**Point-biserial correlation** (Pearson correlation with a 0/1 variable) as a
single-number summary of each numeric variable's linear association with attrition.

## 5. Machine-learning approach

| Decision | Choice | Why |
|---|---|---|
| Target | `AttritionFlag` (0/1) | Numeric, works with sklearn |
| Train/test split | 80 / 20, `stratify=target`, `random_state=42` | Keeps the 16% leaver share on both sides |
| Encoding | Ordinals kept numeric, nominals one-hot (`drop_first=True`) | Preserves real order, avoids the dummy trap |
| Scaling | `StandardScaler` for logistic regression only | Coefficients would otherwise be dominated by salary scale |
| Imbalance | `class_weight="balanced"` | Forces the model to care about the 16% minority class |
| Metrics | Recall, ROC-AUC, PR-AUC, F1 (not accuracy) | Accuracy is misleading when 84% of rows are the majority class |
| Validation | 5-fold stratified cross-validation | A single split can be lucky |
| Models | Logistic Regression + Random Forest | One interpretable, one non-linear comparison |

**I deliberately did not use SMOTE.** The class-weighted models already recovered
minority-class recall (70%), so adding synthetic observations was unnecessary and
would have made the pipeline harder to explain.

## 6. Reproducibility

* I fixed `random_state=42` in every split, model and cross-validation.
* Scripts run in a defined order and print what they did.
* `sql/05_reconciliation.sql` re-computes the headline KPIs independently; the
  SQL and Python results agree to the same 16.1%.
* Environment pinned in `requirements.txt`.
