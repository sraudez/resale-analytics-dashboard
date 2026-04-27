from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from infrastructure.csv_sales_repository import load_processed_sales_csv


NUMERIC_COLUMNS = [
    "item_price",
    "total",
    "seller_fees",
    "estimated_net_before_cogs",
    "days_to_sell",
]


def _to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    converted = df.copy()
    for column in NUMERIC_COLUMNS:
        if column in converted.columns:
            converted[column] = pd.to_numeric(converted[column], errors="coerce")
    return converted


def build_kpi_summary(df: pd.DataFrame) -> dict[str, float | int | str]:
    kpis: dict[str, float | int | str] = {
        "record_count": int(len(df)),
        "sale_period_start": str(df["date_of_sale"].min()),
        "sale_period_end": str(df["date_of_sale"].max()),
        "gross_item_revenue": round(float(df["item_price"].sum()), 2),
        "total_transaction_value": round(float(df["total"].sum()), 2),
        "estimated_net_before_cogs": round(float(df["estimated_net_before_cogs"].sum()), 2),
        "total_seller_fees": round(float(df["seller_fees"].sum()), 2),
        "average_item_sale_price": round(float(df["item_price"].mean()), 2),
        "median_item_sale_price": round(float(df["item_price"].median()), 2),
        "average_days_to_sell": round(float(df["days_to_sell"].mean()), 2),
        "median_days_to_sell": round(float(df["days_to_sell"].median()), 2),
    }
    return kpis


def save_kpi_summary_json(kpis: dict[str, float | int | str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(kpis, indent=2), encoding="utf-8")


def save_kpi_summary_csv(kpis: dict[str, float | int | str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [{"metric": key, "value": value} for key, value in kpis.items()]
    pd.DataFrame(rows).to_csv(output_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate headline KPI summary from cleaned sales data.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/depop_sales_clean.csv"),
        help="Path to cleaned sales CSV.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("data/processed/kpi_summary.json"),
        help="Path for KPI JSON output.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("data/processed/kpi_summary.csv"),
        help="Path for KPI CSV output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_df = load_processed_sales_csv(args.input)
    cleaned_df = _to_numeric(cleaned_df)
    kpis = build_kpi_summary(cleaned_df)

    save_kpi_summary_json(kpis, args.output_json)
    save_kpi_summary_csv(kpis, args.output_csv)

    print("KPI summary JSON saved:", args.output_json)
    print("KPI summary CSV saved:", args.output_csv)
    for metric_name, metric_value in kpis.items():
        print(f"{metric_name}: {metric_value}")


if __name__ == "__main__":
    main()
