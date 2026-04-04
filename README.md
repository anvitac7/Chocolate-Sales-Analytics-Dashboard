# 🍫 Chocolate Sales Analytics Dashboard

## 🔗 Live Demo

👉 https://chocolate-sales-analytics-dashboard-rvgbedcvw3dp3qxtan2jxt.streamlit.app/

---

## 📌 Overview

An end-to-end **interactive analytics dashboard** built using **Streamlit, Plotly, and Python** to analyze chocolate sales data.

The dashboard transforms raw transactional data into **actionable business insights**, helping stakeholders:

* Track revenue trends
* Identify top-performing products & regions
* Analyze sales efficiency
* Forecast future revenue

👉 Built with a focus on **real-world business decision-making**, not just visualization.

---

## 🎯 Business Problem

Organizations need a clear understanding of:

* 📈 How sales evolve over time
* 🌍 Which regions drive the most revenue
* 🏆 Which products perform best
* 📊 How sales teams are performing

This dashboard solves these problems using **interactive analytics + machine learning**.

---

## 🚀 Key Features

### 📊 Interactive Analytics

* Dynamic filters (Country, Product, Time)
* KPI cards (Revenue, Orders, Avg Value)
* Drill-down exploration

### 📈 Advanced Visualizations

* Revenue trends with moving averages
* Country-wise performance
* Product-level insights
* Heatmaps & distribution analysis
* Salesperson performance (bubble chart)

### 🧠 Machine Learning & Advanced Analytics

* **ARIMA Forecasting** → Predict future revenue trends
* **K-Means Clustering** → Segment salespersons based on performance
* **Statistical Analysis** → Box plots for distribution insights

### ⚡ Performance Optimized

* Streamlit caching (`@st.cache_data`) for fast execution
* Modular architecture (data → preprocessing → visualization)

---

## 🧠 Key Insights Generated

* Identify **top revenue-generating countries**
* Detect **best-selling products**
* Analyze **seasonality and peak sales periods**
* Evaluate **salesperson efficiency**
* Forecast **future demand trends**

👉 Dashboards are powerful because they surface insights for decision-making ([Streamlit][1])

---

## 🛠 Tech Stack

| Layer           | Tools          |
| --------------- | -------------- |
| Language        | Python         |
| Frontend        | Streamlit      |
| Data Processing | Pandas, NumPy  |
| Visualization   | Plotly         |
| ML Models       | ARIMA, K-Means |

---

## 🏗 Project Structure

```bash
Chocolate-Sales-Analytics-Dashboard/
│
├── app.py
├── data/
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── visualization.py
│   ├── utils.py
│
├── requirements.txt
└── README.md
```

👉 Follows modular design best practices for scalability ([Mauricio Cárdenas][2])

---

## ⚙️ How to Run Locally

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


### 🌍 Regional & Product Insights
![Revenue Heatmap: Country × Product](Images/Heatmap.png)


### 🧠 Advanced Analytics (Clustering)
![Box Plots](Images/Box Plots.png)

![ARIMA Forecasting](Images/Forecasting.png)

![K-Means_Clustering](Images/K-Means_Clustering.png)

---

## 💼 Business Impact

* 📊 Improve decision-making with real-time insights
* 📦 Optimize product strategy using performance data
* 🌍 Identify high-growth markets
* 📉 Reduce risk using demand forecasting
* 👥 Improve sales team performance via segmentation

---

## 🌟 Future Improvements

* Add customer segmentation (RFM analysis)
* Deploy ML model APIs
* Add anomaly detection
* Enhance UI/UX with animations

---

## 👩‍💻 Author

**Anvita Choudhary**
Department of AI&DS
KJ Somaiya School of Engineering

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!

[1]: https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/?utm_source=chatgpt.com "Building a dashboard in Python using Streamlit"
[2]: https://mauriciojc.com/streamlit-dashboard-development-best-practices-checklist/?utm_source=chatgpt.com "Streamlit Dashboard Development Best Practices Checklist – Mauricio Cárdenas"
