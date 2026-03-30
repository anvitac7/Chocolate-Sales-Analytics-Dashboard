"""
utils.py
--------
Reusable utility functions shared across the dashboard:
  - Number formatting
  - Auto-generated business insights
  - Download helper
  - Colour palette
  - ML helpers: K-Means clustering, Linear Regression forecast, TS decomposition
"""

from __future__ import annotations

import warnings
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as scipy_stats

warnings.filterwarnings("ignore")


# ─── Colour Palette ───────────────────────────────────────────────────────────
PALETTE = {
    "primary":    "#6C3483",
    "secondary":  "#C0392B",
    "accent":     "#F39C12",
    "success":    "#1E8449",
    "danger":     "#C0392B",
    "muted":      "#95A5A6",
    "bg_dark":    "#1C1C2E",
    "bg_card":    "#2D2D44",
}

CHART_COLORS = [
    "#9B59B6", "#C0392B", "#F39C12", "#2ECC71",
    "#3498DB", "#E74C3C", "#1ABC9C", "#F1C40F",
    "#D35400", "#8E44AD",
]

PLOTLY_LAYOUT = dict(
    font          = dict(family="Inter, sans-serif", color="#F0E6FF"),
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(0,0,0,0)",
    margin        = dict(l=20, r=20, t=50, b=30),
    legend        = dict(bgcolor="rgba(0,0,0,0)", font_size=11),
    hoverlabel    = dict(bgcolor="#2D2D44", font_size=12,
                         font_family="Inter", font_color="#F0E6FF"),
)

# ─── Theme flag (set by app.py via configure_theme) ──────────────────────────
_DARK: bool = True


def configure_theme(dark: bool) -> None:
    """Update PLOTLY_LAYOUT and _DARK flag for every Streamlit rerun."""
    global _DARK
    _DARK = dark
    font_color = "#F0E6FF" if dark else "#1A0A2E"
    hover_bg   = "#2D2D44" if dark else "#FFFFFF"
    PLOTLY_LAYOUT["font"]       = dict(family="Inter, sans-serif", color=font_color)
    PLOTLY_LAYOUT["hoverlabel"] = dict(bgcolor=hover_bg, font_size=12,
                                       font_family="Inter", font_color=font_color)
    PLOTLY_LAYOUT["legend"]     = dict(bgcolor="rgba(0,0,0,0)", font_size=11,
                                       font_color=font_color)


# ─── Formatters ───────────────────────────────────────────────────────────────
def fmt_currency(value: float, decimals: int = 0) -> str:
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.{decimals}f}"


def fmt_number(value: float) -> str:
    return f"{int(value):,}"


def fmt_percent(value: float, decimals: int = 1) -> str:
    return f"{value * 100:.{decimals}f}%"


def delta_color(current: float, previous: float) -> str:
    return "normal" if current >= previous else "inverse"


