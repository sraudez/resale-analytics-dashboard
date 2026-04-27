from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from infrastructure.csv_sales_repository import load_raw_sales_csv, save_processed_sales_csv


DATE_COLUMNS = [
    "Date of sale",
    "Date of listing",
    "Estimated payout date",
    "Payout arrival date",
]

CURRENCY_COLUMNS = [
    "Item price",
    "Buyer shipping cost",
    "Total",
    "USPS Cost",
    "Depop fee",
    "Depop Payments fee",
    "Buyer Marketplace Fee",
    "Boosting fee",
    "US Sales tax",
    "Refunded to buyer amount",
    "Fees refunded to seller",
]

PII_COLUMNS = [
    "Buyer",
    "Name",
    "Address Line 1",
    "Address Line 2",
    "City",
    "Post Code",
]

RENAME_MAP = {
    "Date of sale": "date_of_sale",
    "Time of sale": "time_of_sale",
    "Date of listing": "date_of_listing",
    "Bundle": "bundle",
    "Bundle - amount of items": "bundle_item_count",
    "Buyer": "buyer_username",
    "Brand": "brand",
    "Description": "description",
    "Size": "size",
    "Item price": "item_price",
    "Buyer shipping cost": "buyer_shipping_cost",
    "Total": "total",
    "USPS Cost": "usps_cost",
    "Depop fee": "depop_fee",
    "Depop Payments fee": "depop_payments_fee",
    "Buyer Marketplace Fee": "buyer_marketplace_fee",
    "Boosting fee": "boosting_fee",
    "Payment type": "payment_type",
    "Estimated payout date": "estimated_payout_date",
    "Payout arrival date": "payout_arrival_date",
    "Category": "category",
    "State": "state",
    "Country": "country",
    "US Sales tax": "us_sales_tax",
    "Refunded to buyer amount": "refunded_to_buyer_amount",
    "Fees refunded to seller": "fees_refunded_to_seller",
}

NULL_TOKENS = {"", "N/A", "n/a", "NA", "na", "-", '="-"', '="- "', "null", "None"}


@dataclass
class SanityReport:
    record_count: int
    sale_date_min: str
    sale_date_max: str
    gross_item_revenue: float
    total_seller_fees: float
    estimated_net_before_cogs: float
    avg_days_to_sell: float
    median_days_to_sell: float


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _is_null_token(value: Any) -> bool:
    return _normalize_text(value) in NULL_TOKENS


def parse_currency(value: Any) -> float:
    text = _normalize_text(value)
    if _is_null_token(text):
        return 0.0
    cleaned = text.replace("$", "").replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def clean_sales_dataframe(df: pd.DataFrame, drop_pii: bool = True) -> pd.DataFrame:
    working_df = df.copy()

    for column in DATE_COLUMNS:
        working_df[column] = pd.to_datetime(
            working_df[column].map(lambda v: None if _is_null_token(v) else _normalize_text(v)),
            errors="coerce",
            format="%m/%d/%Y",
        )

    for column in CURRENCY_COLUMNS:
        working_df[column] = working_df[column].map(parse_currency).astype(float)

    working_df["days_to_sell"] = (
        working_df["Date of sale"] - working_df["Date of listing"]
    ).dt.days

    working_df["seller_fees"] = (
        working_df["Depop fee"]
        + working_df["Depop Payments fee"]
        + working_df["Boosting fee"]
        - working_df["Fees refunded to seller"]
    )

    working_df["estimated_net_before_cogs"] = (
        working_df["Item price"]
        - working_df["seller_fees"]
        - working_df["Refunded to buyer amount"]
    )
    working_df["seller_fees"] = working_df["seller_fees"].round(2)
    working_df["estimated_net_before_cogs"] = working_df["estimated_net_before_cogs"].round(2)

    if drop_pii:
        columns_to_drop = [column for column in PII_COLUMNS if column in working_df.columns]
        working_df = working_df.drop(columns=columns_to_drop)

    working_df = working_df.rename(columns=RENAME_MAP)

    date_output_columns = [
        "date_of_sale",
        "date_of_listing",
        "estimated_payout_date",
        "payout_arrival_date",
    ]
    for column in date_output_columns:
        if column in working_df.columns:
            working_df[column] = working_df[column].dt.strftime("%Y-%m-%d")

    if "bundle" in working_df.columns:
        working_df["bundle"] = working_df["bundle"].map(lambda v: _normalize_text(v).lower() == "yes")

    if "bundle_item_count" in working_df.columns:
        working_df["bundle_item_count"] = (
            working_df["bundle_item_count"]
            .map(lambda v: 0 if _is_null_token(v) else int(float(_normalize_text(v))))
            .astype(int)
        )

    # Normalize likely categorical nulls for cleaner filtering in later features.
    for column in ["brand", "category", "size", "state", "country", "payment_type"]:
        if column in working_df.columns:
            working_df[column] = working_df[column].map(
                lambda v: "Unknown" if _is_null_token(v) else _normalize_text(v)
            )

    return working_df


def build_sanity_report(df: pd.DataFrame) -> SanityReport:
    return SanityReport(
        record_count=len(df),
        sale_date_min=str(df["date_of_sale"].min()),
        sale_date_max=str(df["date_of_sale"].max()),
        gross_item_revenue=round(float(df["item_price"].sum()), 2),
        total_seller_fees=round(float(df["seller_fees"].sum()), 2),
        estimated_net_before_cogs=round(float(df["estimated_net_before_cogs"].sum()), 2),
        avg_days_to_sell=round(float(df["days_to_sell"].mean()), 2),
        median_days_to_sell=round(float(df["days_to_sell"].median()), 2),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Depop sales data.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/depop_sales_raw.csv"),
        help="Path to the raw Depop CSV export.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/depop_sales_clean.csv"),
        help="Path for cleaned output CSV.",
    )
    parser.add_argument(
        "--keep-pii",
        action="store_true",
        help="Keep PII columns in output (for internal use only).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_df = load_raw_sales_csv(args.input)
    cleaned_df = clean_sales_dataframe(raw_df, drop_pii=not args.keep_pii)
    save_processed_sales_csv(cleaned_df, args.output)

    report = build_sanity_report(cleaned_df)
    print("Cleaned sales dataset saved:", args.output)
    print("records:", report.record_count)
    print("sale_date_range:", f"{report.sale_date_min} to {report.sale_date_max}")
    print("gross_item_revenue:", report.gross_item_revenue)
    print("total_seller_fees:", report.total_seller_fees)
    print("estimated_net_before_cogs:", report.estimated_net_before_cogs)
    print("avg_days_to_sell:", report.avg_days_to_sell)
    print("median_days_to_sell:", report.median_days_to_sell)


if __name__ == "__main__":
    main()
