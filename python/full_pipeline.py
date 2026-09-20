"""Run the whole analysis in one pass and write every output.

This is the script behind the numbers in README.md. It chains the five staged
scripts together: load, clean, explore, test, model. Randomness is fixed with
random_state=42, so a fresh run reproduces the same figures.
"""

import json
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score, confusion_matrix,
                             roc_curve)

RAW = "data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUT = "reports/results"
os.makedirs(OUT, exist_ok=True)

employees = pd.read_csv(RAW)

# Value labels from the dataset documentation, used to make printouts readable.
education_map = {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}
satisfaction_map = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
involvement_map = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
performance_map = {1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"}
worklife_map = {1: "Bad", 2: "Good", 3: "Better", 4: "Best"}

results = {}

results["rows"] = int(employees.shape[0])
results["columns"] = int(employees.shape[1])
results["missing_total"] = int(employees.isnull().sum().sum())
results["duplicate_rows"] = int(employees.duplicated().sum())
results["unique_employee_ids"] = int(employees["EmployeeNumber"].nunique())

constant_columns = [c for c in employees.columns if employees[c].nunique() == 1]
results["constant_columns"] = constant_columns
results["constant_values"] = {c: str(employees[c].unique()[0]) for c in constant_columns}

identifier_columns = ["EmployeeNumber"]
results["id_columns"] = identifier_columns

# Drop what cannot inform the analysis: constant columns and the row identifier.
drop_columns = constant_columns + identifier_columns
hr = employees.drop(columns=drop_columns).copy()

hr["AttritionFlag"] = (hr["Attrition"] == "Yes").astype(int)

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


def attrition_table(data, group_column, label_map=None):
    """Employees, leavers and attrition rate for every group in a column."""
    table = data.groupby(group_column, observed=True).agg(
        Employees=("AttritionFlag", "size"),
        Leavers=("AttritionFlag", "sum"),
        AttritionRate=("AttritionFlag", "mean"),
    )
    table["AttritionRate"] = (table["AttritionRate"] * 100).round(1)
    table = table.sort_values("AttritionRate", ascending=False)
    if label_map is not None:
        table.index = [f"{i} - {label_map.get(i, '')}" if i in label_map else str(i)
                       for i in table.index]
    return table


def chi_square_test(data, group_column):
    """Chi-square test of independence, with Cramer's V as the effect size."""
    crosstab = pd.crosstab(data[group_column], data["AttritionFlag"])
    chi2, p_value, dof, expected = stats.chi2_contingency(crosstab)
    n = crosstab.values.sum()
    k = min(crosstab.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * k)) if k > 0 else np.nan
    return {"chi2": round(chi2, 2), "p_value": p_value, "dof": int(dof),
            "cramers_v": round(cramers_v, 3)}


def ttest_numeric(data, numeric_column):
    """Welch t-test on leavers vs stayers, with Cohen's d as the effect size."""
    leavers = data.loc[data["AttritionFlag"] == 1, numeric_column]
    stayers = data.loc[data["AttritionFlag"] == 0, numeric_column]
    t_stat, p_value = stats.ttest_ind(leavers, stayers, equal_var=False)
    pooled_sd = np.sqrt(((leavers.var(ddof=1) * (len(leavers) - 1)) +
                         (stayers.var(ddof=1) * (len(stayers) - 1))) /
                        (len(leavers) + len(stayers) - 2))
    cohens_d = (leavers.mean() - stayers.mean()) / pooled_sd
    return {"leaver_mean": round(leavers.mean(), 2), "stayer_mean": round(stayers.mean(), 2),
            "t": round(t_stat, 2), "p_value": p_value, "cohens_d": round(cohens_d, 3)}


