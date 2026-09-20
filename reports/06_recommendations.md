# Recommendations

Each recommendation is tied to the evidence that produced it. They are framed as
**investigations to run**, not as guaranteed fixes, because the dataset cannot
prove that changing anything would change attrition.

## 1. Overtime is the strongest and most actionable signal

**Evidence:** 30.5% attrition with overtime (416 employees, 127 leavers) versus
10.4% without (1,054 employees, 110 leavers). Cramer's V 0.244, the strongest of
any variable tested (chi-square 87.56, p = 8.2e-21). Overtime raises attrition in
8 of 9 job roles; Sales Representatives go from 28.8% to 66.7%.

**Recommended action:** audit overtime distribution by role, starting with Sales
Representatives and Laboratory Technicians. Pilot a workload review in those two
roles and measure the effect before scaling it. This is the highest-leverage
single area, but it needs a controlled test.

**Caution:** with a synthetic dataset I cannot rule out that overtime and
attrition are both driven by a third factor such as understaffing.

## 2. Early tenure needs an onboarding intervention

**Evidence:** 34.9% attrition in year 0-1 (215 employees, 75 leavers) falling
monotonically to 8.1% after 11 years. Age band 18-25 shows 35.8%.

**Recommended action:** review the first-year experience - onboarding quality,
mentoring, first-90-day check-ins - and instrument it so the effect can be
measured. The first year is where the volume of loss is concentrated.

## 3. Stock options look like a retention lever worth testing

**Evidence:** employees with level 0 stock options show 24.4% attrition
(631 employees, 154 leavers) versus 7.6% at level 2 (158 employees, 12 leavers).
Cramer's V 0.203, chi-square 60.60 - one of the strongest relationships in the
dataset and rarely highlighted in published versions of this analysis.

**Recommended action:** investigate eligibility design. Do not assume causal
direction - equity may be given *to* people the company already expects to stay.

## 4. Address the entry-level pay gap

**Evidence:** under-3k band shows 28.6% attrition; leavers earned less than
stayers at every education level (e.g. Bachelor: 4,770 vs 6,883). MonthlyIncome
t-test Cohen's d -0.440.

**Recommended action:** benchmark entry-level compensation against the market.
This is a candidate driver, but pay is entangled with job level and age.

## 5. Watch the "long commute" segment

**Evidence:** 21.4% attrition at 20+ distance units versus 12.9% at 0-2.
DistanceFromHome is one of the few variables where leavers score *higher*
(t = 2.89, d = +0.212). Mean commute distance for leavers exceeds stayers in
6 of 9 roles.

**Recommended action:** evaluate flexible/hybrid arrangements for high-commute
employees in Sales and Healthcare Representative roles.

## 6. Do not act on these (no evidence)

| Variable | Evidence | Action |
|---|---|---|
| PerformanceRating | chi-square 0.00, p = 0.990; both levels ~16% | Ignore for retention |
| Gender | p = 0.291, V = 0.028 | Never use as a driver; audit for bias only |
| Education | p = 0.546 | Not a meaningful driver here |
| RelationshipSatisfaction | p = 0.155 | Not statistically significant |
| HourlyRate / MonthlyRate / PercentSalaryHike | p > 0.5 in every test | Not useful |

Reporting these is as important as reporting the significant results: it stops HR
spending budget on factors the data does not support.

## 7. Build the measurement loop before acting on any of this

The dataset cannot tell us whether any intervention works. The real
recommendation for the organisation is to instrument attrition properly:
hire/exit dates, exit reasons, exit costs, and pre/post measurement of every
programme. Then this same analysis becomes a genuine decision tool.

## Priority ranking

| Priority | Driver | Evidence strength | Actionability |
|---|---|---|---|
| 1 | OverTime | Very strong (V 0.244) | High - workload is controllable |
| 2 | JobRole | Very strong (V 0.242) | Medium - role redesign is complex |
| 3 | Tenure / early career | Strong (34.9% -> 8.1%) | High - onboarding is controllable |
| 4 | StockOptionLevel | Strong (V 0.203) | Medium - policy change needed |
| 5 | MonthlyIncome | Strong (d -0.440) | Medium - budget dependent |
| 6 | JobLevel | Strong (V 0.222) | Low - structural |
| 7 | MaritalStatus | Moderate (V 0.177) | None - proxy variable, do not act directly |
| 8 | DistanceFromHome | Moderate (d +0.212) | Medium - hybrid policy |
| 9 | BusinessTravel | Moderate (V 0.128) | Medium - travel policy |
