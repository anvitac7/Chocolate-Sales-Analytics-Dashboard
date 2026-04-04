# 🍫 Chocolate Sales Analytics Dashboard

## 📌 Overview

An interactive **Streamlit dashboard** built using chocolate sales data to analyze revenue trends, product performance, and country-wise insights.

---

## 🎯 Problem Statement

Businesses need a clear understanding of:

* Sales performance over time
* Top-performing products
* Revenue distribution across regions

This dashboard provides **data-driven insights** for decision-making.

---

## 🚀 Features

* 📊 Interactive filters (Country, Product)
* 📈 Sales trend analysis
* 🌍 Revenue by country
* 🏆 Top products visualization
* 📥 Download filtered dataset
* 🧠 Auto-generated insights

---

## 🛠 Tech Stack

* Python
* Streamlit
* Pandas
* Plotly

---

## 📷 Dashboard Preview

(Add screenshot here)

---

## ⚙️ How to Run

```bash
git clone https://github.com/anvitac7/Chocolate-Sales-Analytics-Dashboard
cd Chocolate-Sales-Analytics-Dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌟 Future Improvements

* Add ML model for sales prediction
* Deploy on Streamlit Cloud
* Add advanced filters (date range)
* Improve UI/UX

---

## 💡 Key Insights

<<<<<<< Updated upstream
* Identify top revenue-generating countries
* Discover best-selling products
* Analyze seasonal trends
=======
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
>>>>>>> Stashed changes
