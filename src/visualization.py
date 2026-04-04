"""
visualization.py
----------------
All Plotly chart-building functions.
Each function is pure: takes a DataFrame (+ optional kwargs), returns a go.Figure.
No Streamlit calls — charts are rendered in app.py via st.plotly_chart().

Original charts  (1-10):  Core dashboard visuals
Advanced charts  (11-15): Statistical analysis, ML, forecasting
"""

from __future__ import annotations

import streamlit as st
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats

from src.utils import CHART_COLORS, PLOTLY_LAYOUT, fmt_currency

warnings.filterwarnings("ignore")


# ─── Shared helpers ───────────────────────────────────────────────────────────
def _apply_layout(fig: go.Figure, title: str = "", **kwargs) -> go.Figure:
    """Apply shared dark layout + optional overrides to any figure."""
    layout = {**PLOTLY_LAYOUT, **kwargs}
    if title:
        layout["title"] = dict(text=title, font_size=15, x=0.02, xanchor="left")
    fig.update_layout(**layout)
    return fig


def _axis_style() -> dict:
    """Return common axis styling dict."""
    return dict(
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(size=11),
        title_font=dict(size=12),
    )


# ─────────────────────────────────────────────────────────────────────────────
#  1. Sales over time (area + MA)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def sales_over_time(df: pd.DataFrame, freq: str = "M") -> go.Figure:
    """Area line chart: aggregated revenue over time with 3-period moving average."""
    ts = (
        df.set_index("date")["amount"]
        .resample(freq)
        .sum()
        .reset_index()
    )
    ts.columns = ["date", "revenue"]
    ma = ts["revenue"].rolling(3, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts["date"], y=ts["revenue"],
        fill="tozeroy",
        fillcolor="rgba(108,52,131,0.18)",
        line=dict(color=CHART_COLORS[0], width=2.5),
        name="Revenue",
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=ts["date"], y=ma,
        line=dict(color="#F39C12", width=1.8, dash="dot"),
        name="3-period MA",
        hovertemplate="MA: $%{y:,.0f}<extra></extra>",
    ))
    if not ts.empty:
        peak = ts.loc[ts["revenue"].idxmax()]
        fig.add_annotation(
            x=peak["date"], y=peak["revenue"],
            text=f"Peak: {fmt_currency(peak['revenue'])}",
            showarrow=True, arrowhead=2, arrowcolor="#F39C12",
            font=dict(color="#F39C12", size=11),
            bgcolor="rgba(0,0,0,0.4)", borderpad=4,
        )

    fig = _apply_layout(fig, "Revenue Over Time")
    fig.update_xaxes(**_axis_style(), title="")
    fig.update_yaxes(**_axis_style(), title="Revenue (USD)", tickprefix="$", tickformat=",")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  2. Cumulative revenue (step area)
