from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from infrastructure.csv_sales_repository import load_processed_sales_csv


NUMERIC_COLUMNS = ["item_price", "days_to_sell"]


def _to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    converted = df.copy()
    for column in NUMERIC_COLUMNS:
        if column in converted.columns:
            converted[column] = pd.to_numeric(converted[column], errors="coerce")
    return converted


def _build_group_performance(df: pd.DataFrame, group_column: str) -> pd.DataFrame:
    grouped = (
        df.groupby(group_column, dropna=False)
        .agg(
            items_sold=("item_price", "count"),
            gross_revenue=("item_price", "sum"),
            average_price=("item_price", "mean"),
            average_days_to_sell=("days_to_sell", "mean"),
        )
        .reset_index()
    )
    grouped["gross_revenue"] = grouped["gross_revenue"].round(2)
    grouped["average_price"] = grouped["average_price"].round(2)
    grouped["average_days_to_sell"] = grouped["average_days_to_sell"].round(2)
    grouped = grouped.sort_values(by=["gross_revenue", "items_sold"], ascending=[False, False])
    return grouped


def save_outputs(df: pd.DataFrame, csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate category and brand performance from cleaned sales data."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/depop_sales_clean.csv"),
        help="Path to cleaned sales CSV.",
    )
    parser.add_argument(
        "--output-category-csv",
        type=Path,
        default=Path("data/processed/category_performance.csv"),
        help="Path for category performance CSV output.",
    )
    parser.add_argument(
        "--output-category-json",
        type=Path,
        default=Path("data/processed/category_performance.json"),
        help="Path for category performance JSON output.",
    )
    parser.add_argument(
        "--output-brand-csv",
        type=Path,
        default=Path("data/processed/brand_performance.csv"),
        help="Path for brand performance CSV output.",
    )
    parser.add_argument(
        "--output-brand-json",
        type=Path,
        default=Path("data/processed/brand_performance.json"),
        help="Path for brand performance JSON output.",
    )
    parser.add_argument(
        "--brand-top-n",
        type=int,
        default=10,
        help="Number of top brands to show in terminal preview (file outputs include all brands).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_df = load_processed_sales_csv(args.input)
    cleaned_df = _to_numeric(cleaned_df)

    category_performance = _build_group_performance(cleaned_df, "category")
    brand_performance = _build_group_performance(cleaned_df, "brand")

    save_outputs(category_performance, args.output_category_csv, args.output_category_json)
    save_outputs(brand_performance, args.output_brand_csv, args.output_brand_json)

    print("Category performance CSV saved:", args.output_category_csv)
    print("Category performance JSON saved:", args.output_category_json)
    print("Brand performance CSV saved:", args.output_brand_csv)
    print("Brand performance JSON saved:", args.output_brand_json)
    print()
    print("Top categories by gross revenue:")
    print(category_performance.head(5).to_string(index=False))
    print()
    print(f"Top {args.brand_top_n} brands by gross revenue:")
    print(brand_performance.head(args.brand_top_n).to_string(index=False))


if __name__ == "__main__":
    main()
