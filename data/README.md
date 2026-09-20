# Data

## Folder structure

```
data/
├── raw/         <- original file. NEVER edited by any script.
└── processed/   <- cleaned + feature-engineered file produced by python/02_data_cleaning.py
```

| File | Rows | Columns | Description |
|---|---|---|---|
| `raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` | 1,470 | 35 | Original IBM HR Analytics dataset, unmodified |
| `processed/hr_cleaned.csv` | 1,470 | 35 | 4 uninformative columns dropped, target flag + 4 band features added by me |

Source of the raw data: IBM HR Analytics Employee Attrition & Performance
(Kaggle) - a **fictional dataset created by IBM data scientists**.

To regenerate `processed/hr_cleaned.csv`:

```bash
python python/02_data_cleaning.py
```

The original file is never overwritten. Every transformation is reproducible
with `random_state=42` where randomness is used.
