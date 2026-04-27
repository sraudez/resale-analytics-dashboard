from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from application.calculate_kpis import (
    _to_numeric,
    build_kpi_summary,
    save_kpi_summary_csv,
    save_kpi_summary_json,
)
from application.clean_sales_data import clean_sales_dataframe
from infrastructure.csv_sales_repository import load_raw_sales_csv


def test_to_numeric_converts_expected_columns() -> None:
    df = pd.DataFrame(
        [
            {
                "item_price": "10.5",
                "total": "15.2",
                "seller_fees": "2.3",
                "estimated_net_before_cogs": "8.2",
                "days_to_sell": "3",
            }
        ]
    )

    converted = _to_numeric(df)
    assert converted["item_price"].iloc[0] == 10.5
    assert converted["total"].iloc[0] == 15.2
    assert converted["seller_fees"].iloc[0] == 2.3
    assert converted["estimated_net_before_cogs"].iloc[0] == 8.2
    assert converted["days_to_sell"].iloc[0] == 3


def test_build_kpi_summary_real_dataset_matches_expected_values() -> None:
    raw_df = load_raw_sales_csv(Path("data/depop_sales_raw.csv"))
    cleaned = clean_sales_dataframe(raw_df, drop_pii=True)
    cleaned = _to_numeric(cleaned)
    kpis = build_kpi_summary(cleaned)

    assert kpis == {
        "record_count": 125,
        "sale_period_start": "2024-10-25",
        "sale_period_end": "2025-01-09",
        "gross_item_revenue": 1413.25,
        "total_transaction_value": 2472.49,
        "estimated_net_before_cogs": 1154.13,
        "total_seller_fees": 151.62,
        "average_item_sale_price": 11.31,
        "median_item_sale_price": 10.0,
        "average_days_to_sell": 3.35,
        "median_days_to_sell": 2.0,
    }


def test_kpi_savers_write_json_and_csv(tmp_path: Path) -> None:
    kpis = {
        "record_count": 2,
        "sale_period_start": "2024-01-01",
        "sale_period_end": "2024-01-02",
        "gross_item_revenue": 10.0,
    }
    json_path = tmp_path / "kpi_summary.json"
    csv_path = tmp_path / "kpi_summary.csv"

    save_kpi_summary_json(kpis, json_path)
    save_kpi_summary_csv(kpis, csv_path)

    loaded_json = json.loads(json_path.read_text(encoding="utf-8"))
    loaded_csv = pd.read_csv(csv_path)

    assert loaded_json == kpis
    assert set(loaded_csv.columns) == {"metric", "value"}
    assert set(loaded_csv["metric"].tolist()) == set(kpis.keys())
