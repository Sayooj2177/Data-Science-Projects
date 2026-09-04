# 📦 Supply Chain Analysis

## 📌 Project Overview

This project analyzes supply chain operations using **SQL, Excel, and Tableau** to identify patterns in sales, revenue, profitability, inventory levels, supplier performance, promotions, and demand forecasting.

The analysis is based on **91,250 supply chain records** covering multiple SKUs, warehouses, suppliers, and regions throughout 2024.

The goal is to transform raw supply chain data into actionable business insights that can support better inventory management, supplier evaluation, sales planning, and operational decision-making.

---

## 🎯 Business Objectives

- Analyze overall sales, revenue, and profitability
- Identify monthly sales and revenue trends
- Compare regional performance
- Evaluate warehouse performance
- Analyze supplier performance and lead times
- Identify high-performing SKUs
- Analyze inventory levels and reorder-point risk
- Evaluate stockout patterns
- Measure promotion performance
- Evaluate demand forecast accuracy

---

## 🗂️ Project Structure

```text
Supply Chain Analysis/
├── Data/
│   └── supply_chain_dataset.csv
├── SQL/
│   └── supply_chain_analysis.sql
├── Excel/
│   └── supply_chain_analysis.xlsx
├── Tableau/
│   └── supply_chain_dashboard.twbx
└── README.md
Tools & Technologies
MySQL — Data validation and business analysis
Microsoft Excel — Data analysis and reporting
Tableau — Interactive dashboard and visualization
SQL — Aggregation, filtering, grouping, and KPI analysis
GitHub — Project version control and portfolio management
📊 Dataset Overview
Metric	Value
Total Records	91,250
SKUs	50
Warehouses	5
Suppliers	10
Regions	4
Date Range	Jan 2024 – Dec 2024
💰 Key Business KPIs
KPI	Result
Total Units Sold	1,829,979
Total Revenue	33,426,337.22
Total Profit	11,088,021.23
Profit Margin	33.17%
Average Inventory	471.52
Average Supplier Lead Time	7.98 days
Stockout Rate	0.00%
🔍 Key Analysis
1. Overall Business Performance

Analyzed total units sold, revenue, profit, profit margin, inventory levels, supplier lead time, and stockout performance.

2. Monthly Performance

Analyzed monthly sales, revenue, and profit trends to identify strong and weak periods throughout the year.

March recorded the highest unit sales.
September recorded the lowest unit sales and revenue.
3. Regional Performance

Compared the four operating regions based on sales, revenue, profit, and inventory.

North generated the highest revenue.
East generated the highest profit.
Overall regional performance was relatively balanced.
4. Warehouse Performance

Compared warehouses based on sales, revenue, profit, and inventory levels to identify high-performing and lower-performing locations.

5. Supplier Performance

Evaluated suppliers using revenue, profit, sales volume, and average lead time.

This helps identify suppliers with strong financial contribution as well as suppliers with relatively higher lead times.

6. SKU Performance

Identified top-performing products based on:

Revenue
Profit
Profit margin

SKU-level analysis helps highlight products that contribute significantly to business performance.

7. Inventory & Reorder Analysis

Analyzed inventory buffers and the number of days inventory fell below the reorder point.

Although some warehouse-SKU combinations frequently fell below their reorder points, the dataset recorded no stockout events.

8. Promotion Analysis

Compared sales performance between promotional and non-promotional periods to understand the relationship between promotions and unit sales.

9. Demand Forecast Accuracy

Evaluated forecast performance using:

MAE: 2.38
MAPE: 16.32%

These metrics provide an indication of how closely forecasted demand matched actual demand.

📈 Dashboard

The Tableau dashboard provides interactive views of:

Sales & revenue performance
Profitability
Monthly trends
Regional performance
Warehouse performance
Supplier performance
SKU performance
Inventory risk
Promotion performance
Forecast accuracy
💡 Business Insights

The analysis highlights several important supply chain observations:

Overall profitability remained strong with a 33.17% profit margin.
Sales performance varied considerably across months.
Regional performance was relatively balanced, with North leading revenue.
Supplier lead times varied across suppliers and may influence inventory planning.
Certain SKU-warehouse combinations showed higher inventory buffers.
Some SKU-warehouse combinations frequently fell below reorder points despite having no stockouts.
Promotional periods showed higher average unit sales than non-promotional periods.
Forecast accuracy indicates opportunities for further demand-planning improvements.
🚀 Recommendations

Based on the analysis:

Review SKU-warehouse combinations with frequent reorder-point breaches.
Monitor suppliers with relatively high lead times.
Optimize inventory buffers based on demand patterns.
Investigate seasonal changes in monthly sales.
Evaluate promotional strategies based on their impact on unit sales and profitability.
Improve demand forecasting to support better inventory planning.
Use SKU-level profitability to prioritize high-value products.
📚 Skills Demonstrated
SQL Data Analysis
Data Cleaning & Validation
Business KPI Analysis
Inventory Analysis
Supply Chain Analytics
Sales & Profitability Analysis
Supplier Performance Analysis
Demand Forecast Evaluation
Excel Analysis
Tableau Dashboard Development
Data Visualization
Business Insight Generation

Author

Sayooj Chandran

Data Analyst | Business Intelligence | Data Science