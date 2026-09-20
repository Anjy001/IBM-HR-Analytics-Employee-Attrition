"""Exploratory analysis: who leaves, and how the groups compare.

I print the group size next to every rate. A 50% rate on two employees and a
24% rate on 259 employees are not the same kind of evidence, and the table
should make that visible.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CLEAN_FILE = "data/processed/hr_cleaned.csv"
IMAGE_FOLDER = "images"

education_map = {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}
satisfaction_map = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
worklife_map = {1: "Bad", 2: "Good", 3: "Better", 4: "Best"}
involvement_map = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
performance_map = {1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"}

hr = pd.read_csv(CLEAN_FILE)


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
        table.index = [str(i) + " - " + label_map.get(i, "") for i in table.index]
    return table


def bar_chart(series, title, xlabel, filename, color="#1f3864", horizontal=False):
    """Save a bar chart for one rate series."""
    fig, ax = plt.subplots(figsize=(7, 4))
    if horizontal:
        ax.barh(series.index[::-1], series.values[::-1], color=color)
        ax.set_xlabel(xlabel)
    else:
        ax.bar(series.index, series.values, color=color)
        ax.set_ylabel(xlabel)
        plt.xticks(rotation=45, ha="right")
    ax.set_title(title, fontsize=11, weight="bold")
    fig.tight_layout()
    fig.savefig(IMAGE_FOLDER + "/" + filename)
    plt.close(fig)


# Headline numbers, so the rest of the tables have a baseline to compare against.
total_employees = len(hr)
leavers = int(hr["AttritionFlag"].sum())
print("Total employees :", total_employees)
print("Leavers         :", leavers)
print("Attrition rate  : %.1f%%" % (leavers / total_employees * 100))
print("Retention rate  : %.1f%%" % ((total_employees - leavers) / total_employees * 100))
print("Avg age         : %.1f" % hr["Age"].mean())
print("Avg income      : %.0f" % hr["MonthlyIncome"].mean())
print("Overtime rate   : %.1f%%" % ((hr["OverTime"] == "Yes").mean() * 100))

segment_columns = ["Department", "JobRole", "OverTime", "MaritalStatus",
                   "BusinessTravel", "JobLevel", "Gender", "Education",
                   "EducationField", "JobSatisfaction", "EnvironmentSatisfaction",
                   "RelationshipSatisfaction", "WorkLifeBalance", "JobInvolvement",
                   "StockOptionLevel", "PerformanceRating", "AgeBand",
                   "TenureBand", "DistanceBand", "IncomeBand"]

label_lookup = {"Education": education_map, "JobSatisfaction": satisfaction_map,
                "EnvironmentSatisfaction": satisfaction_map,
                "RelationshipSatisfaction": satisfaction_map,
                "WorkLifeBalance": worklife_map, "JobInvolvement": involvement_map,
                "PerformanceRating": performance_map}

for column in segment_columns:
    table = attrition_table(hr, column, label_lookup.get(column))
    print("\n=== Attrition by", column, "===")
    print(table.to_string())

# The two cuts the dataset documentation suggests looking at.
distance_cut = hr.pivot_table(index="JobRole", columns="Attrition",
                              values="DistanceFromHome", aggfunc="mean").round(1)
distance_counts = hr.pivot_table(index="JobRole", columns="Attrition",
                                 values="DistanceFromHome", aggfunc="size")
print("\n=== Mean distance from home by job role x attrition ===")
print(distance_cut.to_string())
print("\n(group sizes)")
print(distance_counts.to_string())

income_cut = hr.pivot_table(index="Education", columns="Attrition",
                            values="MonthlyIncome", aggfunc="mean").round(0)
print("\n=== Mean monthly income by education x attrition ===")
print(income_cut.to_string())

interaction = hr.pivot_table(index="JobRole", columns="OverTime",
                             values="AttritionFlag", aggfunc=["mean", "size"])
print("\n=== Overtime x job role ===")
print(interaction.round(3).to_string())

bar_chart(attrition_table(hr, "JobRole")["AttritionRate"],
          "Attrition rate by job role", "Attrition rate (%)",
          "01_attrition_by_jobrole.png", horizontal=True)
bar_chart(attrition_table(hr, "OverTime")["AttritionRate"],
          "Attrition rate by overtime", "Attrition rate (%)",
          "02_attrition_overtime.png")
bar_chart(attrition_table(hr, "TenureBand")["AttritionRate"],
          "Attrition rate by years at company", "Attrition rate (%)",
          "03_attrition_tenure.png")
bar_chart(attrition_table(hr, "IncomeBand")["AttritionRate"],
          "Attrition rate by monthly income band", "Attrition rate (%)",
          "04_attrition_income.png")
bar_chart(attrition_table(hr, "MaritalStatus")["AttritionRate"],
          "Attrition rate by marital status", "Attrition rate (%)",
          "05_attrition_marital.png")
print("\nCharts saved to", IMAGE_FOLDER)
