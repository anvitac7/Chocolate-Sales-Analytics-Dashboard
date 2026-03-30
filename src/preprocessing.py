"""
preprocessing.py
----------------
All data-cleaning and feature-engineering logic lives here.
Returns a fully processed DataFrame ready for visualisation.
"""

import pandas as pd
import numpy as np


# ─── Column name map ──────────────────────────────────────────────────────────
COLUMN_RENAME = {
    "Sales Person": "salesperson",
    "Country":      "country",
    "Product":      "product",
    "Date":         "date",
    "Amount":       "amount",
    "Boxes Shipped":"boxes_shipped",
}


def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise column names: lower-snake-case."""
    df = df.rename(columns=COLUMN_RENAME)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def _parse_amount(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert Amount from '$1,234.56' string to float.
    Handles:  '$…'  '£…'  '€…'  plain numeric strings.
    Works with both object dtype and newer pandas StringDtype.
    """
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace(r"[\$£€,\s]", "", regex=True)
        .str.strip()
        .pipe(pd.to_numeric, errors="coerce")
    )
    return df


def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse dates flexibly (handles '1-Jan-23', '01-Jan-2023', ISO, etc.).
    Creates temporal feature columns for time-series analysis.
    """
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, format="mixed")

    df["year"]        = df["date"].dt.year
    df["month"]       = df["date"].dt.month
    df["month_name"]  = df["date"].dt.strftime("%b")
    df["month_year"]  = df["date"].dt.to_period("M")
    df["quarter"]     = df["date"].dt.quarter
    df["day_of_week"] = df["date"].dt.day_name()
    df["week"]        = df["date"].dt.isocalendar().week.astype(int)

    return df


def _handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing / null values.
    Drop rows where critical fields are null.
    Fill non-critical numeric nulls with column median.
    """
    critical = ["salesperson", "country", "product", "date", "amount"]
    before = len(df)
    df = df.dropna(subset=critical)
    after = len(df)
    if before != after:
        print(f"[preprocessing] Dropped {before - after} rows with null critical fields.")

    if "boxes_shipped" in df.columns and df["boxes_shipped"].isnull().any():
        df["boxes_shipped"] = df["boxes_shipped"].fillna(df["boxes_shipped"].median())

    return df


def _derive_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create business-relevant derived columns:
      revenue_per_box     : Revenue efficiency per shipped box
      product_category    : Inferred from product name keywords
      region              : Grouped countries into broader regions
      high_value_order    : Boolean flag – order in top-25% by amount
    """
    # Ensure numeric types
    df["amount"]       = pd.to_numeric(df["amount"],       errors="coerce")
    df["boxes_shipped"]= pd.to_numeric(df["boxes_shipped"],errors="coerce")

    # Revenue per box
    df["revenue_per_box"] = (
        df["amount"] / df["boxes_shipped"].replace(0, np.nan)
    ).round(2)

    # Product category from keywords
    def categorise(name: str) -> str:
        n = str(name).lower()
        if "dark" in n:
            return "Dark Chocolate"
        if any(k in n for k in ["milk", "white", "eclairs", "smooth"]):
            return "Milk / White"
        if any(k in n for k in ["almond", "nut", "hazel", "peanut", "coconut"]):
            return "Nut & Crunch"
        if any(k in n for k in ["caramel", "toffee", "praline", "truffle"]):
            return "Premium / Caramel"
        return "Specialty"

    df["product_category"] = df["product"].apply(categorise)

    # Region grouping
    region_map = {
        "USA": "Americas", "Canada": "Americas",
        "UK": "Europe",
        "Australia": "Asia-Pacific", "New Zealand": "Asia-Pacific",
        "India": "Asia-Pacific",
    }
    df["region"] = df["country"].map(region_map).fillna("Other")

    # High-value flag (top quartile by amount)
    q75 = df["amount"].quantile(0.75)
    df["high_value_order"] = df["amount"] >= q75

    return df


def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate rows, keeping the first occurrence."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before != after:
        print(f"[preprocessing] Removed {before - after} duplicate rows.")
    return df


# ─── Public API ───────────────────────────────────────────────────────────────
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Master pipeline: accepts a raw DataFrame and returns a clean,
    feature-enriched DataFrame.

    Steps
    -----
    1. Standardise column names
    2. Remove duplicates
    3. Parse Amount to float
    4. Parse Date to datetime + temporal features
    5. Handle missing values
    6. Derive business features
    """
    df = _clean_column_names(df)
    df = _remove_duplicates(df)
    df = _parse_amount(df)
    df = _parse_dates(df)
    df = _handle_missing(df)
    df = _derive_features(df)
    df = df.reset_index(drop=True)
    return df


def apply_filters(
    df: pd.DataFrame,
    date_range: tuple,
    countries: list,
    products: list,
    salespersons: list,
) -> pd.DataFrame:
    """
    Apply sidebar filter selections and return the filtered slice.
    """
    start = pd.Timestamp(date_range[0])
    end   = pd.Timestamp(date_range[1])
    mask = (
        (df["date"] >= start) &
        (df["date"] <= end)   &
        (df["country"].isin(countries)) &
        (df["product"].isin(products))  &
        (df["salesperson"].isin(salespersons))
    )
    return df[mask].copy()
