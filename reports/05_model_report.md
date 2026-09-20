# Model Report

## Setup

* Target: `AttritionFlag` (1 = left, 0 = stayed)
* Features: 58 encoded columns (ordinals numeric, nominals one-hot with `drop_first=True`)
* Split: 80 / 20 stratified on the target, `random_state=42`
* Scaling: `StandardScaler` for logistic regression only
* Imbalance handling: `class_weight="balanced"` in both models
* Validation: 5-fold stratified cross-validation

## Results (held-out test set, 294 rows)

| Metric | Logistic Regression | Random Forest | Majority baseline |
|---|---|---|---|
| Accuracy | 0.765 | 0.823 | **0.840** |
| Precision | 0.375 | 0.442 | 0.000 |
| Recall | **0.702** | 0.404 | 0.000 |
| F1 | **0.489** | 0.422 | 0.000 |
| ROC-AUC | **0.829** | 0.785 | 0.500 |
| PR-AUC | **0.525** | 0.419 | 0.160 |
| 5-fold CV ROC-AUC | **0.830 +/- 0.022** | 0.807 +/- 0.028 | - |
| Confusion matrix | TN=192 FP=55 FN=14 TP=33 | TN=223 FP=24 FN=28 TP=19 | - |

![ROC curves](../images/07_roc_curves.png)

## The point that matters most

A model that **always predicts "no attrition"** scores **84% accuracy** - higher
than either real model. This is why accuracy is the wrong headline metric on an
imbalanced target. The logistic regression is the better business model because
it identifies **70% of leavers** (recall 0.702) versus the forest's 40%, at the
cost of more false alarms.

Because HR will act on the output, recall matters more than precision: a false
alarm costs one supportive conversation, while a missed leaver costs a
replacement hire.

## Threshold

My predictions use the default 0.5 cut-off. Lowering it increases recall (catch more
at-risk employees) and increases false positives. The correct threshold is a
**business decision based on the relative cost of a missed leaver versus a false
alarm** - it should not be chosen by maximising accuracy.

## Interpretation: logistic regression odds ratios

| Feature | Odds ratio | Direction |
|---|---|---|
| BusinessTravel = Travel_Frequently | 2.181 | increases attrition odds |
| OverTime = Yes | 2.168 | increases |
| JobRole = Laboratory Technician | 2.043 | increases |
| YearsAtCompany | 1.836 | (see caveat below) |
| NumCompaniesWorked | 1.743 | increases |
| BusinessTravel = Travel_Rarely | 1.710 | increases |
| JobRole = Sales Representative | 1.679 | increases |
| JobRole = Sales Executive | 1.618 | increases |
| JobLevel | 1.586 | increases |
| YearsSinceLastPromotion | 1.548 | increases |
| TotalWorkingYears | 0.474 | decreases |
| TenureBand = 11+ yrs | 0.486 | decreases |
| JobRole = Research Director | 0.590 | decreases |
| EnvironmentSatisfaction | 0.627 | decreases |
| JobSatisfaction | 0.655 | decreases |

**Caveat I want to be upfront about:** `YearsAtCompany` shows a positive coefficient (+0.607) which
looks paradoxical, since longer tenure is associated with *lower* attrition in the
raw cross-tabulation (11+ yrs = 8.1% vs 0-1 yrs = 34.9%). This is
**multicollinearity / suppression**: tenure information is already carried by the
`TenureBand` dummies and `TotalWorkingYears`, so the leftover coefficient for
`YearsAtCompany` is not interpretable in isolation. It is flagged here rather than
presented as a finding.

Full coefficient table: [`results/logistic_coefficients.csv`](results/logistic_coefficients.csv)

## Interpretation: random forest importance

| Feature | Importance |
|---|---|
| MonthlyIncome | 0.0722 |
| Age | 0.0565 |
| OverTime_Yes | 0.0542 |
| TotalWorkingYears | 0.0537 |
| DailyRate | 0.0467 |
| YearsAtCompany | 0.0440 |
| YearsWithCurrManager | 0.0409 |
| HourlyRate | 0.0380 |
| DistanceFromHome | 0.0379 |
| MonthlyRate | 0.0378 |
| StockOptionLevel | 0.0363 |
| NumCompaniesWorked | 0.0346 |
| JobLevel | 0.0295 |
| YearsInCurrentRole | 0.0278 |
| PercentSalaryHike | 0.0273 |

![Feature importance](../images/08_feature_importance.png)

**Feature importance is not causation.** It says the model uses this variable to
separate leavers from stayers - not that changing it would change attrition.

Full table: [`results/random_forest_importance.csv`](results/random_forest_importance.csv)

## Validation summary

| Validation step | Result |
|---|---|
| Stratified split preserves class ratio | train 16.1% / test 16.1% |
| 5-fold CV vs single split | CV ROC-AUC 0.830 +/- 0.022 - stable, not a lucky split |
| Baseline comparison | logistic 0.829 vs do-nothing 0.500 AUC |
| PR-AUC vs base rate | 0.525 vs 0.160 base rate - real lift |
| Leakage check | no post-exit variables used |

## Limitations of the model

1. Trained on a **synthetic** dataset - performance will not transfer to real staff.
2. n = 1,470 with 58 features: overfitting risk is genuine; CV was used to check it.
3. No dates, so no time-based validation (no predict-next-quarter test).
4. The models describe **association**, never causality.
5. Not a decision system: see `07_limitations_and_responsible_ai.md`.