# ─────────────────────────────────────────────────────────────────────────────
def cumulative_revenue(df: pd.DataFrame) -> go.Figure:
    """Step-area chart of cumulative revenue over time."""
    ts = (
        df.sort_values("date")
        .set_index("date")["amount"]
        .resample("W").sum()
        .cumsum()
        .reset_index()
    )
    ts.columns = ["date", "cumulative"]

    fig = go.Figure(go.Scatter(
        x=ts["date"], y=ts["cumulative"],
        fill="tozeroy",
        fillcolor="rgba(30,132,73,0.15)",
        line=dict(color="#2ECC71", width=2.5),
        mode="lines",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Cumulative: $%{y:,.0f}<extra></extra>",
        name="Cumulative Revenue",
    ))

    fig = _apply_layout(fig, "Cumulative Revenue Growth", height=300)
    fig.update_xaxes(**_axis_style(), title="")
    fig.update_yaxes(**_axis_style(), title="Cumulative Revenue", tickprefix="$", tickformat=",")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  3. Revenue by country (bar chart)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def revenue_by_country(df: pd.DataFrame) -> go.Figure:
    """Sorted vertical bar chart of total revenue per country."""
    grp = (
        df.groupby("country")
        .agg(revenue=("amount", "sum"), orders=("amount", "count"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    fig = go.Figure(go.Bar(
        x=grp["country"], y=grp["revenue"],
        marker=dict(
            color=grp["revenue"],
            colorscale=[[0, "#4A235A"], [0.5, "#8E44AD"], [1, "#D7BDE2"]],
            line=dict(width=0),
        ),
        text=[fmt_currency(v) for v in grp["revenue"]],
        textposition="outside",
        textfont=dict(size=11),
        customdata=grp["orders"],
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<br>Orders: %{customdata:,}<extra></extra>",
    ))
    top_country = grp.iloc[0]

    fig.add_annotation(
        x=top_country["country"],
        y=top_country["revenue"],
        text="🏆 Top Country",
        showarrow=True,
        arrowhead=2
    )
    fig = _apply_layout(fig, "Revenue by Country")
    fig.update_xaxes(**_axis_style())
    fig.update_yaxes(**_axis_style(), title="Revenue (USD)", tickprefix="$", tickformat=",")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  4. Category revenue breakdown (donut)
# ─────────────────────────────────────────────────────────────────────────────
def category_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart: revenue split by product_category."""
    grp = df.groupby("product_category")["amount"].sum().reset_index()
    grp.columns = ["category", "revenue"]

    fig = go.Figure(go.Pie(
        labels=grp["category"], values=grp["revenue"],
        hole=0.55,
        marker=dict(colors=CHART_COLORS, line=dict(color="#1C1C2E", width=2)),
        textinfo="label+percent",
        textfont=dict(size=12),
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{percent}<extra></extra>",
    ))
    fig.add_annotation(
        text="Category<br>Revenue", x=0.5, y=0.5,
        font=dict(size=13, color="rgba(255,255,255,0.6)"), showarrow=False,
    )
    fig = _apply_layout(fig, "Revenue by Category",
                        height=340, showlegend=True,
                        legend=dict(orientation="v", x=1, y=0.5,
                                    font_size=11, bgcolor="rgba(0,0,0,0)"))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  5. Top products (horizontal bar)
# ─────────────────────────────────────────────────────────────────────────────
def top_products(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart of top-N products by revenue."""
    grp = (
        df.groupby("product")["amount"].sum()
        .sort_values(ascending=True).tail(top_n).reset_index()
    )
    fig = go.Figure(go.Bar(
        y=grp["product"], x=grp["amount"],
        orientation="h",
        marker=dict(
            color=grp["amount"],
            colorscale=[[0, "#922B21"], [0.5, "#E74C3C"], [1, "#FADBD8"]],
            line=dict(width=0),
        ),
        text=[fmt_currency(v) for v in grp["amount"]],
        textposition="inside",
        textfont=dict(size=11, color="white"),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
    ))
    fig = _apply_layout(fig, f"Top {top_n} Products by Revenue",
                        height=420, margin=dict(l=160, r=40, t=50, b=30))
    fig.update_xaxes(**_axis_style(), title="Revenue (USD)", tickprefix="$", tickformat=",")
    fig.update_yaxes(**_axis_style(), title="")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  6. Revenue per box (efficiency chart)
# ─────────────────────────────────────────────────────────────────────────────
def revenue_per_box_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart showing revenue per box for each product."""
    grp = (
        df.groupby("product")
        .agg(revenue=("amount", "sum"), boxes=("boxes_shipped", "sum"))
        .assign(rev_per_box=lambda x: x["revenue"] / x["boxes"].replace(0, np.nan))
        .dropna()
        .sort_values("rev_per_box", ascending=True)
        .reset_index()
    )
    fig = go.Figure(go.Bar(
        y=grp["product"], x=grp["rev_per_box"],
        orientation="h",
        marker=dict(
            color=grp["rev_per_box"],
            colorscale=[[0, "#117A65"], [0.5, "#1ABC9C"], [1, "#A9DFBF"]],
            line=dict(width=0),
        ),
        text=[f"${v:.2f}" for v in grp["rev_per_box"]],
        textposition="inside",
        textfont=dict(size=10, color="white"),
        hovertemplate="<b>%{y}</b><br>Rev/Box: $%{x:.2f}<extra></extra>",
    ))
    fig = _apply_layout(fig, "Revenue per Box (Efficiency)",
                        height=400, margin=dict(l=160, r=40, t=50, b=30))
    fig.update_xaxes(**_axis_style(), title="Revenue per Box (USD)", tickprefix="$")
    fig.update_yaxes(**_axis_style(), title="")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  7. Monthly trend YoY (grouped bar)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def monthly_trend(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart showing month-by-month revenue, colour-coded by year."""
    MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    grp = df.groupby(["year", "month_name"])["amount"].sum().reset_index()
    grp["month_name"] = pd.Categorical(grp["month_name"], categories=MONTH_ORDER, ordered=True)
    grp = grp.sort_values(["year", "month_name"])
    years = sorted(grp["year"].unique())
    colors = ["#9B59B6", "#F39C12", "#2ECC71", "#3498DB"]

    fig = go.Figure()
    for i, yr in enumerate(years):
        sub = grp[grp["year"] == yr]
        fig.add_trace(go.Bar(
            x=sub["month_name"], y=sub["amount"],
            name=str(yr),
            marker_color=colors[i % len(colors)],
            hovertemplate=f"<b>{yr} — %{{x}}</b><br>Revenue: $%{{y:,.0f}}<extra></extra>",
        ))
    fig = _apply_layout(fig, "Monthly Revenue Trend (YoY)", barmode="group")
    fig.update_xaxes(**_axis_style(), title="Month", categoryorder="array",
                     categoryarray=MONTH_ORDER)
    fig.update_yaxes(**_axis_style(), title="Revenue (USD)", tickprefix="$", tickformat=",")
    peak = grp.loc[grp["amount"].idxmax()]

    fig.add_annotation(
        x=peak["month_name"],
        y=peak["amount"],
        text="📈 Peak Month",
        showarrow=True
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  8. Boxes shipped distribution (histogram + KDE)
# ─────────────────────────────────────────────────────────────────────────────
def boxes_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram + smoothed KDE overlay for Boxes Shipped distribution."""
    vals = df["boxes_shipped"].dropna()
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=vals, nbinsx=40,
        marker_color="rgba(108,52,131,0.65)",
        marker_line=dict(color=CHART_COLORS[0], width=0.8),
        name="Frequency",
        hovertemplate="Boxes: %{x}<br>Count: %{y}<extra></extra>",
    ))
    hist_vals, bin_edges = np.histogram(vals, bins=40, density=True)
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    try:
        from scipy.signal import savgol_filter
        kde_smooth = savgol_filter(hist_vals, window_length=7, polyorder=3)
    except Exception:
        kde_smooth = hist_vals
    scale = len(vals) * (bin_edges[1] - bin_edges[0])
    fig.add_trace(go.Scatter(
        x=bin_centres, y=kde_smooth * scale,
        mode="lines", line=dict(color="#F39C12", width=2),
        name="Distribution curve",
    ))
    fig = _apply_layout(fig, "Boxes Shipped Distribution", height=320)
    fig.update_xaxes(**_axis_style(), title="Boxes Shipped")
    fig.update_yaxes(**_axis_style(), title="Frequency")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  9. Country × Product heatmap
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def heatmap_product_country(df: pd.DataFrame) -> go.Figure:
    """Heatmap of revenue: rows = countries, columns = top-12 products."""
    pivot = df.pivot_table(
        index="country", columns="product",
        values="amount", aggfunc="sum", fill_value=0
    )
    top_prod_list = df.groupby("product")["amount"].sum().nlargest(12).index.tolist()
    pivot = pivot[[c for c in pivot.columns if c in top_prod_list]]

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, "#1C0533"], [0.3, "#6C3483"], [0.7, "#C39BD3"], [1, "#F9EBFF"]],
        hovertemplate="<b>%{y} × %{x}</b><br>Revenue: $%{z:,.0f}<extra></extra>",
        colorbar=dict(title="Revenue", tickprefix="$", tickformat=",", tickfont=dict(size=10)),
    ))
    fig = _apply_layout(fig, "Revenue Heatmap: Country × Product",
                        height=340, margin=dict(l=100, r=40, t=50, b=120))
    fig.update_xaxes(tickangle=-40, tickfont=dict(size=10))
    fig.update_yaxes(tickfont=dict(size=11))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  10. Salesperson performance (bubble chart)
# ─────────────────────────────────────────────────────────────────────────────
def salesperson_performance(df: pd.DataFrame) -> go.Figure:
    """Bubble chart: x = orders, y = revenue, size = avg order value."""
    grp = (
        df.groupby("salesperson")
        .agg(revenue=("amount", "sum"), orders=("amount", "count"),
             avg_order=("amount", "mean"), total_boxes=("boxes_shipped", "sum"))
        .reset_index()
    )
    fig = go.Figure(go.Scatter(
        x=grp["orders"], y=grp["revenue"],
        mode="markers+text",
        marker=dict(
            size=grp["avg_order"] / grp["avg_order"].max() * 50 + 8,
            color=grp["revenue"],
            colorscale="Purples",
            showscale=True,
            colorbar=dict(title="Revenue", tickprefix="$", tickformat=",", tickfont_size=10),
            line=dict(width=1.2, color="rgba(255,255,255,0.3)"),
            opacity=0.85,
        ),
        text=grp["salesperson"].str.split().str[0],
        textposition="top center",
        textfont=dict(size=10, color="rgba(255,255,255,0.7)"),
        customdata=grp[["avg_order", "total_boxes", "salesperson"]].values,
        hovertemplate=(
            "<b>%{customdata[2]}</b><br>"
            "Revenue: $%{y:,.0f}<br>Orders: %{x:,}<br>"
            "Avg Order: $%{customdata[0]:,.0f}<br>Boxes: %{customdata[1]:,}<extra></extra>"
        ),
    ))
    fig = _apply_layout(fig, "Salesperson Performance (bubble = avg order size)", height=440)
    fig.update_xaxes(**_axis_style(), title="Number of Orders")
    fig.update_yaxes(**_axis_style(), title="Total Revenue (USD)", tickprefix="$", tickformat=",")
    return fig


# ═════════════════════════════════════════════════════════════════════════════
#  ADVANCED ANALYTICS CHARTS  (11-15)
# ═════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
#  11. Box Plots — Revenue distribution analysis
# ─────────────────────────────────────────────────────────────────────────────
def boxplot_revenue_analysis(df: pd.DataFrame, group_by: str = "country") -> go.Figure:
    """
    Box-and-whisker plots showing revenue distribution per group.

    Parameters
    ----------
    df       : Filtered DataFrame
    group_by : One of 'country', 'salesperson', 'product_category', 'product'
    """
    label_map = {
        "country":          "Country",
        "salesperson":      "Salesperson",
        "product_category": "Product Category",
        "product":          "Product",
    }
    label = label_map.get(group_by, group_by)

    # Sort groups by median for easier reading
    order = (
        df.groupby(group_by)["amount"]
        .median()
        .sort_values(ascending=True)
        .index.tolist()
    )

    # Assign a distinct colour per group
    palette = CHART_COLORS * 5
    color_map = {grp: palette[i] for i, grp in enumerate(order)}

    def _hex_to_rgba(hex_color: str, alpha: float = 0.25) -> str:
        """Convert '#RRGGBB' to 'rgba(r,g,b,alpha)'."""
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    fig = go.Figure()
    for grp in order:
        sub = df[df[group_by] == grp]["amount"]
        fig.add_trace(go.Box(
            y=sub,
            name=grp,
            boxpoints="outliers",          # show outlier dots
            marker=dict(
                color=color_map[grp],
                opacity=0.7,
                size=4,
                line=dict(width=0.8, color="rgba(255,255,255,0.4)"),
            ),
            line=dict(color=color_map[grp], width=1.8),
            fillcolor=_hex_to_rgba(color_map[grp], 0.26),
            hovertemplate=(
                f"<b>{grp}</b><br>"
                "Value: $%{y:,.0f}<extra></extra>"
            ),
        ))

    fig = _apply_layout(
        fig,
        f"Revenue Distribution by {label}",
        height=460,
        boxmode="group",
    )
    fig.update_xaxes(**_axis_style(), title=label, tickangle=-20)
    fig.update_yaxes(**_axis_style(), title="Order Revenue (USD)", tickprefix="$", tickformat=",")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  12. Linear Regression Forecast
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
#  12. ARIMA Forecast Chart
# ─────────────────────────────────────────────────────────────────────────────
def revenue_forecast_arima(
    ts_history,
    forecast_df: pd.DataFrame,
    fitted_vals,
    best_order: tuple,
    best_aic: float,
) -> go.Figure:
    """
    Historical bars + in-sample green fit + amber forecast + 95% CI band.
    All inputs come from utils.run_arima_forecast().
    """
    fig = go.Figure()

    # 95% CI shaded band
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_df["date"], forecast_df["date"][::-1]]),
        y=pd.concat([forecast_df["ci_upper"], forecast_df["ci_lower"][::-1]]),
        fill="toself", fillcolor="rgba(243,156,18,0.13)",
        line=dict(width=0), name="95% Confidence Interval", hoverinfo="skip",
    ))

    # Forecast line + markers
    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["predicted"],
        mode="lines+markers",
        line=dict(color="#F39C12", width=2.5, dash="dot"),
        marker=dict(size=8, color="#F39C12",
                    line=dict(width=1.5, color="rgba(255,255,255,0.4)")),
        name=f"ARIMA{best_order} Forecast",
        hovertemplate="<b>Forecast %{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>",
    ))

    # Historical actuals (bars)
    fig.add_trace(go.Bar(
        x=ts_history.index, y=ts_history.values,
        marker_color="rgba(155,89,182,0.50)",
        marker_line=dict(color=CHART_COLORS[0], width=0.7),
        name="Actual Revenue",
        hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>",
    ))

    # In-sample ARIMA fitted values
    fig.add_trace(go.Scatter(
        x=fitted_vals.index, y=fitted_vals.values,
        mode="lines", line=dict(color="#2ECC71", width=2),
        name="ARIMA In-Sample Fit",
        hovertemplate="Fitted: $%{y:,.0f}<extra></extra>",
    ))

    # Separator at forecast start
    if not forecast_df.empty:
        fig.add_vline(
            x=forecast_df["date"].iloc[0].timestamp() * 1000,
            line_dash="dash", line_color="rgba(128,128,128,0.35)",
            annotation_text="  Forecast →",
            annotation_font=dict(color="rgba(128,128,128,0.7)", size=11),
        )

    p, d, q = best_order
    fig = _apply_layout(
        fig,
        f"ARIMA({p},{d},{q}) Revenue Forecast  "
        f"<span style='font-size:11px;color:#95A5A6'>AIC = {best_aic:.1f}</span>",
        height=460, barmode="overlay",
    )
    fig.update_xaxes(**_axis_style(), title="")
    fig.update_yaxes(**_axis_style(), title="Revenue (USD)", tickprefix="$", tickformat=",")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  13. K-Means salesperson clustering
# ─────────────────────────────────────────────────────────────────────────────
CLUSTER_COLORS = {
    "High Performer":    "#2ECC71",
    "Solid Contributor": "#F39C12",
    "Growth Potential":  "#9B59B6",
}


def salesperson_cluster_chart(cluster_df: pd.DataFrame) -> go.Figure:
    """Scatter: x=orders, y=revenue, size=avg order, colour=cluster label."""
    fig = go.Figure()
    for label, sub in cluster_df.groupby("cluster_label"):
        color = CLUSTER_COLORS.get(label, "#3498DB")
        fig.add_trace(go.Scatter(
            x=sub["orders"], y=sub["revenue"],
            mode="markers+text", name=label,
            marker=dict(
                size=sub["avg_order"] / sub["avg_order"].max() * 46 + 12,
                color=color, opacity=0.82,
                line=dict(width=1.4, color="rgba(255,255,255,0.25)"),
            ),
            text=sub["salesperson"].str.split().str[0],
            textposition="top center",
            textfont=dict(size=10, color="rgba(128,128,128,0.8)"),
            customdata=sub[["avg_order", "revenue_per_box", "salesperson"]].values,
            hovertemplate=(
                "<b>%{customdata[2]}</b><br>"
                "Cluster: " + label + "<br>"
                "Revenue: $%{y:,.0f}<br>Orders: %{x:,}<br>"
                "Avg Order: $%{customdata[0]:,.0f}<br>"
                "Rev/Box: $%{customdata[1]:.2f}<extra></extra>"
            ),
        ))
    fig = _apply_layout(
        fig,
        "Salesperson Segmentation — K-Means Clustering  "
        "<span style='font-size:11px;color:#95A5A6'>bubble size = avg order value</span>",
        height=480,
    )
    fig.update_xaxes(**_axis_style(), title="Number of Orders")
    fig.update_yaxes(**_axis_style(), title="Total Revenue (USD)", tickprefix="$", tickformat=",")
    return fig


def cluster_radar_chart(cluster_df: pd.DataFrame) -> go.Figure:
    """Radar chart of normalised cluster centroid profiles."""
    features    = ["revenue", "orders", "avg_order", "revenue_per_box"]
    feat_labels = ["Revenue", "Orders", "Avg Order", "Rev/Box"]
    centroids   = cluster_df.groupby("cluster_label")[features].mean()
    normed      = (centroids - centroids.min()) / (centroids.max() - centroids.min() + 1e-9)

    def _h2r(h: str, a: float = 0.16) -> str:
        h = h.lstrip("#")
        r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16)
        return f"rgba({r},{g},{b},{a})"

    from src.utils import _DARK
    grid_c = "rgba(255,255,255,0.08)" if _DARK else "rgba(0,0,0,0.08)"
    tick_c = "#C8BAE0" if _DARK else "#3A2A5A"

    fig = go.Figure()
    for label, row in normed.iterrows():
        vals = row.tolist() + [row.tolist()[0]]
        c    = CLUSTER_COLORS.get(label, "#3498DB")
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=feat_labels + [feat_labels[0]],
            fill="toself", name=label,
            line=dict(color=c, width=2), fillcolor=_h2r(c, 0.16),
        ))

    layout_kw = {k: v for k, v in PLOTLY_LAYOUT.items() if k != "margin"}
    fig.update_layout(
        **layout_kw, height=380,
        title=dict(text="Cluster Profile Radar", font_size=15, x=0.02, xanchor="left"),
        margin=dict(l=20, r=20, t=50, b=30),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor=grid_c,
                            tickfont=dict(size=9, color=tick_c)),
            angularaxis=dict(gridcolor=grid_c, tickfont=dict(size=11, color=tick_c)),
        ),
    )
    return fig

def correlation_heatmap(df):
    import plotly.express as px

    corr = df[["amount", "boxes_shipped", "revenue_per_box"]].corr()

    fig = px.imshow(corr, text_auto=True, color_continuous_scale="Purples")
    return _apply_layout(fig, "Feature Correlation Heatmap")