# ─── Business Insights Generator ─────────────────────────────────────────────
def generate_insights(df: pd.DataFrame) -> list[dict]:
    """Auto-generate business insight cards from the filtered data."""
    insights = []
    if df.empty:
        return [{"icon": "⚠️", "title": "No Data",
                 "body": "Adjust your filters to see insights."}]

    top_sp     = df.groupby("salesperson")["amount"].sum().idxmax()
    top_sp_rev = df.groupby("salesperson")["amount"].sum().max()
    insights.append({
        "icon": "🏆", "title": "Star Performer",
        "body": (
            f"**{top_sp}** leads with **{fmt_currency(top_sp_rev)}** in revenue. "
            "Consider highlighting their techniques in team training."
        ),
    })

    top_country   = df.groupby("country")["amount"].sum().idxmax()
    country_share = df.groupby("country")["amount"].sum().max() / df["amount"].sum()
    insights.append({
        "icon": "🌍", "title": "Dominant Market",
        "body": (
            f"**{top_country}** contributes **{fmt_percent(country_share)}** of total revenue. "
            "Expanding inventory depth here could yield outsized returns."
        ),
    })

    top_prod     = df.groupby("product")["amount"].sum().idxmax()
    top_prod_rev = df.groupby("product")["amount"].sum().max()
    insights.append({
        "icon": "🍫", "title": "Best-Selling Product",
        "body": (
            f"**{top_prod}** generates **{fmt_currency(top_prod_rev)}**. "
            "Bundling this with lower performers may lift average order value."
        ),
    })

    monthly = df.groupby("month")["amount"].mean()
    if not monthly.empty:
        peak_month = monthly.idxmax()
        month_names = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
                       5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
                       9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        insights.append({
            "icon": "📈", "title": "Peak Season",
            "body": (
                f"**{month_names.get(peak_month, peak_month)}** is historically the strongest month. "
                "Pre-position stock and run promotions heading into this period."
            ),
        })

    best_rpb_prod = df.groupby("product")["revenue_per_box"].mean().idxmax()
    best_rpb      = df.groupby("product")["revenue_per_box"].mean().max()
    insights.append({
        "icon": "💡", "title": "Most Efficient Product",
        "body": (
            f"**{best_rpb_prod}** earns **{fmt_currency(best_rpb, 2)} per box** — "
            "the highest revenue efficiency. Prioritise in constrained-logistics markets."
        ),
    })

    hv_pct       = df["high_value_order"].mean()
    hv_rev_share = (
        df[df["high_value_order"]]["amount"].sum() / df["amount"].sum()
    )
    insights.append({
        "icon": "💎", "title": "High-Value Order Concentration",
        "body": (
            f"Only **{fmt_percent(hv_pct)}** of orders are high-value, yet they represent "
            f"**{fmt_percent(hv_rev_share)}** of total revenue — a classic Pareto pattern."
        ),
    })

    return insights


# ─── Download Helper ─────────────────────────────────────────────────────────
def get_download_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


# ─── KPI Helper ──────────────────────────────────────────────────────────────
def compute_kpis(df: pd.DataFrame, df_prev: pd.DataFrame | None = None) -> dict:
    kpis: dict = {}
    kpis["total_revenue"]   = df["amount"].sum()
    kpis["total_orders"]    = len(df)
    kpis["avg_order_value"] = df["amount"].mean() if len(df) else 0
    kpis["total_boxes"]     = df["boxes_shipped"].sum()
    kpis["top_product"]     = (
        df.groupby("product")["amount"].sum().idxmax() if len(df) else "—"
    )
    kpis["top_country"]     = (
        df.groupby("country")["amount"].sum().idxmax() if len(df) else "—"
    )
    kpis["revenue_per_box"] = (
        df["amount"].sum() / df["boxes_shipped"].sum()
        if df["boxes_shipped"].sum() > 0 else 0
    )

    if df_prev is not None and len(df_prev) > 0:
        kpis["total_revenue_delta"]   = kpis["total_revenue"]   - df_prev["amount"].sum()
        kpis["total_orders_delta"]    = kpis["total_orders"]     - len(df_prev)
        kpis["avg_order_value_delta"] = kpis["avg_order_value"]  - df_prev["amount"].mean()
        kpis["total_boxes_delta"]     = kpis["total_boxes"]      - df_prev["boxes_shipped"].sum()

    return kpis


# ═════════════════════════════════════════════════════════════════════════════
#  ADVANCED ANALYTICS HELPERS
# ═════════════════════════════════════════════════════════════════════════════

