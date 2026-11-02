# Dashboard data provenance

- Source: [`NCAA_Seed_Training_Set2.0.csv`](../NCAA_Seed_Training_Set2.0.csv).
- SHA-256 of reviewed input: `327a188f26aadb5b734e4dffa553fa31fb82d8ea739d21897c97b69a5f53d953`.
- Refresh descriptive counts from the repository root: `python scripts/refresh_dashboard_data.py`.
- `data.json` stores the displayed chart series. Expand each chart's table to inspect exact values.
- The refresh script does not train or validate a predictive model. Captions and result claims need review if the input changes.

Selection means a nonempty Overall Seed. Counts are team-seasons, not unique teams. The dashboard does not show an inferred ROC or precision-recall curve; saved predictions are unavailable.

## Interactive analysis

The dashboard filters the supplied team-season records by season and conference. Selection rates use selected rows divided by all matching rows; median NET excludes missing NET values. Conference charts show the top 12 rates with sample sizes. The record table shows the first 50 matching rows; CSV export includes all matching rows.
