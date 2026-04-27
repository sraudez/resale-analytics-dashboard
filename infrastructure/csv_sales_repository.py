from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_raw_sales_csv(path: Path) -> pd.DataFrame:
    """Load Depop raw CSV and preserve original text content."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def load_processed_sales_csv(path: Path) -> pd.DataFrame:
    """Load processed sales CSV."""
    return pd.read_csv(path)


def save_processed_sales_csv(df: pd.DataFrame, path: Path) -> None:
    """Save processed sales CSV to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
