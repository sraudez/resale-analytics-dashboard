from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from infrastructure.csv_sales_repository import load_processed_sales_csv


NUMERIC_COLUMNS = ["item_price", "estimated_net_before_cogs", "days_to_sell"]


def _prepare_monthly_frame(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["date_of_sale"] = pd.to_datetime(working["date_of_sale"], errors="coerce")
    for column in NUMERIC_COLUMNS:
        if column in working.columns:
            working[column] = pd.to_numeric(working[column], errors="coerce")
    working["month"] = working["date_of_sale"].dt.to_period("M").astype(str)
    return working


def build_monthly_performance(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby("month", dropna=False)
        .agg(
            items_sold=("item_price", "count"),
            gross_revenue=("item_price", "sum"),
            estimated_net_before_cogs=("estimated_net_before_cogs", "sum"),
            average_days_to_sell=("days_to_sell", "mean"),
        )
        .reset_index()
        .sort_values("month")
    )
    monthly["gross_revenue"] = monthly["gross_revenue"].round(2)
    monthly["estimated_net_before_cogs"] = monthly["estimated_net_before_cogs"].round(2)
    monthly["average_days_to_sell"] = monthly["average_days_to_sell"].round(2)
    return monthly


def save_outputs(df: pd.DataFrame, csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate monthly sales performance from cleaned data.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/depop_sales_clean.csv"),
        help="Path to cleaned sales CSV.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("data/processed/monthly_performance.csv"),
        help="Path for monthly performance CSV output.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("data/processed/monthly_performance.json"),
        help="Path for monthly performance JSON output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_df = load_processed_sales_csv(args.input)
    monthly_df = build_monthly_performance(_prepare_monthly_frame(cleaned_df))
    save_outputs(monthly_df, args.output_csv, args.output_json)

    print("Monthly performance CSV saved:", args.output_csv)
    print("Monthly performance JSON saved:", args.output_json)
    print()
    print(monthly_df.to_string(index=False))


if __name__ == "__main__":
    main()
