from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from application.calculate_performance import _build_group_performance, _to_numeric, save_outputs
from application.clean_sales_data import clean_sales_dataframe
from infrastructure.csv_sales_repository import load_raw_sales_csv


def test_build_group_performance_basic_aggregation_and_sorting() -> None:
    df = pd.DataFrame(
        [
            {"category": "Tops", "item_price": 5.0, "days_to_sell": 2},
            {"category": "Tops", "item_price": 7.0, "days_to_sell": 4},
            {"category": "Bottoms", "item_price": 20.0, "days_to_sell": 1},
        ]
    )

    grouped = _build_group_performance(df, "category")

    assert grouped.iloc[0]["category"] == "Bottoms"
    assert grouped.iloc[0]["gross_revenue"] == 20.0
    assert grouped.iloc[0]["items_sold"] == 1
    assert grouped.iloc[1]["category"] == "Tops"
    assert grouped.iloc[1]["gross_revenue"] == 12.0
    assert grouped.iloc[1]["average_price"] == 6.0
    assert grouped.iloc[1]["average_days_to_sell"] == 3.0


def test_feature3_real_dataset_matches_readme_top_values() -> None:
    raw_df = load_raw_sales_csv(Path("data/depop_sales_raw.csv"))
    cleaned = clean_sales_dataframe(raw_df, drop_pii=True)
    cleaned = _to_numeric(cleaned)

    category = _build_group_performance(cleaned, "category")
    brand = _build_group_performance(cleaned, "brand")

    assert category.iloc[0].to_dict() == {
        "category": "Tops",
        "items_sold": 67,
        "gross_revenue": 640.25,
        "average_price": 9.56,
        "average_days_to_sell": 3.13,
    }
    assert brand.iloc[0].to_dict() == {
        "brand": "Other",
        "items_sold": 42,
        "gross_revenue": 382.5,
        "average_price": 9.11,
        "average_days_to_sell": 3.17,
    }


def test_save_outputs_writes_csv_and_json(tmp_path: Path) -> None:
    df = pd.DataFrame(
        [
            {
                "brand": "A",
                "items_sold": 1,
                "gross_revenue": 10.0,
                "average_price": 10.0,
                "average_days_to_sell": 2.0,
            }
        ]
    )
    csv_path = tmp_path / "brand_performance.csv"
    json_path = tmp_path / "brand_performance.json"

    save_outputs(df, csv_path, json_path)

    loaded_csv = pd.read_csv(csv_path)
    loaded_json = json.loads(json_path.read_text(encoding="utf-8"))

    assert loaded_csv.shape == (1, 5)
    assert loaded_csv.iloc[0]["brand"] == "A"
    assert loaded_json[0]["brand"] == "A"
    assert loaded_json[0]["gross_revenue"] == 10.0