total = len(hr)
leavers = int(hr["AttritionFlag"].sum())
results["total_employees"] = total
results["attrition_count"] = leavers
results["attrition_rate"] = round(leavers / total * 100, 1)
results["retention_rate"] = round((total - leavers) / total * 100, 1)
results["avg_age"] = round(hr["Age"].mean(), 1)
results["avg_monthly_income"] = round(hr["MonthlyIncome"].mean(), 0)
results["median_monthly_income"] = round(hr["MonthlyIncome"].median(), 0)
results["avg_years_at_company"] = round(hr["YearsAtCompany"].mean(), 1)
results["overtime_rate"] = round((hr["OverTime"] == "Yes").mean() * 100, 1)
results["avg_job_satisfaction"] = round(hr["JobSatisfaction"].mean(), 2)
results["avg_worklife"] = round(hr["WorkLifeBalance"].mean(), 2)
results["avg_job_involvement"] = round(hr["JobInvolvement"].mean(), 2)

segment_columns = {
    "Department": None, "JobRole": None, "OverTime": None, "MaritalStatus": None,
    "BusinessTravel": None, "JobLevel": None, "Gender": None,
    "Education": education_map, "EducationField": None,
    "JobSatisfaction": satisfaction_map, "EnvironmentSatisfaction": satisfaction_map,
    "RelationshipSatisfaction": satisfaction_map, "WorkLifeBalance": worklife_map,
    "JobInvolvement": involvement_map, "PerformanceRating": performance_map,
    "StockOptionLevel": None, "AgeBand": None, "TenureBand": None,
    "DistanceBand": None, "IncomeBand": None,
}

segment_tables = {}
for column, label_map in segment_columns.items():
    segment_tables[column] = attrition_table(hr, column, label_map)

results["attrition_by_jobrole"] = segment_tables["JobRole"].to_dict("index")
results["attrition_by_overtime"] = segment_tables["OverTime"].to_dict("index")
results["attrition_by_department"] = segment_tables["Department"].to_dict("index")
results["attrition_by_marital"] = segment_tables["MaritalStatus"].to_dict("index")
results["attrition_by_travel"] = segment_tables["BusinessTravel"].to_dict("index")
results["attrition_by_joblevel"] = segment_tables["JobLevel"].to_dict("index")
results["attrition_by_ageband"] = segment_tables["AgeBand"].to_dict("index")
results["attrition_by_tenureband"] = segment_tables["TenureBand"].to_dict("index")
results["attrition_by_education"] = segment_tables["Education"].to_dict("index")
results["attrition_by_distanceband"] = segment_tables["DistanceBand"].to_dict("index")
results["attrition_by_incomeband"] = segment_tables["IncomeBand"].to_dict("index")

distance_cut = hr.pivot_table(index="JobRole", columns="Attrition",
                              values="DistanceFromHome", aggfunc="mean").round(1)
distance_counts = hr.pivot_table(index="JobRole", columns="Attrition",
                                 values="DistanceFromHome", aggfunc="size")
results["distance_by_role_and_attrition"] = distance_cut.to_dict("index")
results["distance_counts"] = distance_counts.to_dict("index")

income_cut = hr.pivot_table(index="Education", columns="Attrition",
                            values="MonthlyIncome", aggfunc="mean").round(0)
income_cut.index = [f"{i} - {education_map[i]}" for i in income_cut.index]
results["income_by_education_and_attrition"] = income_cut.to_dict("index")

interaction = hr.pivot_table(index="JobRole", columns="OverTime",
                             values="AttritionFlag", aggfunc=["mean", "size"])
interaction_mean = (interaction["mean"] * 100).round(1)
interaction_mean.columns = [f"Attrition% {c}" for c in interaction_mean.columns]
interaction_size = interaction["size"]
interaction_size.columns = [f"N {c}" for c in interaction_size.columns]
overtime_role = pd.concat([interaction_mean, interaction_size], axis=1)
results["overtime_by_role"] = overtime_role.round(1).to_dict("index")

categorical_for_tests = ["Department", "JobRole", "OverTime", "MaritalStatus",
                         "BusinessTravel", "JobLevel", "Gender", "Education",
                         "EducationField", "JobSatisfaction", "EnvironmentSatisfaction",
                         "RelationshipSatisfaction", "WorkLifeBalance", "JobInvolvement",
                         "StockOptionLevel", "PerformanceRating"]

chi_results = {}
for column in categorical_for_tests:
    chi_results[column] = chi_square_test(hr, column)
results["chi_square"] = chi_results

