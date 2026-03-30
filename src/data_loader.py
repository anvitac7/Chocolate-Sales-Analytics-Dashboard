"""
data_loader.py
--------------
Responsible for reading the raw CSV file and returning a clean DataFrame.
Uses Streamlit's caching to avoid re-reading on every rerun.
"""

import pandas as pd
import streamlit as st
from pathlib import Path


# ─── Constants ────────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "chocolate_sales.csv"


# ─── Loader ───────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_raw_data(path: str = str(DATA_PATH)) -> pd.DataFrame:
    """
    Load the raw chocolate sales CSV and return as a DataFrame.

    Parameters
    ----------
    path : str
        Absolute path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Raw DataFrame (no preprocessing applied yet).

    Raises
    ------
    FileNotFoundError
        If the CSV file is missing at the expected path.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {p}\n"
            "Please place 'chocolate_sales.csv' inside the data/ directory."
        )
    df = pd.read_csv(p)
    return df


def get_data(path: str = str(DATA_PATH)) -> pd.DataFrame:
    """
    Public entry point: load raw data, then preprocess.
    Imported by app.py so there is a single call site.
    """
    from src.preprocessing import preprocess  # avoid circular at import time
    raw = load_raw_data(path)
    return preprocess(raw)
