# NCAA Tournament Selection — Final Four Analytics Challenge 2026

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) ![scikit-learn](https://img.shields.io/badge/scikit--learn-stacked%20ensemble-f7931e?logo=scikit-learn) ![pandas](https://img.shields.io/badge/pandas-feature%20engineering-150458?logo=pandas)

> **Two decisions, two models.** Classify who makes the tournament, then predict a seed only for the teams that clear the cut. Selection AUC **0.966**. A precision-recall threshold of **0.653** names **70** teams against a **68-team** field.

**[Live demo](https://daniel-kang-vs.github.io/ncaa-tournament-prediction/)**

---

## Project Highlights

- Selection and seeding are not the same task. A single model that emits both mixes a yes/no decision with a ranking
- **15 raw columns → 50 features** across 2,701 team-seasons: records parsed into wins, losses, and win rate, plus conference strength, NET momentum, quality wins, and strength of schedule
- **8 base learners** (HistGradientBoosting, GradientBoosting, ExtraTrees, RandomForest, each as a classifier and a regressor). Logistic regression stacks selection. Ridge stacks the seed
- Scores come from **10-fold stratified cross-validation** and out-of-fold predictions, so the threshold is not tuned on the same rows the model just fit

---

## Problem Statement

The tournament has a fixed number of bids. A cutoff of 0.5 ignores that. It also treats a 1-seed and a bubble team as the same kind of error.

| Stage | Question | Metric |
|-------|----------|--------|
| Selection | Does this team get a bid? | ROC-AUC, then an F1-maximizing threshold |
| Seed | If yes, where are they seeded? | Mean absolute error on seed |

Training file: `NCAA_Seed_Training_Set2.0.csv`. Test file: `NCAA_Seed_Test_Set2.0.csv` (451 team-rows to score). Feature definitions are in `FFAC Data Dictionary.xlsx`.

---

## Feature Engineering

W–L fields arrive as strings, and some were corrupted when Excel read `8-9` as a date. Those strings are parsed back into wins, losses, and a win percentage before any model sees them.

| Family | What it captures |
|--------|------------------|
| Record rates | Wins, losses, win% from the W–L columns |
| Conference context | Conference tier, Power conference flag |
| NET | Rank, year-over-year momentum, improvement |
| Quality | Quality wins, bad losses |
| Schedule | Composite strength of schedule |

NET rank is the strongest single signal. Quality-of-win and overall win rate still move the score after NET is in the model, which is why the feature set is not “just use NET.”

---

## Model

```
2,701 team-seasons
        │
        ▼
50 engineered features
        │
        ├── 4 classifiers  →  out-of-fold probabilities  →  logistic regression  →  P(selected)
        │                                                                      │
        │                                                           threshold 0.653
        │
        └── 4 regressors   →  out-of-fold seed predictions →  ridge  →  seed, only if selected
```

Base models: HistGradientBoosting, GradientBoosting, ExtraTrees, RandomForest.

The threshold is read off the precision-recall curve of the out-of-fold selection scores. The default 0.5 cutoff selects too many teams. 0.653 is the cutoff that keeps the predicted field near 68.

---

## Results

| Metric | Value |
|--------|-------|
| Selection AUC | 0.966 |
| Decision threshold | 0.653 (precision-recall, not 0.5) |
| Teams selected on the test file | 70 |
| Field size | 68 |
| Raw columns → features | 15 → 50 |
| Team-seasons in the history | 2,701 |
| Validation | 10-fold stratified CV, out-of-fold predictions |

The seed stage is fit to mean absolute error, not to classification accuracy. A learning-rate sweep in the notebook puts single-model seed MAE near 3.85–3.89 lines (XGBoost 3.851, LightGBM 3.885, CatBoost 3.887). That is seed error, not “usually inside two lines.” The within-±2 rate is computed in the notebook; it is a share of teams, not a guarantee on every team.

---

## Key Technical Decisions

1. **Two stages.** Bubble teams are where a combined model is most expensive. Selection is a classification decision. Seed is a rank among teams that already made it.

2. **Stack on out-of-fold predictions.** If the meta-learner trains on in-sample base predictions, it learns each base model’s optimism. Out-of-fold predictions are the ones it will actually see.

3. **Tune the cutoff to the field size.** AUC can be excellent and the submitted list can still be the wrong length. The 68-team constraint is a threshold problem.

4. **What the validation does not prove.** Folds are stratified, not a pure walk-forward by season. A later season can still sit in the training side of an earlier fold. A stricter test would train only on past tournaments.

---

## Repository Structure

```
├── FinalFourAnalyticsChallenge2026.ipynb
├── NCAA_Seed_Training_Set2.0.csv
├── NCAA_Seed_Test_Set2.0.csv
├── FFAC Data Dictionary.xlsx
├── submission_template2.0.csv
├── docs/                 # Live demo
└── README.md
```

---

## How to Run

```bash
pip install scikit-learn pandas numpy matplotlib openpyxl
jupyter notebook FinalFourAnalyticsChallenge2026.ipynb
```

Run the notebook top to bottom. The selection AUC, the 0.653 threshold, and the 70-team list are the numbers the demo reports from that pipeline.

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| scikit-learn | Base learners, logistic regression, ridge, stratified CV |
| pandas / NumPy | W–L parsing and the 50-feature matrix |
| matplotlib | Score, threshold, and comparison charts |
| Chart.js | Charts on the live demo |
