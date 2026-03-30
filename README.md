# 🍫 Chocolate Sales Analytics Dashboard

> A production-grade interactive business intelligence dashboard built with **Streamlit** and **Plotly**, analysing global chocolate sales data from 2023–2024.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.20%2B-3F4F75?logo=plotly)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Project Overview

This dashboard transforms raw transactional chocolate sales data into actionable business insights through a clean, interactive UI. It covers the full data pipeline — from loading and cleaning to feature engineering and multi-dimensional visualisation.

**Dataset:** [Kaggle – Chocolate Sales Dataset 2023–2024](https://www.kaggle.com/datasets/ssssws/chocolate-sales-dataset-2023-2024)
**Fields:** `Sales Person`, `Country`, `Product`, `Date`, `Amount`, `Boxes Shipped`

---

## ✨ Features

### 🎛️ Interactive Sidebar Filters
| Filter | Description |
|---|---|
| Date range | Restrict analysis to any custom time window |
| Country | Multi-select from 6 countries |
| Product | Multi-select from 20 chocolate products |
| Sales Person | Focus on individual or team performance |
| Chart granularity | Switch between weekly / monthly / quarterly views |
| Top-N | Adjust how many products appear in rankings |

### 📊 KPI Cards (auto-computed, delta vs prior period)
- **Total Revenue** · **Total Orders** · **Avg Order Value**
- **Boxes Shipped** · **Top Product** · **Top Country**

### 📈 10 Interactive Plotly Charts
| # | Chart | Insight |
|---|---|---|
| 1 | **Revenue over time** (area + MA) | Trend + peak detection |
| 2 | **Cumulative revenue** (step area) | Growth trajectory |
| 3 | **Revenue by country** (bar) | Geographic winners |
| 4 | **Category donut** | Revenue mix at a glance |
| 5 | **Top N products** (horizontal bar) | Best-sellers ranked |
| 6 | **Revenue per box** (efficiency bar) | Profit-per-unit leaders |
| 7 | **Monthly trend YoY** (grouped bar) | Seasonality patterns |
| 8 | **Boxes shipped distribution** (histogram) | Operational logistics insight |
| 9 | **Country × Product heatmap** | Cross-market performance |
| 10 | **Salesperson bubble chart** | Team performance overview |

### 🧠 Auto-Generated Insights
Six business insight cards are dynamically generated from the filtered slice — covering top performer, dominant market, best-seller, peak season, most efficient product, and Pareto concentration analysis.

### ⬇️ Data Export
One-click download of the currently filtered dataset as a CSV file.

### 🌗 Dark / Light Mode
Toggle between dark (default) and light themes from the sidebar.

---

## 🗂️ Project Structure

```
chocolate-sales-dashboard/
│
├── app.py                  # Main Streamlit entry point
│
├── data/
│   └── chocolate_sales.csv # Raw dataset (replace with Kaggle download)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # CSV loading with @st.cache_data
│   ├── preprocessing.py    # Cleaning, parsing, feature engineering
│   ├── visualization.py    # All 10 Plotly chart functions
│   └── utils.py            # KPIs, insights, formatters, colour palette
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/chocolate-sales-dashboard.git
cd chocolate-sales-dashboard
```

### 2. Set up the Python environment
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add the dataset
Download **chocolate_sales.csv** from [Kaggle](https://www.kaggle.com/datasets/ssssws/chocolate-sales-dataset-2023-2024) and place it in:
```
data/chocolate_sales.csv
```
> A realistic sample dataset is already included so the dashboard works out of the box.

### 4. Run the dashboard
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Dashboard** | Streamlit 1.32+ |
| **Charts** | Plotly 5.20+ |
| **Data** | Pandas 2.1+, NumPy 1.26+ |
| **Stats** | SciPy (distribution curves) |
| **ML** | Scikit-learn (K-Means clustering) |
| **Time Series** |	Statsmodels (ARIMA forecasting) |
| **Styling** | Custom CSS injected via `st.markdown` |

---

## 🧠 Data Processing Pipeline

```
Raw CSV
  │
  ▼
data_loader.py      ← load_raw_data() with @st.cache_data
  │
  ▼
preprocessing.py    ← preprocess()
  ├── _clean_column_names()      # Standardise to snake_case
  ├── _remove_duplicates()       # Drop exact duplicate rows
  ├── _parse_amount()            # "$1,234.56" → 1234.56 (float)
  ├── _parse_dates()             # str → datetime + Year/Month/Quarter
  ├── _handle_missing()          # Drop critical nulls, fill numeric medians
  └── _derive_features()         # revenue_per_box, product_category, region, high_value_order
  │
  ▼
apply_filters()     ← respects sidebar selections, returns filtered slice
  │
  ▼
visualization.py    ← pure chart functions (DataFrame → go.Figure)
utils.py            ← KPIs, insights, formatting helpers
  │
  ▼
app.py              ← renders everything with st.plotly_chart / st.markdown
```

---

## 🔬 Advanced Analytics
### Box Plot Analysis
- Interactive box-and-whisker plots for revenue distribution
- Group by country, salesperson, product category, or product
- Descriptive statistics table with quartiles and outliers

### ARIMA Forecasting
- Auto-selects best ARIMA(p,d,q) model via AIC grid search
- Projects revenue 1–6 months forward with 95% confidence intervals
- Visual comparison of historical data, in-sample fit, and forecast

### K-Means Clustering
-Segments salespersons into performance tiers (High Performer, Solid Contributor, Growth Potential)
- Features: total revenue, order count, average order value, revenue per box
- Scatter plot + radar chart for cluster profile comparison

---

## 📸 Screenshots

| Hero + KPIs | Time Series |
|---|---|
| *(add screenshot)* | *(add screenshot)* |

| Heatmap | Insights |
|---|---|
| *(add screenshot)* | *(add screenshot)* |

> Run the app and take screenshots. Save them to `assets/` and update the paths above.

---

## 🔮 Future Improvements

- [ ] **Streamlit Cloud deployment** — add `secrets.toml` for cloud dataset loading
- [ ] **Google Sheets integration** — live data refresh via `gspread`
- [ ] **PDF export** — generate a one-page summary report with `WeasyPrint`
- [ ] **User authentication** — `streamlit-authenticator` for role-based views
- [ ] **A/B testing view** — compare two custom time periods side by side
- [ ] **Map visualisation** — `px.choropleth` world map for country-level revenue

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE) © 2024 [Your Name]

---