# ─── K-Means Clustering ──────────────────────────────────────────────────────
def run_kmeans_clustering(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """
    Segment salespersons into n_clusters groups using K-Means.

    Features used (all normalised before clustering):
      - total revenue
      - number of orders
      - average order value
      - average revenue per box

    Returns
    -------
    DataFrame with one row per salesperson plus columns:
      revenue, orders, avg_order, revenue_per_box, cluster (int), cluster_label (str)
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    grp = (
        df.groupby("salesperson")
        .agg(
            revenue         = ("amount",        "sum"),
            orders          = ("amount",        "count"),
            avg_order       = ("amount",        "mean"),
            revenue_per_box = ("revenue_per_box","mean"),
        )
        .reset_index()
        .dropna()
    )

    if len(grp) < n_clusters:
        grp["cluster"]       = 0
        grp["cluster_label"] = "All Performers"
        return grp

    features = ["revenue", "orders", "avg_order", "revenue_per_box"]
    X        = StandardScaler().fit_transform(grp[features])

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    grp["cluster"] = km.fit_predict(X)

    # Label clusters by their mean revenue rank (highest = High Performer)
    cluster_revenue = grp.groupby("cluster")["revenue"].mean().sort_values(ascending=False)
    labels_ordered  = ["High Performer", "Solid Contributor", "Growth Potential"]
    label_map       = {
        cluster_id: labels_ordered[rank]
        for rank, cluster_id in enumerate(cluster_revenue.index)
    }
    grp["cluster_label"] = grp["cluster"].map(label_map)

    return grp


# ─── ARIMA Forecast ──────────────────────────────────────────────────────────
def run_arima_forecast(
    df: pd.DataFrame,
    forecast_months: int = 3,
) -> tuple | None:
    """
    Auto-select ARIMA(p,d,q) via AIC grid search on monthly revenue, then
    forecast forward with 95% confidence intervals.

    Grid: p in {0,1,2}, d in {0,1}, q in {0,1,2}  (18 candidates).

    Returns
    -------
    (forecast_df, best_order, best_aic, fitted_vals, ts_history)
    or None if fewer than 8 months of data are available.
    """
    from statsmodels.tsa.arima.model import ARIMA

    ts = (
        df.set_index("date")["amount"]
        .resample("ME").sum()
        .asfreq("ME")
    )

    if len(ts) < 8:
        return None

    best_aic   = np.inf
    best_order = (1, 1, 1)
    best_model = None

    for p in range(0, 3):
        for d in range(0, 2):
            for q in range(0, 3):
                try:
                    m = ARIMA(ts, order=(p, d, q)).fit()
                    if m.aic < best_aic:
                        best_aic   = m.aic
                        best_order = (p, d, q)
                        best_model = m
                except Exception:
                    pass

    if best_model is None:
        return None

    fc        = best_model.get_forecast(steps=forecast_months)
    pred_mean = fc.predicted_mean
    ci        = fc.conf_int(alpha=0.05)

    forecast_df = pd.DataFrame({
        "date":      pred_mean.index,
        "predicted": np.maximum(pred_mean.values, 0),
        "ci_lower":  np.maximum(ci.iloc[:, 0].values, 0),
        "ci_upper":  ci.iloc[:, 1].values,
    })

    return forecast_df, best_order, best_aic, best_model.fittedvalues, ts


# ─── Statistical Summary ─────────────────────────────────────────────────────
def compute_revenue_stats(df: pd.DataFrame) -> dict:
    """
    Compute detailed descriptive statistics and distribution fit metrics.

    Returns a dict with:
      mean, median, std, skewness, kurtosis, iqr,
      normality_p (Shapiro-Wilk p-value),
      lognormal_fit (True if log-normal fits better than normal)
    """
    vals = df["amount"].dropna()
    if len(vals) < 5:
        return {}

    mean     = float(vals.mean())
    median   = float(vals.median())
    std      = float(vals.std())
    skewness = float(scipy_stats.skew(vals))
    kurt     = float(scipy_stats.kurtosis(vals))
    p25, p75 = np.percentile(vals, [25, 75])
    iqr      = float(p75 - p25)

    # Shapiro-Wilk normality test (subsample if large)
    sample = vals.sample(min(500, len(vals)), random_state=42)
    try:
        _, norm_p = scipy_stats.shapiro(sample)
    except Exception:
        norm_p = None

    # Compare AIC: normal vs log-normal
    try:
        mu_n, sigma_n = scipy_stats.norm.fit(vals)
        ll_norm       = scipy_stats.norm.logpdf(vals, mu_n, sigma_n).sum()
        s, loc, scale = scipy_stats.lognorm.fit(vals, floc=0)
        ll_logn       = scipy_stats.lognorm.logpdf(vals, s, loc=loc, scale=scale).sum()
        lognormal_better = ll_logn > ll_norm
    except Exception:
        lognormal_better = None

    return dict(
        mean=mean, median=median, std=std,
        skewness=skewness, kurtosis=kurt, iqr=iqr,
        p25=p25, p75=p75,
        normality_p=norm_p,
        lognormal_fit=lognormal_better,
        n=len(vals),
    )