"""
app.py
======
Chocolate Sales Analytics Dashboard — Main Entry Point
Author : [Anvita Choudhary]
Dataset: Kaggle – Chocolate Sales Dataset 2023–2024
"""
import streamlit as st

import pandas as pd
import re

from src.data_loader   import get_data
from src.preprocessing import apply_filters
from src.visualization import (
    # Core charts
    sales_over_time, cumulative_revenue,
    revenue_by_country, category_donut,
    top_products, revenue_per_box_chart,
    monthly_trend, boxes_distribution,
    heatmap_product_country, salesperson_performance,
    # Advanced charts
    boxplot_revenue_analysis,
    revenue_forecast_arima,
    salesperson_cluster_chart, cluster_radar_chart,
)
from src.utils import (
    fmt_currency, fmt_number,
    generate_insights, get_download_bytes, compute_kpis,
    run_kmeans_clustering, run_arima_forecast,
    configure_theme,
)


# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title            = "Chocolate Sales Dashboard",
    layout                = "wide",
    initial_sidebar_state = "expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────
def inject_css(dark_mode: bool):
    bg       = "#0F0F1A" if dark_mode else "#F5F0FF"
    bg2      = "#1A1A2E" if dark_mode else "#FFFFFF"
    text     = "#F0E6FF" if dark_mode else "#1A0A2E"
    text_sub = "#9B8FBF" if dark_mode else "#3F315C"
    border   = "rgba(255,255,255,0.08)" if dark_mode else "rgba(108,52,131,0.18)"
    kpi_bg   = "#1E1E35" if dark_mode else "#FFFFFF"
    sidebar  = "#13132A" if dark_mode else "#EDE8F8"
    tag_text = "#C39BD3" if dark_mode else "#5B2D8E"
    tag_bg   = "rgba(108,52,131,0.18)" if dark_mode else "rgba(108,52,131,0.12)"
    pill_bg  = "rgba(108,52,131,0.18)" if dark_mode else "rgba(108,52,131,0.08)"
    pill_bd  = "rgba(155,89,182,0.30)" if dark_mode else "rgba(108,52,131,0.25)"
    adv_hdr  = "rgba(108,52,131,0.22)" if dark_mode else "rgba(108,52,131,0.10)"
    muted_inline = "#6B5B8B" if dark_mode else text_sub

    # Scoped Streamlit native overrides for light mode.
    native_text = "" if dark_mode else f"""
    :root, .stApp {{
        --text-color: {text};
        --secondary-text-color: {text_sub};
        --background-color: {bg};
        --secondary-background-color: {bg2};
    }}
    .stApp,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] :where(p, li, h1, h2, h3, h4, h5, h6, strong),
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stCaptionContainer"],
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {{
        color: {text} !important;
    }}
    button[data-baseweb="tab"] {{ color: {text_sub} !important; }}
    button[data-baseweb="tab"][aria-selected="true"] {{ color: {text} !important; }}
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stRadio label, .stDateInput label, .stToggle label {{
        color: {text} !important;
    }}
    .stSlider [data-testid="stTickBar"] *,
    .stSlider [data-testid="stThumbValue"],
    [data-baseweb="input"] *,
    [data-baseweb="select"] *,
    [data-baseweb="popover"] *,
    [data-baseweb="menu"] *,
    [role="listbox"] *,
    [role="option"] *,
    input,
    textarea {{
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
    }}
    [data-baseweb="input"] input,
    [data-baseweb="input"] div {{
        color: {text} !important;
        background-color: {bg2} !important;
        border-color: {border} !important;
    }}
    [data-baseweb="select"] > div,
    [data-baseweb="input"] {{
        background-color: {bg2} !important;
        border-color: {border} !important;
        box-shadow: none !important;
    }}
    [data-baseweb="select"] div,
    [data-baseweb="select"] input {{
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
    }}
    [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [class*="value"],
    [data-baseweb="select"] [class*="Value"],
    [data-baseweb="select"] [class*="placeholder"],
    [data-baseweb="select"] [class*="Placeholder"] {{
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
        opacity: 1 !important;
    }}
    [data-baseweb="select"] input::placeholder,
    [data-baseweb="input"] input::placeholder,
    [data-baseweb="select"] [aria-disabled="true"],
    [data-baseweb="select"] [aria-disabled="true"] *,
    [data-baseweb="select"] div[disabled],
    [data-baseweb="select"] div[disabled] * {{
        color: {text_sub} !important;
        -webkit-text-fill-color: {text_sub} !important;
        opacity: 1 !important;
    }}
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"] {{
        background-color: {bg2} !important;
        border: 1px solid {border} !important;
    }}
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li *,
    [data-baseweb="menu"] div,
    [data-baseweb="menu"] div *,
    [role="option"],
    [role="option"] * {{
        background-color: {bg2} !important;
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
    }}
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] li:hover *,
    [role="option"]:hover,
    [role="option"]:hover *,
    [aria-selected="true"],
    [aria-selected="true"] * {{
        background-color: rgba(108,52,131,0.12) !important;
        color: {text} !important;
    }}
    [data-baseweb="tag"] {{
        background-color: rgba(108,52,131,0.14) !important;
        border: 1px solid rgba(108,52,131,0.28) !important;
    }}
    [data-baseweb="tag"] *,
    [data-baseweb="tag"] span {{
        color: {text} !important;
    }}
    [data-baseweb="calendar"] *,
    [data-baseweb="calendar"] button {{
        color: {text} !important;
    }}
    [data-testid="stDataFrame"] {{ color: {text}; }}
    [data-testid="stMetricValue"] {{ color: {text} !important; }}
    .stAlert p {{ color: {text} !important; }}
    [data-baseweb="select"] span {{ color: {text} !important; }}
    .stPlotlyChart svg text {{
        fill: {text} !important;
    }}
    .stPlotlyChart {{
        background: {bg2};
        border: 1px solid rgba(108,52,131,0.22);
        border-radius: 10px;
        padding: 0.35rem;
    }}
    .st-key-box_group [data-baseweb="select"],
    .st-key-box_group [data-baseweb="select"] *,
    .st-key-box_group [data-baseweb="select"] input,
    .st-key-box_group [data-baseweb="select"] input::placeholder {{
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
        opacity: 1 !important;
    }}
    """

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body {{
        font-family: 'Inter', sans-serif;
        font-size: 14px;
    }}
    .stApp {{ background-color: {bg} !important; color: {text} !important; }}
    section[data-testid="stSidebar"] {{
        background-color: {sidebar} !important;
        border-right: 1px solid {border};
    }}
    section[data-testid="stSidebar"] * {{ color: {text_sub}; }}
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] strong {{ color: {text} !important; }}

    /* KPI cards */
    .kpi-card {{
        background: {kpi_bg};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 1.2rem 1.4rem 1rem;
        margin-bottom: 0.3rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .kpi-card:hover {{
        border-color: #9B59B6;
        box-shadow: 0 4px 24px rgba(108,52,131,0.18);
    }}
    .kpi-label {{
        font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em;
        text-transform: uppercase; color: {text_sub};
        font-family: 'DM Mono', monospace; margin-bottom: 0.35rem;
    }}
    .kpi-value {{
        font-size: 1.75rem; font-weight: 700; color: {text};
        letter-spacing: -0.02em; line-height: 1;
    }}
    .kpi-sub  {{ font-size: 0.78rem; color: {text_sub}; margin-top: 0.25rem; }}
    .kpi-positive {{ color: #27AE60; }}
    .kpi-negative {{ color: #E74C3C; }}

    /* Section labels */
    .section-tag {{
        display: inline-block; background: {tag_bg};
        color: {tag_text}; border-radius: 20px; padding: 2px 12px;
        font-size: 0.68rem; font-weight: 600; letter-spacing: 0.1em;
        text-transform: uppercase; font-family: 'DM Mono', monospace;
        margin-bottom: 4px;
    }}
    .section-title {{ font-size: 1.1rem; font-weight: 600; color: {text}; margin: 2px 0; }}
    .section-desc  {{ font-size: 0.8rem; color: {text_sub}; margin-bottom: 0.75rem; }}
    .custom-divider {{ border: none; border-top: 1px solid {border}; margin: 1.6rem 0; }}

    /* Insight cards */
    .insight-card {{
        background: {kpi_bg}; border: 1px solid {border};
        border-left: 4px solid #9B59B6;
        border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.75rem;
    }}
    .insight-title {{ font-weight: 600; color: {text}; font-size: 0.88rem; }}
    .insight-body  {{ font-size: 0.82rem; color: {text_sub}; margin-top: 0.25rem; line-height: 1.5; }}

    /* Hero — always dark-gradient regardless of theme */
    .hero {{
        background: linear-gradient(135deg, #1A0533 0%, #2D0A4E 50%, #1A0533 100%);
        border: 1px solid rgba(155,89,182,0.3); border-radius: 18px;
        padding: 1.8rem 2.4rem; margin-bottom: 1.4rem;
        position: relative; overflow: hidden;
    }}
    .hero::after {{
        content: ""; position: absolute; right: 2rem; top: 50%;
        transform: translateY(-50%); font-size: 5rem; opacity: 0.15;
    }}
    .hero-eyebrow {{
        font-size: 0.68rem; letter-spacing: 0.14em; text-transform: uppercase;
        color: #C39BD3; font-family: 'DM Mono', monospace; margin-bottom: 0.4rem;
    }}
    .hero-title {{ font-size: 2rem; font-weight: 700; color: #FFFFFF; margin: 0 0 0.4rem; letter-spacing: -0.02em; }}
    .hero-sub   {{ font-size: 0.9rem; color: rgba(255,255,255,0.82); max-width: 680px; }}
    .hero, .hero .hero-title {{ color: #FFFFFF !important; }}
    .hero-eyebrow {{ color: #C39BD3 !important; }}
    .hero-sub, .hero-sub strong {{ color: rgba(255,255,255,0.82) !important; }}

    /* Download button */
    .stDownloadButton button {{
        background: linear-gradient(135deg, #6C3483, #9B59B6) !important;
        color: white !important; border: none !important; border-radius: 8px !important;
        font-weight: 600 !important; padding: 0.45rem 1.2rem !important;
    }}
    .stDownloadButton button * {{ color: white !important; }}

    /* DataFrame */
    .stDataFrame {{ border: 1px solid {border}; border-radius: 10px; overflow: hidden; }}

    /* Stat pills (box plots tab) */
    .stat-pill {{
        display: inline-block; background: {pill_bg};
        border: 1px solid {pill_bd}; border-radius: 8px;
        padding: 0.55rem 0.9rem; margin: 0.2rem;
        font-family: 'DM Mono', monospace; font-size: 0.8rem; color: {text};
    }}
    .stat-pill-label {{ color: {text_sub}; font-size: 0.68rem; display: block; }}

    /* Cluster badges */
    .cluster-badge {{
        display: inline-block; border-radius: 20px; padding: 3px 10px;
        font-size: 0.72rem; font-weight: 600; margin-right: 6px;
    }}

    /* Advanced section header bar */
    .adv-section-header {{
        background: linear-gradient(90deg, {adv_hdr} 0%, transparent 100%);
        border-left: 3px solid #9B59B6; border-radius: 0 8px 8px 0;
        padding: 0.6rem 1rem; margin: 1rem 0 0.5rem; color: {text};
    }}
    .muted-inline {{
        color: {muted_inline}; font-family: 'DM Mono', monospace;
    }}

    {native_text}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  HELPER COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────
def section_header(tag: str, title: str, desc: str = ""):
    st.markdown(
        f'<div class="section-tag">{tag}</div>'
        f'<div class="section-title">{title}</div>'
        + (f'<div class="section-desc">{desc}</div>' if desc else ""),
        unsafe_allow_html=True,
    )


def adv_section_header(title: str):
    st.markdown(
        f'<div class="adv-section-header"><strong>{title}</strong></div>',
        unsafe_allow_html=True,
    )


def divider():
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", delta: float | None = None):
    delta_html = ""
    if delta is not None:
        arrow = "▲" if delta >= 0 else "▼"
        cls   = "kpi-positive" if delta >= 0 else "kpi-negative"
        delta_html = f'<div class="kpi-sub {cls}">{arrow} {fmt_currency(abs(delta))} vs prev period</div>'
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{delta_html or (f"<div class=kpi-sub>{sub}</div>" if sub else "")}'
        f'</div>',
        unsafe_allow_html=True,
    )


def insight_cards(insights: list[dict]):
    for ins in insights:
        body = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", ins["body"])
        st.markdown(
            f'<div class="insight-card">'
            f'<span class="insight-title">{ins["title"]}</span>'
            f'<div class="insight-body">{body}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def stat_pill(label: str, value: str):
    return (
        f'<div class="stat-pill">'
        f'<span class="stat-pill-label">{label}</span>'
        f'{value}'
        f'</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Chocolate Dashboard")
    st.markdown("---")

    dark_mode = st.toggle("Dark Mode", value=True)
    configure_theme(dark_mode)
    inject_css(dark_mode)

    st.markdown("### Filters")

    df_master = get_data()

    min_date = df_master["date"].min().date()
    max_date = df_master["date"].max().date()

    d_start, d_end = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    _countries = st.multiselect(
        "Country",
        options=sorted(df_master["country"].unique()),
        default=sorted(df_master["country"].unique()),
    )
    _products = st.multiselect(
        "Product",
        options=sorted(df_master["product"].unique()),
        default=sorted(df_master["product"].unique()),
    )
    _sp = st.multiselect(
        "Salesperson",
        options=sorted(df_master["salesperson"].unique()),
        default=sorted(df_master["salesperson"].unique()),
    )

    st.markdown("---")
    st.markdown("### Chart Options")
    chart_freq = st.radio(
        "Time Granularity",
        options=["W", "ME", "QE"],
        format_func=lambda x: {"W": "Weekly", "ME": "Monthly", "QE": "Quarterly"}[x],
        horizontal=True,
        index=1,
    )
    top_n = st.slider("Top-N Products", min_value=5, max_value=20, value=10)

    st.markdown("---")
    st.markdown("### Advanced Analytics")
    box_group = st.selectbox(
        "Box Plot Group By",
        options=["country", "salesperson", "product_category", "product"],
        format_func=lambda x: x.replace("_", " ").title(),
        placeholder="Select group",
        label_visibility="visible",
        key="box_group",
    )
    n_clusters = st.slider("K-Means Clusters", min_value=2, max_value=5, value=3)
    forecast_months = st.slider("Forecast Horizon (months)", min_value=1, max_value=6, value=3)

    st.markdown("---")
    st.markdown(
        "<div class='muted-inline' style='font-size:0.72rem'>"
        "Dataset: Kaggle – ssssws<br>chocolate-sales-dataset-2023-2024"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  FILTER DATA
# ─────────────────────────────────────────────────────────────────────────────
df = apply_filters(
    df_master,
    date_range   = (d_start, d_end),
    countries    = _countries or df_master["country"].unique().tolist(),
    products     = _products  or df_master["product"].unique().tolist(),
    salespersons = _sp        or df_master["salesperson"].unique().tolist(),
)

# Previous period (same length) for KPI deltas
period_len = max((pd.Timestamp(d_end) - pd.Timestamp(d_start)).days, 1)
prev_start = pd.Timestamp(d_start) - pd.Timedelta(days=period_len)
df_prev    = apply_filters(
    df_master,
    date_range   = (prev_start.date(), d_start),
    countries    = _countries or df_master["country"].unique().tolist(),
    products     = _products  or df_master["product"].unique().tolist(),
    salespersons = _sp        or df_master["salesperson"].unique().tolist(),
)

if df.empty:
    st.warning("No data matches your current filters. Please adjust the sidebar selections.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
#  KPIs
# ─────────────────────────────────────────────────────────────────────────────
kpis = compute_kpis(df, df_prev if not df_prev.empty else None)


# ─────────────────────────────────────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-eyebrow">Chocolate Sales · Analytics Dashboard</div>
        <div class="hero-title">Sales Performance Overview</div>
        <div class="hero-sub">
            Showing <strong>{fmt_number(len(df))}</strong> transactions ·
            {d_start.strftime("%d %b %Y")} → {d_end.strftime("%d %b %Y")} ·
            {len(_countries)} countries · {len(_products)} products · {len(_sp)} salespeople
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    kpi_card("Total Revenue",   fmt_currency(kpis["total_revenue"]),
             delta=kpis.get("total_revenue_delta"))
with c2:
    kpi_card("Total Orders",    fmt_number(kpis["total_orders"]),
             delta=kpis.get("total_orders_delta"))
with c3:
    kpi_card("Avg Order Value", fmt_currency(kpis["avg_order_value"]),
             delta=kpis.get("avg_order_value_delta"))
with c4:
    kpi_card("Boxes Shipped",   fmt_number(kpis["total_boxes"]),
             delta=kpis.get("total_boxes_delta"))
with c5:
    kpi_card("Top Product",     kpis["top_product"],  sub="by revenue")
with c6:
    kpi_card("Top Country",     kpis["top_country"],  sub="by revenue")

divider()


# ─────────────────────────────────────────────────────────────────────────────
#  CORE DASHBOARD TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_core, tab_advanced = st.tabs([
    "Core Dashboard",
    "Advanced Analytics",
])


# ═════════════════════════════════════════════════════════════════════════════
#  CORE DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
with tab_core:

    # ── Row 1: Revenue over time + Cumulative ─────────────────────────────
    section_header(
        "Time Series", "Revenue Trend",
        "Aggregated revenue with 3-period moving average and cumulative growth.",
    )
    col_ts, col_cum = st.columns([3, 2], gap="medium")
    with col_ts:
        st.plotly_chart(sales_over_time(df, freq=chart_freq), use_container_width=True)
    with col_cum:
        st.plotly_chart(cumulative_revenue(df), use_container_width=True)

    divider()

    # ── Row 2: Country + Category donut ──────────────────────────────────
    section_header(
        "Geographic & Category Mix", "Where Revenue Comes From",
        "Country-level totals alongside product-category share.",
    )
    col_ctry, col_donut = st.columns([3, 2], gap="medium")
    with col_ctry:
        st.plotly_chart(revenue_by_country(df), use_container_width=True)
    with col_donut:
        st.plotly_chart(category_donut(df), use_container_width=True)

    divider()

    # ── Row 3: Top products + Revenue per box ─────────────────────────────
    section_header(
        "Product Analysis", "Revenue & Efficiency by Product",
        f"Top {top_n} products ranked by total revenue, and revenue per box shipped.",
    )
    col_prod, col_rpb = st.columns([1, 1], gap="medium")
    with col_prod:
        st.plotly_chart(top_products(df, top_n=top_n), use_container_width=True)
    with col_rpb:
        st.plotly_chart(revenue_per_box_chart(df), use_container_width=True)

    divider()

    # ── Row 4: Monthly trend + Boxes dist ────────────────────────────────
    section_header(
        "Seasonality & Operations", "Monthly Trends & Shipping Distribution",
        "Year-over-year monthly revenue comparison and boxes-shipped frequency.",
    )
    col_mo, col_box = st.columns([3, 2], gap="medium")
    with col_mo:
        st.plotly_chart(monthly_trend(df), use_container_width=True)
    with col_box:
        st.plotly_chart(boxes_distribution(df), use_container_width=True)

    divider()

    # ── Row 5: Heatmap ───────────────────────────────────────────────────
    section_header(
        "Cross-Dimensional View", "Revenue Heatmap: Country × Product",
        "Colour intensity reveals where specific products perform best regionally.",
    )
    st.plotly_chart(heatmap_product_country(df), use_container_width=True)

    divider()

    # ── Row 6: Salesperson bubbles ───────────────────────────────────────
    section_header(
        "Team Performance", "Salesperson Analysis",
        "Bubble size = average order value. Hover for full breakdown.",
    )
    st.plotly_chart(salesperson_performance(df), use_container_width=True)

    divider()

    # ── Row 7: Insights + Raw data ───────────────────────────────────────
    col_ins, col_tbl = st.columns([2, 3], gap="medium")
    with col_ins:
        section_header("AI Insights", "Auto-Generated Business Insights",
                       "Key findings from the filtered dataset.")
        insight_cards(generate_insights(df))

    with col_tbl:
        section_header("Raw Data", "Filtered Transaction Table",
                       f"{fmt_number(len(df))} records matching current filters.")
        display_cols = ["date", "salesperson", "country", "product",
                        "product_category", "amount", "boxes_shipped", "revenue_per_box"]
        show_df = df[display_cols].copy()
        show_df["amount"]          = show_df["amount"].apply(lambda x: f"${x:,.2f}")
        show_df["revenue_per_box"] = show_df["revenue_per_box"].apply(
            lambda x: f"${x:.2f}" if pd.notna(x) else "—"
        )
        show_df.columns = ["Date", "Salesperson", "Country", "Product",
                           "Category", "Revenue", "Boxes", "Rev/Box"]
        show_df["Date"] = pd.to_datetime(show_df["Date"]).dt.strftime("%d %b %Y")
        st.dataframe(
            show_df.sort_values("Date", ascending=False),
            use_container_width=True, height=420, hide_index=True,
        )
        st.download_button(
            label     = "Download Filtered Data (CSV)",
            data      = get_download_bytes(df),
            file_name = f"chocolate_sales_filtered_{d_start}_{d_end}.csv",
            mime      = "text/csv",
            use_container_width=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
#  ADVANCED ANALYTICS
# ═════════════════════════════════════════════════════════════════════════════
with tab_advanced:

    adv_tab1, adv_tab2, adv_tab3 = st.tabs([
        "Box Plots",
        "ARIMA Forecasting",
        "K-Means Clustering",
    ])


    # ─────────────────────────────────────────────────────────────────────
    #  ADV TAB 1 — Box Plots
    # ─────────────────────────────────────────────────────────────────────
    with adv_tab1:

        adv_section_header("Revenue Distribution — Box & Whisker")
        st.markdown(
            "Box plots reveal central tendency, spread, and outliers across groups. "
            "The box spans the interquartile range (Q1–Q3); whiskers extend to 1.5 × IQR; "
            "individual dots are statistical outliers.",
        )

        st.plotly_chart(
            boxplot_revenue_analysis(df, group_by=box_group),
            use_container_width=True,
        )

        group_label = box_group.replace("_", " ").title()
        stats_grp = (
            df.groupby(box_group)["amount"]
            .agg(
                Count   = "count",
                Median  = "median",
                Mean    = "mean",
                Std_Dev = "std",
                Q1      = lambda x: x.quantile(0.25),
                Q3      = lambda x: x.quantile(0.75),
                Min     = "min",
                Max     = "max",
            )
            .sort_values("Median", ascending=False)
            .reset_index()
        )
        stats_grp.columns = [group_label, "Count", "Median ($)", "Mean ($)",
                              "Std Dev ($)", "Q1 ($)", "Q3 ($)", "Min ($)", "Max ($)"]
        for col in ["Median ($)", "Mean ($)", "Std Dev ($)",
                    "Q1 ($)", "Q3 ($)", "Min ($)", "Max ($)"]:
            stats_grp[col] = stats_grp[col].apply(lambda x: f"${x:,.0f}")

        with st.expander("Descriptive Statistics Table", expanded=False):
            st.dataframe(stats_grp, use_container_width=True, hide_index=True)

        st.info(
            "**Reading the chart:** A narrow box with few outliers indicates consistent "
            "order sizes. A wide box signals high variability — potential for both "
            "upselling and churn risk.",
        )


    # ─────────────────────────────────────────────────────────────────────
    #  ADV TAB 2 — ARIMA Forecast
    # ─────────────────────────────────────────────────────────────────────
    with adv_tab2:

        adv_section_header("Revenue Forecasting — ARIMA Model")
        st.write("Used for time-series forecasting of revenue trends.")

        with st.spinner("Fitting ARIMA models (AIC grid search)…"):
            arima_result = run_arima_forecast(df, forecast_months=forecast_months)

        if arima_result is None:
            st.warning(
                "Not enough monthly data points for ARIMA. "
                "Expand your date range to cover at least 8 months.",
            )
        else:
            forecast_df, best_order, best_aic, fitted_vals, ts_history = arima_result
            p, d, q = best_order

            # Model KPI row
            fm1, fm2, fm3, fm4 = st.columns(4)
            with fm1:
                kpi_card("Best Model", f"ARIMA({p},{d},{q})", sub="lowest AIC order")
            with fm2:
                kpi_card("AIC Score", f"{best_aic:.1f}", sub="lower = better fit")
            with fm3:
                kpi_card(
                    "Forecast Horizon",
                    f"{forecast_months} month{'s' if forecast_months > 1 else ''}",
                    sub=f"up to {forecast_df['date'].max().strftime('%b %Y')}",
                )
            with fm4:
                kpi_card(
                    "Projected Revenue",
                    fmt_currency(forecast_df["predicted"].iloc[-1]),
                    sub=f"in {forecast_df['date'].iloc[-1].strftime('%b %Y')}",
                )

            st.plotly_chart(
                revenue_forecast_arima(
                    ts_history, forecast_df, fitted_vals, best_order, best_aic
                ),
                use_container_width=True,
            )

            with st.expander("Forecast Table", expanded=False):
                fc_display = forecast_df.copy()
                fc_display["date"]      = fc_display["date"].dt.strftime("%b %Y")
                fc_display["predicted"] = fc_display["predicted"].apply(fmt_currency)
                fc_display["ci_upper"]  = fc_display["ci_upper"].apply(fmt_currency)
                fc_display["ci_lower"]  = fc_display["ci_lower"].apply(fmt_currency)
                fc_display.columns     = ["Month", "Predicted Revenue",
                                          "Upper 95% CI", "Lower 95% CI"]
                st.dataframe(fc_display, use_container_width=True, hide_index=True)

            st.info(
                f"**Model selection:** ARIMA({p},{d},{q}) was chosen from 18 candidates "
                f"(AIC = {best_aic:.1f}). The differencing order d={d} handles "
                f"{'non-stationarity' if d > 0 else 'an already-stationary series'}. "
                "Wider CI bands in later months reflect compounding forecast uncertainty.",
            )


    # ─────────────────────────────────────────────────────────────────────
    #  ADV TAB 3 — K-Means Clustering
    # ─────────────────────────────────────────────────────────────────────
    with adv_tab3:

        adv_section_header(f"Salesperson Segmentation — K-Means (k={n_clusters})")
        st.markdown(
            "K-Means clusters salespersons into performance tiers based on "
            "**total revenue**, **order count**, **average order value**, and "
            "**revenue per box**. Features are standardised (z-scored) before clustering "
            "to prevent scale bias.",
        )
        st.write("Used to segment salespersons based on performance.")

        with st.spinner("Running K-Means clustering…"):
            cluster_df = run_kmeans_clustering(df, n_clusters=n_clusters)

        if cluster_df.empty:
            st.warning("Not enough salesperson data to cluster.")
        else:
            badge_colors = {
                "High Performer":    "#27AE60",
                "Solid Contributor": "#F39C12",
                "Growth Potential":  "#9B59B6",
            }
            cluster_summary = (
                cluster_df.groupby("cluster_label")
                .agg(Count=("salesperson", "count"), Avg_Revenue=("revenue", "mean"))
                .reset_index()
                .sort_values("Avg_Revenue", ascending=False)
            )
            badges_html = ""
            for _, row in cluster_summary.iterrows():
                lbl   = row["cluster_label"]
                color = badge_colors.get(lbl, "#3498DB")
                badges_html += (
                    f'<span class="cluster-badge" '
                    f'style="background:{color}22;color:{color};border:1px solid {color}55">' 
                    f'{lbl} ({int(row["Count"])} reps)</span>'
                )
            st.markdown(f'<div style="margin-bottom:1rem">{badges_html}</div>',
                        unsafe_allow_html=True)

            col_scatter, col_radar = st.columns([3, 2], gap="medium")
            with col_scatter:
                st.plotly_chart(salesperson_cluster_chart(cluster_df),
                                use_container_width=True)
            with col_radar:
                st.plotly_chart(cluster_radar_chart(cluster_df),
                                use_container_width=True)

            with st.expander("Cluster Assignment Table", expanded=False):
                tbl = cluster_df[[
                    "salesperson", "cluster_label", "revenue",
                    "orders", "avg_order", "revenue_per_box"
                ]].copy().sort_values(["cluster_label", "revenue"], ascending=[True, False])
                tbl["revenue"]         = tbl["revenue"].apply(fmt_currency)
                tbl["avg_order"]       = tbl["avg_order"].apply(fmt_currency)
                tbl["revenue_per_box"] = tbl["revenue_per_box"].apply(
                    lambda x: f"${x:.2f}" if pd.notna(x) else "—"
                )
                tbl.columns = ["Salesperson", "Cluster", "Revenue",
                               "Orders", "Avg Order", "Rev/Box"]
                st.dataframe(tbl, use_container_width=True, hide_index=True)

            st.info(
                "**Interpretation:** Cluster labels are assigned by average revenue rank. "
                "The radar chart normalises all features 0–1 to compare profile shapes — "
                "a cluster tall on Orders but short on Avg Order signals "
                "high-volume / lower-value selling behaviour.",
            )

# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
divider()
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;align-items:center;
                padding:0.5rem 0;font-size:0.72rem" class="muted-inline">
        <span>Chocolate Sales Analytics Dashboard · Built with Streamlit + Plotly · Scikit-Learn · Statsmodels</span>
        <span>Dataset: Kaggle – ssssws/chocolate-sales-dataset-2023-2024</span>
    </div>
    """,
    unsafe_allow_html=True,
)
