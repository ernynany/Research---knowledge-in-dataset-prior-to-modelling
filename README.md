# Detecting Learnable Signal in Tabular Datasets Before Model Training

Code, data and paper for the 10 ECTS master's research project.

## Contents

| Folder | What it holds |
|---|---|
| `notebooks/` | Eight documented Jupyter notebooks, executed, with all outputs saved |
| `data/raw`, `data/processed` | Downloaded files and the cleaned datasets used by every notebook |
| `results/` | Cached results of every experiment (CSV/PKL); notebooks reuse them instead of recomputing |
| `figures/` | All figures (PNG, 200 dpi) |
| `paper/` | IEEE-format paper: `paper.pdf`, LaTeX sources (`paper.tex`, `sections/`, `generated/` tables), `IEEEtran.cls` |
| `ext/problexity/` | Source of the problexity library (only two modules are imported) |

## Notebook order

1. `00_data_acquisition` — downloads Adult, NSW, the Malawi incentive experiment, Pima, Banknote, Breast Cancer; documents and cleans them.
2. `01_probe_library` — every function: preprocessing, sanity check, synthetic generators, the 11 probes, the permutation/Simes inference layer, Ojala–Garriga Tests 1 and 2, self-tests.
3. `02_ojala_garriga_replication` — Tests 1 and 2, four classifiers, all datasets.
4. `03_experiment_A_calibration` — false-positive rates; multiple-testing inflation.
5. `04_experiments_B_C_power_robustness` — power, minimum detectable effect, robustness.
6. `05_semisynthetic_and_case_studies` — label shuffling on real data; Adult, NSW and incentive-experiment case studies; within-village permutation test.
7. `06_experiment_D_leakage_and_runtime` — leakage cases and runtime.
8. `07_analysis_protocol_and_paper_tables` — hypothesis verdicts, two-stage protocol, LaTeX tables, `paper/generated/key_numbers.json`.

## Running

Python ≥ 3.10 with numpy, pandas, scipy, scikit-learn (≥ 1.4), matplotlib and joblib. Open the notebooks from the `notebooks/` folder in Jupyter and run them in order. Results are cached in `results/`; delete a cache file to recompute that experiment. The full computation took about 6 hours on two CPU cores.

## Deviations from the proposal

TabPFN and LightGBM could not be installed in the build environment (network restricted to GitHub). A random forest replaces TabPFN, and scikit-learn's histogram gradient boosting replaces LightGBM. Power experiments stop at n = 5,000. See paper Section V-C.
