
from pathlib import Path
import pandas as pd

FEATURES = [
    "NDVI",
    "EVI",
    "NDMI",
    "SAVI",
    "BSI",
    "NBR",
]


def find_first(paths):
    for path in paths:
        if path.exists():
            return path
    return None


def load_dataset(csv_path):
    data = pd.read_csv(csv_path)

    required = ["month", "sample_id"] + FEATURES

    missing = [
        column for column in required
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    data["month"] = data["month"].astype(str)

    data["month_dt"] = pd.to_datetime(
        data["month"],
        format="%Y-%m",
        errors="coerce"
    )

    data["sample_id"] = pd.to_numeric(
        data["sample_id"],
        errors="coerce"
    )

    for column in FEATURES:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data = data.dropna(
        subset=["month_dt", "sample_id"]
    ).copy()

    data["sample_id"] = data["sample_id"].astype(int)

    return data.sort_values(
        ["sample_id", "month_dt"]
    ).reset_index(drop=True)
