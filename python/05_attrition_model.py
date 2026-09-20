"""Predict attrition, and be honest about what the numbers mean.

I fit two models: logistic regression, because its coefficients convert to odds
ratios I can explain to HR, and a random forest as a non-linear comparison.

Only about 16% of employees left, so accuracy is a trap here - predicting
"nobody leaves" for every row already scores roughly 84%. I judge the models on
recall, ROC-AUC and PR-AUC instead, and weight the classes to compensate.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, average_precision_score, confusion_matrix,
                             roc_curve)

CLEAN_FILE = "data/processed/hr_cleaned.csv"
hr = pd.read_csv(CLEAN_FILE)

model_data = hr.drop(columns=["Attrition", "AttritionFlag"]).copy()
target = hr["AttritionFlag"]

# The 1-4 and 1-5 scales have a real order, so I leave them as numbers.
ordinal_columns = ["Education", "EnvironmentSatisfaction", "JobInvolvement",
                   "JobSatisfaction", "PerformanceRating", "RelationshipSatisfaction",
                   "WorkLifeBalance", "JobLevel", "StockOptionLevel"]

# Job titles and categories have no order, so they become dummy variables.
categorical_columns = ["BusinessTravel", "Department", "EducationField", "Gender",
                       "JobRole", "MaritalStatus", "OverTime", "AgeBand",
                       "TenureBand", "DistanceBand", "IncomeBand"]

features = pd.get_dummies(model_data, columns=categorical_columns, drop_first=True)
print("Encoded feature count:", features.shape[1])

# Stratified so the 16% leaver share is preserved on both sides of the split.
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.20, random_state=42, stratify=target)
print("Train rows:", len(X_train), "Test rows:", len(X_test))

# Logistic regression coefficients are only comparable once the inputs share a
# scale, otherwise salary dominates age purely through its units.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_model = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
log_model.fit(X_train_scaled, y_train)
log_pred = log_model.predict(X_test_scaled)
log_prob = log_model.predict_proba(X_test_scaled)[:, 1]

rf_model = RandomForestClassifier(n_estimators=400, min_samples_leaf=3,
                                  class_weight="balanced", random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_prob = rf_model.predict_proba(X_test)[:, 1]


def model_report(name, y_true, y_pred, y_prob, cv_scores):
    """Every metric I care about for one model, on the held-out test set."""
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
        "confusion": "TN=%d FP=%d FN=%d TP=%d" % (tn, fp, fn, tp),
    }


cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

log_cv = cross_val_score(log_model, X_train_scaled, y_train, cv=cv, scoring="roc_auc")
rf_cv = cross_val_score(rf_model, X_train, y_train, cv=cv, scoring="roc_auc")

print("\n=== MODEL COMPARISON (held-out test set) ===")
print(model_report("Logistic Regression", y_test, log_pred, log_prob, log_cv))
print(model_report("Random Forest", y_test, rf_pred, rf_prob, rf_cv))

# The benchmark that makes accuracy meaningless: always answer "no attrition".
baseline = 1 - y_test.mean()
print("\nMajority-class baseline accuracy: %.3f" % baseline)
print("(Any model below this is worse than guessing 'nobody leaves'.)")

coef_table = pd.DataFrame({
    "Feature": features.columns,
    "Coefficient": log_model.coef_[0],
    "OddsRatio": np.exp(log_model.coef_[0]),
}).sort_values("Coefficient", ascending=False)

print("\n=== DRIVERS TOWARDS LEAVING (odds ratio above 1) ===")
print(coef_table.head(10).round(3).to_string(index=False))
print("\n=== PROTECTIVE FACTORS (odds ratio below 1) ===")
print(coef_table.tail(10).round(3).to_string(index=False))

importance_table = pd.DataFrame({
    "Feature": features.columns,
    "Importance": rf_model.feature_importances_,
}).sort_values("Importance", ascending=False)
print("\n=== RANDOM FOREST IMPORTANCE (top 15) ===")
print(importance_table.head(15).round(4).to_string(index=False))

coef_table.to_csv("reports/results/logistic_coefficients.csv", index=False)
importance_table.to_csv("reports/results/random_forest_importance.csv", index=False)

plt.rcParams.update({"figure.dpi": 130, "font.size": 9})
fig, ax = plt.subplots(figsize=(5.5, 5))
for name, prob, color in [("Logistic Regression", log_prob, "#1f3864"),
                          ("Random Forest", rf_prob, "#e07b39")]:
    fpr, tpr, _ = roc_curve(y_test, prob)
    ax.plot(fpr, tpr, color=color,
            label=name + " (AUC = %.3f)" % roc_auc_score(y_test, prob))
ax.plot([0, 1], [0, 1], linestyle="--", color="#9aa5b1", label="Random guess (0.5)")
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.set_title("ROC curves - attrition model", fontsize=11, weight="bold")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("images/07_roc_curves.png")
plt.close(fig)

top_importance = importance_table.head(12).set_index("Feature")["Importance"]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(top_importance.index[::-1], top_importance.values[::-1], color="#1f3864")
ax.set_xlabel("Importance")
ax.set_title("Random forest feature importance (top 12)", fontsize=11, weight="bold")
fig.tight_layout()
fig.savefig("images/08_feature_importance.png")
plt.close(fig)
print("\nCharts saved: images/07_roc_curves.png, images/08_feature_importance.png")
