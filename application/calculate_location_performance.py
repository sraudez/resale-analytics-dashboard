from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from infrastructure.csv_sales_repository import load_processed_sales_csv


def _prepare_location_frame(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["item_price"] = pd.to_numeric(working["item_price"], errors="coerce")
    working["state"] = working["state"].fillna("Unknown").astype(str).str.strip()
    working["state"] = working["state"].replace({"": "Unknown"})
    return working


def build_location_performance(df: pd.DataFrame) -> pd.DataFrame:
    location = (
        df.groupby("state", dropna=False)
        .agg(
            items_sold=("item_price", "count"),
            gross_revenue=("item_price", "sum"),
        )
        .reset_index()
        .sort_values(by=["items_sold", "gross_revenue"], ascending=[False, False])
    )
    location["gross_revenue"] = location["gross_revenue"].round(2)
    return location


def save_outputs(df: pd.DataFrame, csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate buyer state performance from cleaned data.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/depop_sales_clean.csv"),
        help="Path to cleaned sales CSV.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("data/processed/location_performance.csv"),
        help="Path for location performance CSV output.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("data/processed/location_performance.json"),
        help="Path for location performance JSON output.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of top states to print in terminal preview.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_df = load_processed_sales_csv(args.input)
    location_df = build_location_performance(_prepare_location_frame(cleaned_df))
    save_outputs(location_df, args.output_csv, args.output_json)

    print("Location performance CSV saved:", args.output_csv)
    print("Location performance JSON saved:", args.output_json)
    print()
    print(f"Top {args.top_n} states by items sold:")
    print(location_df.head(args.top_n).to_string(index=False))


if __name__ == "__main__":
    main()
