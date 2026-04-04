# 🍫 Chocolate Sales Intelligence Platform

## 🚀 Live Application

👉 https://chocolate-sales-analytics-dashboard-rvgbedcvw3dp3qxtan2jxt.streamlit.app/

---

## 🧠 From Raw Data to Business Decisions

Most dashboards stop at visualization.
This project goes further — it transforms raw chocolate sales data into a **decision-making system** powered by analytics and machine learning.

It answers not just:

* *What is happening?*
* *What will happen next?*

But also begins to uncover:

* *Where should the business focus to grow revenue?*

---

## 🎯 Problem Statement

Sales teams and business stakeholders often lack clear answers to:

* Which markets are truly driving revenue?
* What products should be prioritized?
* Are sales trends seasonal or consistent?
* How do we forecast demand reliably?
* Which salespersons contribute the most impact?

Without these insights, decisions are reactive rather than strategic.

---

## 💡 Solution

This project delivers an **interactive analytics platform** that combines:

* 📊 Real-time exploratory data analysis
* 📈 Time-series forecasting
* 🧠 Sales performance segmentation
* 📌 Actionable business insights

All within a single, intuitive Streamlit interface.

---

## ⚡ Key Capabilities

### 🔹 1. Interactive Business Dashboard

* Dynamic filtering by country, product, and time
* Real-time KPI updates
* Drill-down analysis for granular insights

---

### 🔹 2. Executive KPI Layer

Quick snapshot of business health:

* **Total Revenue**
* **Total Orders**
* **Average Order Value**
* **Top Performing Product**

---

### 🔹 3. Advanced Visual Analytics

* 📈 Revenue trends with moving averages
* 🌍 Country-level performance comparison
* 🏆 Product-wise contribution analysis
* 🔥 Heatmaps (Country × Product)
* 👥 Salesperson performance (bubble chart)

---

## 🤖 Machine Learning Layer

### 📈 Time-Series Forecasting

**Model Used:** ARIMA

* Captures temporal patterns in revenue
* Models trend and seasonality
* Enables short-term demand forecasting

**Business Impact:**

* Supports inventory planning
* Reduces overstocking/stockouts
* Improves revenue predictability

---

### 👥 Sales Segmentation

**Model Used:** K-Means Clustering

* Groups salespersons based on performance patterns
* Identifies high vs low performers

**Business Impact:**

* Enables targeted training programs
* Helps optimize sales team strategy

---

## 📊 Model Evaluation & Reliability

To ensure trust in predictions:

### Forecasting Model

* RMSE (error magnitude)
* MAE (prediction accuracy)

### Clustering Model

* Inertia (cluster compactness)
* Silhouette Score (cluster quality)

---

## 🔍 Key Insights Discovered

* 🌍 A small number of countries drive a disproportionate share of revenue
* 🏆 Top-performing products contribute significantly to overall sales
* 📈 Clear seasonal patterns exist in revenue trends
* 👥 Sales performance varies widely across clusters
* 🔮 Forecasting reveals predictable short-term demand patterns

---

## 💼 Business Recommendations

Based on analysis:

* Focus marketing on **high-revenue regions**
* Promote **top-performing products** to maximize ROI
* Upskill **low-performing sales clusters**
* Use forecasting for **inventory and supply chain optimization**

---

## 🏗️ System Design

```bash
Chocolate-Sales-Analytics-Dashboard/
│
├── app.py                  # Streamlit entry point
├── data/                   # Raw dataset
├── src/
│   ├── data_loader.py      # Data ingestion
│   ├── preprocessing.py    # Cleaning & feature engineering
│   ├── visualization.py    # Plotly charts
│   └── utils.py            # Helper functions
│
├── Images/                 # Dashboard previews
├── requirements.txt
└── README.md
```

### Design Principles:

* Modular architecture
* Separation of concerns
* Scalable and maintainable codebase

---

## ⚙️ Local Setup

```bash
git clone https://github.com/anvitac7/Chocolate-Sales-Analytics-Dashboard
cd Chocolate-Sales-Analytics-Dashboard

pip install -r requirements.txt
streamlit run app.py
```

---

## 📷 Dashboard Preview

### 🏠 Main Dashboard

![Main Dashboard](Images/Main.png)

### 📈 Sales Trends & Forecasting

![Revenue Trend](Images/Revenue_Trend.png)

![Product Analysis](Images/Product_Analysis.png)

### 🌍 Regional Insights

![Heatmap](Images/Heatmap.png)

### 🧠 Advanced Analytics

![Box Plots](Images/Box_Plots.png)

![Forecasting](Images/Forecasting.png)

![K-Means](Images/K-Means_Clustering.png)

---

## ⚡ Performance Optimization

* Streamlit caching (`@st.cache_data`) for faster load times
* Efficient preprocessing pipeline
* Optimized data transformations

---

## 📈 Scalability & Future Work

* Integrate real-time data pipelines (APIs)
* Compare forecasting models (Prophet, LSTM)
* Add anomaly detection for sales spikes
* Implement customer segmentation (RFM analysis)

---

## 👩‍💻 About the Author

**Anvita Choudhary**
AI & Data Science Student
KJ Somaiya School of Engineering

---

## ⭐ If You Found This Useful

Give it a ⭐ on GitHub — it helps the project reach more people!
