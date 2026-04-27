from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from application.calculate_monthly_performance import (
    _prepare_monthly_frame,
    build_monthly_performance,
    save_outputs,
)
from application.clean_sales_data import clean_sales_dataframe
from infrastructure.csv_sales_repository import load_raw_sales_csv


def test_prepare_monthly_frame_converts_dates_numbers_and_month() -> None:
    df = pd.DataFrame(
        [
            {
                "date_of_sale": "2024-10-25",
                "item_price": "10.5",
                "estimated_net_before_cogs": "8.25",
                "days_to_sell": "2",
            }
        ]
    )
    prepared = _prepare_monthly_frame(df)
    row = prepared.iloc[0]
    assert str(row["date_of_sale"].date()) == "2024-10-25"
    assert row["item_price"] == 10.5
    assert row["estimated_net_before_cogs"] == 8.25
    assert row["days_to_sell"] == 2
    assert row["month"] == "2024-10"


def test_build_monthly_performance_real_dataset_matches_expected_values() -> None:
    raw_df = load_raw_sales_csv(Path("data/depop_sales_raw.csv"))
    cleaned_df = clean_sales_dataframe(raw_df, drop_pii=True)
    monthly = build_monthly_performance(_prepare_monthly_frame(cleaned_df))

    expected = [
        {
            "month": "2024-10",
            "items_sold": 11,
            "gross_revenue": 145.5,
            "estimated_net_before_cogs": 125.6,
            "average_days_to_sell": 2.36,
        },
        {
            "month": "2024-11",
            "items_sold": 61,
            "gross_revenue": 543.25,
            "estimated_net_before_cogs": 450.23,
            "average_days_to_sell": 2.18,
        },
        {
            "month": "2024-12",
            "items_sold": 49,
            "gross_revenue": 680.5,
            "estimated_net_before_cogs": 541.15,
            "average_days_to_sell": 4.98,
        },
        {
            "month": "2025-01",
            "items_sold": 4,
            "gross_revenue": 44.0,
            "estimated_net_before_cogs": 37.15,
            "average_days_to_sell": 4.0,
        },
    ]

    assert monthly.to_dict(orient="records") == expected


def test_save_outputs_writes_monthly_csv_and_json(tmp_path: Path) -> None:
    monthly_df = pd.DataFrame(
        [
            {
                "month": "2024-10",
                "items_sold": 11,
                "gross_revenue": 145.5,
                "estimated_net_before_cogs": 125.6,
                "average_days_to_sell": 2.36,
            }
        ]
    )
    csv_path = tmp_path / "monthly_performance.csv"
    json_path = tmp_path / "monthly_performance.json"

    save_outputs(monthly_df, csv_path, json_path)

    loaded_csv = pd.read_csv(csv_path)
    loaded_json = json.loads(json_path.read_text(encoding="utf-8"))

    assert loaded_csv.shape == (1, 5)
    assert loaded_csv.iloc[0]["month"] == "2024-10"
    assert loaded_json[0]["month"] == "2024-10"
    assert loaded_json[0]["gross_revenue"] == 145.5
