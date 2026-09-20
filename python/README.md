# Python

Beginner-readable, professionally efficient scripts. Each file runs on its own
and prints what it did.

| Script | What it does |
|---|---|
| `01_data_loading.py` | Loads the raw CSV and prints shape, columns, dtypes |
| `02_data_cleaning.py` | Drops constant + ID columns, builds target flag and bands, writes `data/processed/hr_cleaned.csv` |
| `03_eda.py` | Segment tables + the two dataset-page cuts + saves charts |
| `04_statistical_analysis.py` | Chi-square, Welch t-tests, Cohen's d, correlations |
| `05_attrition_model.py` | Logistic Regression vs Random Forest, metrics, ROC, importance |
| `full_pipeline.py` | End-to-end script: cleaning -> EDA -> statistics -> ML -> charts. This is the script behind every figure in the README |

Run order:

```bash
python python/01_data_loading.py
python python/02_data_cleaning.py
python python/03_eda.py
python python/04_statistical_analysis.py
python python/05_attrition_model.py
```

Or run everything at once:

```bash
python python/full_pipeline.py
```

## Code philosophy

I deliberately avoided "clever" one-liners in these scripts. They use:

* clear descriptive variable names (`attrition_rate`, not `ar`)
* one logical step per statement
* small helper functions instead of deeply nested expressions
* vectorised pandas instead of `for` loops over rows
* counts (`N`) reported next to every percentage

