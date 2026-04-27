from __future__ import annotations

from pathlib import Path

import pandas as pd

from application.clean_sales_data import (
    build_sanity_report,
    clean_sales_dataframe,
    parse_currency,
)
from infrastructure.csv_sales_repository import load_raw_sales_csv


def test_parse_currency_handles_common_tokens() -> None:
    assert parse_currency("$8.50") == 8.5
    assert parse_currency('="-"') == 0.0
    assert parse_currency("N/A") == 0.0
    assert parse_currency("") == 0.0
    assert parse_currency(None) == 0.0


def test_clean_sales_dataframe_transforms_fields_and_drops_pii() -> None:
    sample = pd.DataFrame(
        [
            {
                "Date of sale": "10/25/2024",
                "Time of sale": "8:29 AM",
                "Date of listing": "10/23/2024",
                "Bundle": "No",
                "Bundle - amount of items": "N/A",
                "Buyer": "buyer123",
                "Brand": "Other",
                "Description": "Sample",
                "Size": "L",
                "Item price": "$8.50",
                "Buyer shipping cost": "$6.29",
                "Total": "$15.54",
                "USPS Cost": "$0.00",
                "Depop fee": "$0.96",
                "Depop Payments fee": "$1.12",
                "Buyer Marketplace Fee": "$0.68",
                "Boosting fee": '="-"',
                "Payment type": "STRIPE",
                "Estimated payout date": "10/29/2024",
                "Payout arrival date": "11/02/2024",
                "Category": "Tops",
                "Name": "John Doe",
                "Address Line 1": "123 Main",
                "Address Line 2": "Apt 1",
                "City": "Perris",
                "State": "CA",
                "Post Code": "92571",
                "Country": "US",
                "US Sales tax": "$0.75",
                "Refunded to buyer amount": "N/A",
                "Fees refunded to seller": "N/A",
            }
        ]
    )

    cleaned = clean_sales_dataframe(sample, drop_pii=True)
    row = cleaned.iloc[0]

    assert "buyer_username" not in cleaned.columns
    assert "Name" not in cleaned.columns
    assert "Address Line 1" not in cleaned.columns
    assert row["date_of_sale"] == "2024-10-25"
    assert row["date_of_listing"] == "2024-10-23"
    assert row["bundle"] == False
    assert row["bundle_item_count"] == 0
    assert row["item_price"] == 8.5
    assert row["seller_fees"] == 2.08
    assert row["estimated_net_before_cogs"] == 6.42
    assert row["days_to_sell"] == 2


def test_feature1_real_dataset_matches_expected_sanity_metrics() -> None:
    raw_df = load_raw_sales_csv(Path("data/depop_sales_raw.csv"))
    cleaned = clean_sales_dataframe(raw_df, drop_pii=True)
    report = build_sanity_report(cleaned)

    assert report.record_count == 125
    assert report.sale_date_min == "2024-10-25"
    assert report.sale_date_max == "2025-01-09"
    assert report.gross_item_revenue == 1413.25
    assert report.total_seller_fees == 151.62
    assert report.estimated_net_before_cogs == 1154.13
    assert report.avg_days_to_sell == 3.35
    assert report.median_days_to_sell == 2.0
    assert "buyer_username" not in cleaned.columns
