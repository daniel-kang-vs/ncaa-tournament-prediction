# NCAA Selection & Seed Modeling

> Who should make the tournament, and how should selected teams be ordered?

**Modeling study · evaluation needs revalidation**

A two-stage modeling workflow separates tournament selection from overall seed prediction, with engineered team-performance features.

[Case study](https://daniel-kang-vs.github.io/projects/ncaa.html) · [Source evidence](https://github.com/daniel-kang-vs/ncaa-tournament-prediction/blob/main/FinalFourAnalyticsChallenge2026.ipynb) · [Live dashboard](https://daniel-kang-vs.github.io/ncaa-tournament-prediction/)

[![Dashboard preview](https://raw.githubusercontent.com/daniel-kang-vs/daniel-kang-vs.github.io/main/pngs/project-ncaa.png)](https://daniel-kang-vs.github.io/ncaa-tournament-prediction/)

## Highlights

- **1,353 training rows**
- **249 seeded team-seasons**
- **Two-stage workflow**

## The problem

Selection is a binary decision; assigning an overall seed is a ranking and regression problem. Combining them into one target obscures the tradeoffs around bubble teams.

## Data & scope

The committed training file has 1,353 rows and 20 source columns. A populated Overall Seed identifies 249 selected team-seasons. Overall seed is a national ordering, not a 1–16 bracket seed line.

## How it works

1. Derive features from records, NET rankings, schedule strength and quadrant results.
2. Generate base-model predictions and use a logistic meta-model for selection.
3. Model overall seed separately for selected teams.
4. Inspect class balance and season coverage before interpreting model scores.

## Key technical decision

Separate classification from regression and expose the evaluation design. Some notebook labels say XGBoost, LightGBM and CatBoost while the corresponding estimators are scikit-learn GradientBoosting, HistGradientBoosting and ExtraTrees.

## Results & interpretation

The committed artifact demonstrates the modeling workflow and feature engineering. The earlier narrative reports 0.966 AUC and a 0.653 threshold, but the notebook contains no saved evaluation outputs to verify those figures. The dashboard therefore shows source-derived dataset analysis rather than invented model curves.

## Limitations & next steps

Imputation precedes cross-validation, and the meta-model is fitted and scored on the same out-of-fold feature matrix. The score is not an independent nested evaluation. Refit preprocessing within folds, evaluate the full stack on held-out seasons, and save predictions before claiming generalization.

## Evidence & reproducibility

NCAA_Seed_Training_Set2.0.csv supports the dashboard’s dataset counts. Historical model scores remain unverified, not newly reproduced.

## Repository guide

- [`FinalFourAnalyticsChallenge2026.ipynb`](FinalFourAnalyticsChallenge2026.ipynb) — analysis implementation.
- [`docs/`](docs/) — static dashboard, styles, and browser-side analysis.

## Run or inspect

Clone this repository and run from its root:

```bash
pip install jupyter pandas numpy matplotlib scikit-learn
jupyter notebook FinalFourAnalyticsChallenge2026.ipynb
```

Notebook commands require the referenced CSV files and compatible dependencies; recorded results have not been retrained for this documentation refresh.

## Technology

Python · scikit-learn · pandas · Ensembles

NCAA input-quality note: some win–loss fields contain date-like strings (for example `8-Sep`). Recover the original record notation and validate parsing before retraining; the dashboard counts rows and selection labels without interpreting those fields.

## Refresh the descriptive dashboard

Run `python scripts/refresh_dashboard_data.py` from the repository root, then serve `docs/` with `python3 -m http.server 8000 --directory docs`. Source hashes and interpretation notes are in [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).
