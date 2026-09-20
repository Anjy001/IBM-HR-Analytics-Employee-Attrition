# Notebooks

These notebooks mirror the scripts in `../python/` one-to-one, so the analysis can be
followed cell by cell with the outputs visible.

| Notebook | Mirrors |
|---|---|
| `01_data_understanding.ipynb` | `python/01_data_loading.py` |
| `02_data_cleaning.ipynb` | `python/02_data_cleaning.py` |
| `03_eda.ipynb` | `python/03_eda.py` |
| `04_statistical_analysis.ipynb` | `python/04_statistical_analysis.py` |
| `05_attrition_model.ipynb` | `python/05_attrition_model.py` |

I kept the notebooks deliberately short: the logic lives in the `.py` scripts,
the notebooks walk through it. Run them from the repository root so the relative
`data/` and `images/` paths resolve.
