import streamlit as st
from src.data_loader import get_data
from src.visualization import *
from src.insights import generate_insights
from src.utils import fmt_currency

st.set_page_config(page_title="Chocolate Sales Dashboard", layout="wide")

# ─────────────────────────────────────────────────────────────
# 🎯 HEADER (VERY IMPORTANT)
# ─────────────────────────────────────────────────────────────
st.title("🍫 Chocolate Sales Analytics Dashboard")

st.markdown("""
### 💼 Business Objective
This dashboard helps analyze chocolate sales performance, identify top markets, 
forecast future revenue, and optimize business strategy using data-driven insights.
""")

# ─────────────────────────────────────────────────────────────
# 📦 LOAD DATA (with loading state)
# ─────────────────────────────────────────────────────────────
with st.spinner("Loading and processing data..."):
    df = get_data()

# ─────────────────────────────────────────────────────────────
# 🎛️ SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

countries = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].unique(),
    default=df["country"].unique()
)

products = st.sidebar.multiselect(
    "Select Product",
    options=df["product"].unique(),
    default=df["product"].unique()
)

# Filter data
filtered_df = df[
    (df["country"].isin(countries)) &
    (df["product"].isin(products))
]

# ─────────────────────────────────────────────────────────────
# ⚠️ EMPTY STATE HANDLING
# ─────────────────────────────────────────────────────────────
if filtered_df.empty:
    st.warning("⚠️ No data available for selected filters")
    st.stop()

# ─────────────────────────────────────────────────────────────
# 📊 KPI SECTION
# ─────────────────────────────────────────────────────────────
total_revenue = filtered_df["amount"].sum()
total_orders = filtered_df.shape[0]
avg_order = filtered_df["amount"].mean()

top_country = (
    filtered_df.groupby("country")["amount"].sum().idxmax()
)
top_product = (
    filtered_df.groupby("product")["amount"].sum().idxmax()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", fmt_currency(total_revenue))
col2.metric("📦 Total Orders", f"{total_orders:,}")
col3.metric("📊 Avg Order Value", fmt_currency(avg_order))
col4.metric("🌍 Top Country", top_country)

# ─────────────────────────────────────────────────────────────
# 🧠 INSIGHT HIGHLIGHTS (NEW 🔥)
# ─────────────────────────────────────────────────────────────
st.info(
    f"""
    🔹 Top Performing Country: **{top_country}**  
    🔹 Best Selling Product: **{top_product}**  
    🔹 Total Revenue Generated: **{fmt_currency(total_revenue)}**
    """
)

# ─────────────────────────────────────────────────────────────
# 📈 MAIN CHARTS
# ─────────────────────────────────────────────────────────────
st.markdown("## 📊 Sales Overview")

with st.spinner("Generating charts..."):

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            sales_over_time(filtered_df),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            revenue_by_country(filtered_df),
            use_container_width=True
        )

    st.plotly_chart(
        top_products(filtered_df),
        use_container_width=True
    )

# ─────────────────────────────────────────────────────────────
# 📊 ADVANCED ANALYTICS
# ─────────────────────────────────────────────────────────────
st.markdown("## 🧠 Advanced Analytics")

tab1, tab2 = st.tabs(["📈 Forecasting", "👥 Clustering"])

# ─── Forecasting ─────────────────────────────────────────────
with tab1:
    st.caption("ARIMA model predicts future revenue trends based on historical data.")

    try:
        from src.utils import run_arima_forecast

        ts, forecast_df, fitted, order, aic = run_arima_forecast(filtered_df)

        fig = revenue_forecast_arima(ts, forecast_df, fitted, order, aic)
        st.plotly_chart(fig, use_container_width=True)

    except Exception:
        st.error("Forecast could not be generated for selected filters")

# ─── Clustering ──────────────────────────────────────────────
with tab2:
    st.caption("K-Means clustering groups salespersons based on performance metrics.")

    try:
        from src.utils import run_kmeans_clustering

        cluster_df = run_kmeans_clustering(filtered_df)

        st.plotly_chart(
            salesperson_cluster_chart(cluster_df),
            use_container_width=True
        )

        st.plotly_chart(
            cluster_radar_chart(cluster_df),
            use_container_width=True
        )

    except Exception:
        st.error("Clustering could not be performed")

# ─────────────────────────────────────────────────────────────
# 📌 BUSINESS RECOMMENDATIONS (🔥 BIG DIFFERENCE)
# ─────────────────────────────────────────────────────────────
st.markdown("## 📌 Business Recommendations")

st.success("""
- Focus on high-performing countries to maximize revenue  
- Increase inventory before peak demand periods  
- Train low-performing salespersons identified via clustering  
- Promote high-margin products to improve profitability  
""")

# ─────────────────────────────────────────────────────────────
# 📥 DOWNLOAD DATA
# ─────────────────────────────────────────────────────────────
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_sales_data.csv"
)