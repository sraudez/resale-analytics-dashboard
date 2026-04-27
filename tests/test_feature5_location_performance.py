from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from application.calculate_location_performance import (
    _prepare_location_frame,
    build_location_performance,
    save_outputs,
)
from application.clean_sales_data import clean_sales_dataframe
from infrastructure.csv_sales_repository import load_raw_sales_csv


def test_prepare_location_frame_converts_price_and_normalizes_state() -> None:
    df = pd.DataFrame(
        [
            {"state": " CA ", "item_price": "10.5"},
            {"state": "", "item_price": "N/A"},
        ]
    )
    prepared = _prepare_location_frame(df)

    assert prepared.iloc[0]["state"] == "CA"
    assert prepared.iloc[1]["state"] == "Unknown"
    assert prepared.iloc[0]["item_price"] == 10.5
    assert pd.isna(prepared.iloc[1]["item_price"])


def test_build_location_performance_real_dataset_matches_readme_top_states() -> None:
    raw_df = load_raw_sales_csv(Path("data/depop_sales_raw.csv"))
    cleaned_df = clean_sales_dataframe(raw_df, drop_pii=True)
    location = build_location_performance(_prepare_location_frame(cleaned_df))

    top10 = location.head(10).to_dict(orient="records")
    assert top10 == [
        {"state": "CA", "items_sold": 17, "gross_revenue": 197.5},
        {"state": "TX", "items_sold": 14, "gross_revenue": 169.5},
        {"state": "FL", "items_sold": 9, "gross_revenue": 106.0},
        {"state": "NY", "items_sold": 6, "gross_revenue": 66.5},
        {"state": "PA", "items_sold": 6, "gross_revenue": 44.0},
        {"state": "IN", "items_sold": 5, "gross_revenue": 50.0},
        {"state": "NC", "items_sold": 5, "gross_revenue": 27.6},
        {"state": "GA", "items_sold": 4, "gross_revenue": 46.5},
        {"state": "NJ", "items_sold": 4, "gross_revenue": 41.0},
        {"state": "IL", "items_sold": 4, "gross_revenue": 24.75},
    ]


def test_save_outputs_writes_location_csv_and_json(tmp_path: Path) -> None:
    location_df = pd.DataFrame([{"state": "CA", "items_sold": 2, "gross_revenue": 20.0}])
    csv_path = tmp_path / "location_performance.csv"
    json_path = tmp_path / "location_performance.json"

    save_outputs(location_df, csv_path, json_path)

    loaded_csv = pd.read_csv(csv_path)
    loaded_json = json.loads(json_path.read_text(encoding="utf-8"))

    assert loaded_csv.shape == (1, 3)
    assert loaded_csv.iloc[0]["state"] == "CA"
    assert loaded_json[0]["state"] == "CA"
    assert loaded_json[0]["gross_revenue"] == 20.0
