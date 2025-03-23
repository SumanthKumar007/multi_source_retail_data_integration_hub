# DataFoundation: Multi-source Retail Data Integration Hub

## 📌 Project Overview
The **DataFoundation: Multi-source Retail Data Integration Hub** is an end-to-end **ETL (Extract, Transform, Load) pipeline** that integrates retail datasets from Kaggle into a structured **MySQL data warehouse**. This hub enables **data-driven decision-making** through interactive dashboards and insightful analytics.

## 🛠️ Technologies Used
- **Python** 🐍 (for ETL, data processing, and visualization)
- **SQL** (for data transformation and warehouse structuring)
- **MySQL** 🗄️ (as the primary database for storing processed data)
- **Pandas** 📊 (for data manipulation and cleaning)
- **Matplotlib & Plotly** 📈 (for data visualization)
- **Streamlit** 🚀 (for building interactive dashboards)
- **Git** 🔄 (for version control and collaboration)
- **PyMySQL** 🔌 (to connect Python scripts to MySQL for database interactions)
- **MySQL Connector** 🔗 (alternative MySQL connection library for seamless queries)

## 🏗️ ETL Pipeline Workflow
### **Extract** 📥
- Load raw data from Kaggle CSV files.

### **Transform** 🔄
- Data cleansing (handling **nulls, duplicates, inconsistencies**).
- Aggregation of key metrics (**sales, revenue, product performance**).
- Implementation of **Slowly Changing Dimension Type 2 (SCD Type 2)** for historical tracking.

### **Load** 📤
- Store transformed data into a **MySQL data warehouse**.

## 📊 Data Warehouse Design
### **Fact Table**
- `fact_orders`

### **Dimension Tables**
- `dim_products`
- `dim_customers`
- `dim_dates`
- `dim_payments`
- `dim_sellers`

### **Data Marts Tables**
- `dm_product_category`
- `dm_sales_performance`
- `dm_sales_trends`

## 🌟 Streamlit Dashboard Features
### **📌 Sidebar Navigation**
- 🎯 **Sales Performance**: State-wise revenue analysis.
- 📦 **Product Analysis**: Revenue breakdown by product category.
- 📊 **Aggregation**: Daily, monthly, and category-wise revenue trends.
- 📑 **Business Metrics**: KPI insights from `business_metrics_view`.
- 📆 **Date-Based Trends**: Time-series analysis of sales trends.

### **📊 Key Visualizations**
- **Bar Charts** (State-wise revenue, Business KPIs)
- **Line Charts** (Sales trends over time)
- **Pie Charts** (Revenue distribution by category)
- **Donut Charts** (Proportional sales analysis)

## 🚀 How to Run the Project
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo-url.git
cd datafoundation-retail-hub
```

### **2️⃣ Set Up MySQL Database**
- Create a MySQL database (`Project_db`).
- Load pre-processed data using `data_loader.py`.

### **3️⃣ Run the Streamlit Dashboard**
```sh
streamlit run app.py
```

## 📢 Contributions & Feedback
We welcome contributions! Feel free to submit **issues, pull requests, or feature suggestions** to enhance this project.

---
🔗 **Developed by Sumanth Kumar**