numeric_for_tests = ["Age", "DailyRate", "DistanceFromHome", "HourlyRate",
                     "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked",
                     "PercentSalaryHike", "TotalWorkingYears", "TrainingTimesLastYear",
                     "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion",
                     "YearsWithCurrManager"]
ttest_results = {}
for column in numeric_for_tests:
    ttest_results[column] = ttest_numeric(hr, column)
results["ttest"] = ttest_results

numeric_matrix = hr[numeric_for_tests + ["AttritionFlag"]]
correlation = numeric_matrix.corr()["AttritionFlag"].drop("AttritionFlag")
correlation = correlation.sort_values()
results["correlation_with_attrition"] = correlation.round(3).to_dict()

model_data = hr.drop(columns=["Attrition", "EmployeeNumber"], errors="ignore").copy()

ordinal_columns = ["Education", "EnvironmentSatisfaction", "JobInvolvement",
                   "JobSatisfaction", "PerformanceRating", "RelationshipSatisfaction",
                   "WorkLifeBalance", "JobLevel", "StockOptionLevel"]
categorical_columns = ["BusinessTravel", "Department", "EducationField", "Gender",
                       "JobRole", "MaritalStatus", "OverTime", "AgeBand",
                       "TenureBand", "DistanceBand", "IncomeBand"]

features = model_data.drop(columns=["AttritionFlag"])
target = model_data["AttritionFlag"]

features = pd.get_dummies(features, columns=categorical_columns, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.20, random_state=42, stratify=target)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_model = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
log_model.fit(X_train_scaled, y_train)
log_prob = log_model.predict_proba(X_test_scaled)[:, 1]
log_pred = log_model.predict(X_test_scaled)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
log_cv_auc = cross_val_score(log_model, X_train_scaled, y_train, cv=cv, scoring="roc_auc")

rf_model = RandomForestClassifier(n_estimators=400, min_samples_leaf=3,
                                  class_weight="balanced", random_state=42)
rf_model.fit(X_train, y_train)
rf_prob = rf_model.predict_proba(X_test)[:, 1]
rf_pred = rf_model.predict(X_test)
rf_cv_auc = cross_val_score(rf_model, X_train, y_train, cv=cv, scoring="roc_auc")


