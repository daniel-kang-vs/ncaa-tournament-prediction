"""Refresh descriptive chart values from the committed CSV; does not train a model."""
from pathlib import Path
import csv
import json
import collections

root = Path(__file__).resolve().parents[1]
with (root / 'NCAA_Seed_Training_Set2.0.csv').open(newline="") as stream:
    rows = list(csv.DictReader(stream))
target = root / "docs" / "data.json"
data = json.loads(target.read_text())
charts = data["charts"]
missing = sorted(
    ((key, sum(row[key].strip() in ("", "?", "NA", "nan") for row in rows))
     for key in rows[0]), key=lambda item: -item[1]
)[:10]
def selected(row):
    return bool(row["Overall Seed"].strip())

positive = sum(selected(row) for row in rows)
charts[0]["series"][0]["values"] = [len(rows) - positive, positive]
seasons = sorted({row["Season"] for row in rows})
charts[1]["labels"] = seasons
charts[1]["series"][0]["values"] = [sum(r["Season"] == s for r in rows) for s in seasons]
charts[1]["series"][1]["values"] = [sum(r["Season"] == s and selected(r) for r in rows) for s in seasons]
conferences = collections.Counter(r["Conference"] for r in rows if selected(r)).most_common(10)
charts[2]["labels"] = [key for key, value in conferences]
charts[2]["series"][0]["values"] = [value for key, value in conferences]
charts[3]["labels"] = [key for key, value in missing]
charts[3]["series"][0]["values"] = [value for key, value in missing]
data["records"] = [{"season": r["Season"], "team": r["Team"], "conference": r["Conference"], "selected": selected(r), "seed": float(r["Overall Seed"]) if selected(r) else None, "net": float(r["NET Rank"]) if r["NET Rank"].strip() else None} for r in rows]
target.write_text(json.dumps(data, indent=2) + "\n")
print(f"Refreshed descriptive charts from {len(rows):,} input rows; review captions if the source changed.")