def model_report(name, y_true, y_pred, y_prob, cv_scores):
    """Every metric I report for one model, on the held-out test set."""
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {
        "model": name,
        "accuracy": round(accuracy_score(y_true, y_pred), 3),
        "precision": round(precision_score(y_true, y_pred), 3),
        "recall": round(recall_score(y_true, y_pred), 3),
        "f1": round(f1_score(y_true, y_pred), 3),
        "roc_auc": round(roc_auc_score(y_true, y_prob), 3),
        "pr_auc": round(average_precision_score(y_true, y_prob), 3),
        "cv_roc_auc_mean": round(cv_scores.mean(), 3),
        "cv_roc_auc_std": round(cv_scores.std(), 3),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


results["models"] = [
    model_report("Logistic Regression (class_weight=balanced)", y_test, log_pred, log_prob, log_cv_auc),
    model_report("Random Forest (class_weight=balanced)", y_test, rf_pred, rf_prob, rf_cv_auc),
]

results["baseline_accuracy"] = round(1 - y_test.mean(), 3)

coef_table = pd.DataFrame({
    "Feature": features.columns,
    "Coefficient": log_model.coef_[0],
    "OddsRatio": np.exp(log_model.coef_[0]),
}).sort_values("Coefficient", ascending=False)
results["log_top_positive"] = coef_table.head(10).round(3).to_dict("records")
results["log_top_negative"] = coef_table.tail(10).iloc[::-1].round(3).to_dict("records")

importance_table = pd.DataFrame({
    "Feature": features.columns,
    "Importance": rf_model.feature_importances_,
}).sort_values("Importance", ascending=False)
results["rf_top_importance"] = importance_table.head(15).round(4).to_dict("records")

plt.rcParams.update({"figure.dpi": 130, "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False})
NAVY, ORANGE, GREY = "#1f3864", "#e07b39", "#9aa5b1"


def bar_chart(table, title, xlabel, filename, color=NAVY, horizontal=False):
    """Save one bar chart for a rate series."""
    fig, ax = plt.subplots(figsize=(7, 4))
    if horizontal:
        ax.barh(table.index[::-1], table.values[::-1], color=color)
        ax.set_xlabel(xlabel)
    else:
        ax.bar(table.index, table.values, color=color)
        ax.set_ylabel(xlabel)
        plt.xticks(rotation=45, ha="right")
    ax.set_title(title, fontsize=11, weight="bold")
    for i, value in enumerate(table.values):
        if horizontal:
            ax.text(value, i, f" {value:.1f}%", va="center", fontsize=8)
        else:
            ax.text(i, value, f"{value:.1f}%", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig("images/" + filename)
    plt.close(fig)


bar_chart(segment_tables["JobRole"]["AttritionRate"],
          "Attrition rate by job role", "Attrition rate (%)",
          "01_attrition_by_jobrole.png", horizontal=True)
bar_chart(segment_tables["OverTime"]["AttritionRate"],
          "Attrition rate by overtime", "Attrition rate (%)", "02_attrition_overtime.png")
bar_chart(segment_tables["TenureBand"]["AttritionRate"],
          "Attrition rate by years at company", "Attrition rate (%)",
          "03_attrition_tenure.png")
bar_chart(segment_tables["IncomeBand"]["AttritionRate"],
          "Attrition rate by monthly income band", "Attrition rate (%)",
          "04_attrition_income.png")
bar_chart(segment_tables["MaritalStatus"]["AttritionRate"],
          "Attrition rate by marital status", "Attrition rate (%)",
          "05_attrition_marital.png")

fig, ax = plt.subplots(figsize=(7, 5))
colors = [ORANGE if v > 0 else NAVY for v in correlation.values]
ax.barh(correlation.index, correlation.values, color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Correlation with attrition (point-biserial)")
ax.set_title("Numeric variables: correlation with attrition", fontsize=11, weight="bold")
fig.tight_layout()
fig.savefig("images/06_correlation.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(5.5, 5))
for name, prob, color in [("Logistic Regression", log_prob, NAVY),
                          ("Random Forest", rf_prob, ORANGE)]:
    fpr, tpr, _ = roc_curve(y_test, prob)
    auc_value = roc_auc_score(y_test, prob)
    ax.plot(fpr, tpr, color=color, label=f"{name} (AUC = {auc_value:.3f})")
ax.plot([0, 1], [0, 1], linestyle="--", color=GREY, label="Random guess (AUC = 0.5)")
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.set_title("ROC curves - attrition model", fontsize=11, weight="bold")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("images/07_roc_curves.png")
plt.close(fig)

top_importance = importance_table.head(12).set_index("Feature")["Importance"]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(top_importance.index[::-1], top_importance.values[::-1], color=NAVY)
ax.set_xlabel("Importance")
ax.set_title("Random forest feature importance (top 12)", fontsize=11, weight="bold")
fig.tight_layout()
fig.savefig("images/08_feature_importance.png")
plt.close(fig)

with open(OUT + "/all_results.json", "w") as file:
    json.dump(results, file, indent=2, default=str)

coef_table.to_csv(OUT + "/logistic_coefficients.csv", index=False)
importance_table.to_csv(OUT + "/random_forest_importance.csv", index=False)
hr.to_csv("data/processed/hr_cleaned.csv", index=False)

print("=== HEADLINE ===")
for key in ["rows", "columns", "missing_total", "duplicate_rows", "constant_columns",
            "total_employees", "attrition_count", "attrition_rate", "retention_rate",
            "avg_age", "avg_monthly_income", "median_monthly_income",
            "avg_years_at_company", "overtime_rate"]:
    print(key, "=", results[key])

for name, table in segment_tables.items():
    print(f"\n=== ATTRITION BY {name} ===")
    print(table.to_string())

print("\n=== MODELS ===")
for row in results["models"]:
    print(row)
print("baseline_accuracy =", results["baseline_accuracy"])
print("features used:", len(features.columns))
