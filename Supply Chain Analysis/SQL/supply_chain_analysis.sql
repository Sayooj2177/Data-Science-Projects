-- ============================================================
-- SUPPLY CHAIN ANALYSIS
-- SQL ANALYTICS PROJECT
-- ============================================================


-- ============================================================
-- 1. SELECT DATABASE
-- Purpose: Select the database used for the analysis
-- ============================================================

USE supply_chain_analysis;


-- ============================================================
-- 2. DATASET IMPORT & VALIDATION
-- Purpose: Import the CSV dataset into the analysis table
-- ============================================================

LOAD DATA LOCAL INFILE '/Users/sayoojchandran/Desktop/Supply Chain Analysis/supply_chain_dataset.csv'
INTO TABLE supply_chain_dataset
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- ============================================================
-- 3. DATASET ROW COUNT
-- Purpose: Confirm the number of records in the dataset
-- ============================================================

SELECT
    COUNT(*) AS total_rows
FROM supply_chain_dataset;


-- ============================================================
-- 4. DATASET PREVIEW
-- Purpose: Preview the first few records
-- ============================================================

SELECT *
FROM supply_chain_dataset
LIMIT 10;


-- ============================================================
-- 5. DATASET SUMMARY
-- Purpose: Understand the number of SKUs, warehouses,
--          suppliers and regions
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT SKU_ID) AS total_skus,
    COUNT(DISTINCT Warehouse_ID) AS total_warehouses,
    COUNT(DISTINCT Supplier_ID) AS total_suppliers,
    COUNT(DISTINCT Region) AS total_regions
FROM supply_chain_dataset;


-- ============================================================
-- 6. DATE RANGE
-- Purpose: Identify the period covered by the dataset
-- ============================================================

SELECT
    MIN(Date) AS start_date,
    MAX(Date) AS end_date
FROM supply_chain_dataset;


-- ============================================================
-- 7. DATA QUALITY / MISSING VALUES
-- Purpose: Check important columns for missing values
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    SUM(Date IS NULL) AS missing_date,
    SUM(SKU_ID IS NULL) AS missing_sku,
    SUM(Warehouse_ID IS NULL) AS missing_warehouse,
    SUM(Supplier_ID IS NULL) AS missing_supplier,
    SUM(Region IS NULL) AS missing_region,
    SUM(Units_Sold IS NULL) AS missing_units_sold,
    SUM(Inventory_Level IS NULL) AS missing_inventory,
    SUM(Supplier_Lead_Time_Days IS NULL) AS missing_lead_time,
    SUM(Reorder_Point IS NULL) AS missing_reorder_point,
    SUM(Order_Quantity IS NULL) AS missing_order_quantity,
    SUM(Unit_Cost IS NULL) AS missing_unit_cost,
    SUM(Unit_Price IS NULL) AS missing_unit_price,
    SUM(Promotion_Flag IS NULL) AS missing_promotion,
    SUM(Stockout_Flag IS NULL) AS missing_stockout,
    SUM(Demand_Forecast IS NULL) AS missing_forecast
FROM supply_chain_dataset;


-- ============================================================
-- 8. DUPLICATE CHECK
-- Purpose: Identify duplicate records using Date, SKU,
--          Warehouse and Supplier as the business key
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(
        DISTINCT Date,
        SKU_ID,
        Warehouse_ID,
        Supplier_ID
    ) AS unique_records,
    COUNT(*) -
    COUNT(
        DISTINCT Date,
        SKU_ID,
        Warehouse_ID,
        Supplier_ID
    ) AS duplicate_records
FROM supply_chain_dataset;


-- ============================================================
-- 9. OVERALL BUSINESS KPIs
-- Purpose: Calculate the main business and operational KPIs
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS total_revenue,

    ROUND(
        SUM(Units_Sold * (Unit_Price - Unit_Cost)),
        2
    ) AS total_profit,

    ROUND(
        100 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        )
        / NULLIF(
            SUM(Units_Sold * Unit_Price),
            0
        ),
        2
    ) AS profit_margin_pct,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time_days,

    SUM(Stockout_Flag) AS total_stockout_days
FROM supply_chain_dataset;


-- ============================================================
-- 10. OVERALL SALES / REVENUE / PROFIT
-- Purpose: Calculate total revenue, cost and profit
-- ============================================================

SELECT
    SUM(Units_Sold * Unit_Price) AS total_revenue,

    SUM(Units_Sold * Unit_Cost) AS total_cost,

    SUM(
        Units_Sold * (Unit_Price - Unit_Cost)
    ) AS total_profit,

    ROUND(
        AVG(Unit_Price),
        2
    ) AS avg_selling_price,

    ROUND(
        AVG(Unit_Cost),
        2
    ) AS avg_unit_cost
FROM supply_chain_dataset;


-- ============================================================
-- 11. OVERALL OPERATIONAL METRICS
-- Purpose: Analyze units sold, orders, inventory,
--          lead time and stockouts
-- ============================================================

SELECT
    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        AVG(Units_Sold),
        2
    ) AS avg_units_sold,

    SUM(Order_Quantity) AS total_order_quantity,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory_level,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_supplier_lead_time,

    SUM(Stockout_Flag) AS total_stockout_days
FROM supply_chain_dataset;


-- ============================================================
-- 12. MONTHLY SALES TREND
-- Purpose: Analyze monthly units sold, revenue and profit
-- ============================================================

SELECT
    DATE_FORMAT(Date, '%Y-%m') AS month,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit

FROM supply_chain_dataset

GROUP BY DATE_FORMAT(Date, '%Y-%m')

ORDER BY month;


-- ============================================================
-- 13. REGIONAL PERFORMANCE
-- Purpose: Compare sales, revenue, profit and inventory
--          across regions
-- ============================================================

SELECT
    Region,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory

FROM supply_chain_dataset

GROUP BY Region

ORDER BY revenue DESC;


-- ============================================================
-- 14. SUPPLIER PERFORMANCE
-- Purpose: Evaluate supplier sales, orders, revenue,
--          profit and lead time
-- ============================================================

SELECT
    Supplier_ID,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time_days,

    SUM(Order_Quantity) AS total_order_quantity,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit

FROM supply_chain_dataset

GROUP BY Supplier_ID

ORDER BY avg_lead_time_days DESC;


-- ============================================================
-- 15. INVENTORY / REORDER ANALYSIS
-- Purpose: Identify warehouse-SKU combinations with
--          the lowest inventory buffer
-- ============================================================

SELECT
    Warehouse_ID,
    SKU_ID,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory,

    ROUND(
        AVG(Reorder_Point),
        2
    ) AS avg_reorder_point,

    ROUND(
        AVG(Inventory_Level - Reorder_Point),
        2
    ) AS avg_inventory_buffer

FROM supply_chain_dataset

GROUP BY Warehouse_ID, SKU_ID

ORDER BY avg_inventory_buffer ASC

LIMIT 10;


-- ============================================================
-- 16. TOP 10 WAREHOUSE-SKU INVENTORY BUFFERS
-- Purpose: Identify warehouse-SKU combinations with
--          the largest inventory buffer
-- ============================================================

SELECT
    Warehouse_ID,
    SKU_ID,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory,

    ROUND(
        AVG(Reorder_Point),
        2
    ) AS avg_reorder_point,

    ROUND(
        AVG(Inventory_Level - Reorder_Point),
        2
    ) AS avg_inventory_buffer

FROM supply_chain_dataset

GROUP BY Warehouse_ID, SKU_ID

ORDER BY avg_inventory_buffer DESC

LIMIT 10;


-- ============================================================
-- 17. DAYS BELOW REORDER POINT
-- Purpose: Identify warehouse-SKU combinations that
--          frequently fall below their reorder point
-- ============================================================

SELECT
    Warehouse_ID,
    SKU_ID,

    COUNT(*) AS total_days,

    SUM(
        Inventory_Level < Reorder_Point
    ) AS days_below_reorder_point,

    ROUND(
        100.0 *
        SUM(Inventory_Level < Reorder_Point)
        / COUNT(*),
        2
    ) AS pct_days_below_reorder_point

FROM supply_chain_dataset

GROUP BY Warehouse_ID, SKU_ID

ORDER BY pct_days_below_reorder_point DESC

LIMIT 10;


-- ============================================================
-- 18. STOCKOUT BY WAREHOUSE / SKU
-- Purpose: Identify warehouse-SKU combinations with
--          the highest stockout rates
-- ============================================================

SELECT
    Warehouse_ID,
    SKU_ID,

    COUNT(*) AS total_days,

    SUM(Stockout_Flag) AS stockout_days,

    ROUND(
        100.0 *
        SUM(Stockout_Flag)
        / COUNT(*),
        2
    ) AS stockout_rate_pct

FROM supply_chain_dataset

GROUP BY Warehouse_ID, SKU_ID

ORDER BY stockout_rate_pct DESC

LIMIT 10;


-- ============================================================
-- 19. OVERALL STOCKOUT RATE
-- Purpose: Calculate the overall percentage of stockout days
-- ============================================================

SELECT
    SUM(Stockout_Flag) AS total_stockout_days,

    COUNT(*) AS total_days,

    ROUND(
        100.0 *
        SUM(Stockout_Flag)
        / COUNT(*),
        2
    ) AS overall_stockout_rate_pct

FROM supply_chain_dataset;


-- ============================================================
-- 20. STOCKOUT BY REGION
-- Purpose: Compare stockout rates across regions
-- ============================================================

SELECT
    Region,

    COUNT(*) AS total_days,

    SUM(Stockout_Flag) AS stockout_days,

    ROUND(
        100.0 *
        SUM(Stockout_Flag)
        / COUNT(*),
        2
    ) AS stockout_rate_pct

FROM supply_chain_dataset

GROUP BY Region

ORDER BY stockout_rate_pct DESC;


-- ============================================================
-- 21. PROMOTION ANALYSIS
-- Purpose: Compare sales and profitability during
--          promotional and non-promotional periods
-- ============================================================

SELECT
    Promotion_Flag,

    COUNT(*) AS total_records,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        AVG(Units_Sold),
        2
    ) AS avg_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit

FROM supply_chain_dataset

GROUP BY Promotion_Flag

ORDER BY Promotion_Flag;


-- ============================================================
-- 22. WAREHOUSE PERFORMANCE
-- Purpose: Compare warehouse sales, revenue, profit,
--          inventory and lead time
-- ============================================================

SELECT
    Warehouse_ID,

    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time

FROM supply_chain_dataset

GROUP BY Warehouse_ID

ORDER BY revenue DESC;


-- ============================================================
-- 23. TOP 10 SKUs BY REVENUE
-- Purpose: Identify the highest-revenue products
-- ============================================================

SELECT
    SKU_ID,

    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory

FROM supply_chain_dataset

GROUP BY SKU_ID

ORDER BY revenue DESC

LIMIT 10;


-- ============================================================
-- 24. TOP 10 SKUs BY PROFIT
-- Purpose: Identify the most profitable products
-- ============================================================

SELECT
    SKU_ID,

    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        100 *
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        )
        / NULLIF(
            SUM(Units_Sold * Unit_Price),
            0
        ),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY SKU_ID

ORDER BY profit DESC

LIMIT 10;


-- ============================================================
-- 25. TOP 10 WAREHOUSE-SKU COMBINATIONS BY PROFIT
-- Purpose: Identify the most profitable product-location
--          combinations
-- ============================================================

SELECT
    Warehouse_ID,
    SKU_ID,

    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit

FROM supply_chain_dataset

GROUP BY Warehouse_ID, SKU_ID

ORDER BY profit DESC

LIMIT 10;


-- ============================================================
-- 26. DEMAND FORECAST ACCURACY
-- Purpose: Measure forecast accuracy using MAE and MAPE
-- ============================================================

SELECT
    ROUND(
        AVG(
            ABS(
                Units_Sold - Demand_Forecast
            )
        ),
        2
    ) AS MAE,

    ROUND(
        AVG(
            ABS(
                Units_Sold - Demand_Forecast
            )
            / NULLIF(Units_Sold, 0)
        ) * 100,
        2
    ) AS MAPE

FROM supply_chain_dataset;


-- ============================================================
-- 27. SUPPLIER LEAD-TIME ANALYSIS
-- Purpose: Identify suppliers with the longest average
--          lead times and compare their business performance
-- ============================================================

SELECT
    Supplier_ID,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time_days,

    SUM(Order_Quantity) AS total_order_quantity,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit

FROM supply_chain_dataset

GROUP BY Supplier_ID

ORDER BY avg_lead_time_days DESC;


-- ============================================================
-- 28. SKU PERFORMANCE ANALYSIS
-- Purpose: Identify top-performing SKUs by sales, revenue,
--          profit, and average inventory
-- ============================================================

SELECT
    SKU_ID,

    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory

FROM supply_chain_dataset

GROUP BY SKU_ID

ORDER BY revenue DESC

LIMIT 10;


-- ============================================================
-- 29. SKU PROFIT MARGIN ANALYSIS
-- Purpose: Identify SKUs with the highest profit margins
-- ============================================================

SELECT
    SKU_ID,

    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        100.0 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ) / SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY SKU_ID

ORDER BY profit_margin_pct DESC

LIMIT 10;


-- ============================================================
-- 30. PROMOTION PERFORMANCE ANALYSIS
-- Purpose: Compare sales and profitability during promotions
-- ============================================================

SELECT
    Promotion_Flag,

    COUNT(*) AS total_records,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        100.0 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ) / SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY Promotion_Flag

ORDER BY Promotion_Flag;


-- ============================================================
-- 31. PROMOTION PERFORMANCE BY REGION
-- Purpose: Compare promotional performance across regions
-- ============================================================

SELECT
    Region,
    Promotion_Flag,

    COUNT(*) AS total_records,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        100.0 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ) / SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY Region, Promotion_Flag

ORDER BY Region, Promotion_Flag;


-- ============================================================
-- 32. MONTHLY SALES PERFORMANCE
-- Purpose: Analyze monthly sales, revenue, profit, and margin
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        100.0 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ) / SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY YEAR(Date), MONTH(Date)

ORDER BY year, month;

-- ============================================================
-- 33. MONTHLY PERFORMANCE BY REGION
-- Purpose: Compare monthly sales and profit across regions
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    Region,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        100.0 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ) / SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    MONTH(Date),
    Region

ORDER BY
    year,
    month,
    Region;
    
    
    -- ============================================================
-- 34. WAREHOUSE MONTHLY PERFORMANCE
-- Purpose: Compare warehouse performance month by month
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    Warehouse_ID,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    MONTH(Date),
    Warehouse_ID

ORDER BY
    year,
    month,
    Warehouse_ID;
    
    
    -- ============================================================
-- 35. SUPPLIER MONTHLY PERFORMANCE
-- Purpose: Compare supplier performance month by month
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    Supplier_ID,

    SUM(Order_Quantity) AS total_order_quantity,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time_days

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    MONTH(Date),
    Supplier_ID

ORDER BY
    year,
    month,
    Supplier_ID;
    
    
    -- ============================================================
-- 36. REGIONAL MONTHLY PERFORMANCE
-- Purpose: Compare regional performance month by month
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    Region,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        100.0 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ) / SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    MONTH(Date),
    Region

ORDER BY
    year,
    month,
    Region;
    
    
    -- ============================================================
-- 37. WAREHOUSE MONTHLY PERFORMANCE
-- Purpose: Compare warehouse performance month by month
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    Warehouse_ID,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    MONTH(Date),
    Warehouse_ID

ORDER BY
    year,
    month,
    Warehouse_ID;
    
    
    -- ============================================================
-- 38. SUPPLIER MONTHLY PERFORMANCE
-- Purpose: Compare supplier performance month by month
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    Supplier_ID,

    SUM(Order_Quantity) AS total_order_quantity,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time_days

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    MONTH(Date),
    Supplier_ID

ORDER BY
    year,
    month,
    Supplier_ID;
    
    
    -- ============================================================
-- 39. SKU MONTHLY PERFORMANCE
-- Purpose: Compare SKU performance month by month
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    SKU_ID,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    MONTH(Date),
    SKU_ID

ORDER BY
    year,
    month,
    SKU_ID;
    
    -- ============================================================
-- 40. SUPPLIER YEARLY PERFORMANCE
-- Purpose: Compare supplier performance year by year
-- ============================================================

SELECT
    YEAR(Date) AS year,
    Supplier_ID,

    SUM(Order_Quantity) AS total_order_quantity,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time_days

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    Supplier_ID

ORDER BY
    year,
    Supplier_ID;
    
    -- ============================================================
-- 41. SKU YEARLY PERFORMANCE
-- Purpose: Compare SKU performance year by year
-- ============================================================

SELECT
    YEAR(Date) AS year,
    SKU_ID,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS profit,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory

FROM supply_chain_dataset

GROUP BY
    YEAR(Date),
    SKU_ID

ORDER BY
    year,
    SKU_ID;
    
    
-- ============================================================
-- 42. FINAL KPI SUMMARY
-- Purpose: Create a single executive-level KPI summary
-- ============================================================

SELECT
    COUNT(*) AS total_records,

    COUNT(DISTINCT SKU_ID) AS total_skus,

    COUNT(DISTINCT Warehouse_ID) AS total_warehouses,

    COUNT(DISTINCT Supplier_ID) AS total_suppliers,

    COUNT(DISTINCT Region) AS total_regions,

    MIN(Date) AS start_date,

    MAX(Date) AS end_date,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS total_profit,

    ROUND(
        100.0 * SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ) / SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct,

    ROUND(
        AVG(Inventory_Level),
        2
    ) AS avg_inventory,

    ROUND(
        AVG(Supplier_Lead_Time_Days),
        2
    ) AS avg_lead_time_days,

    SUM(Stockout_Flag) AS total_stockout_days

FROM supply_chain_dataset;


-- ============================================================
-- SUPPLY CHAIN ANALYSIS
-- SQL BUSINESS ANALYSIS PROJECT
-- ============================================================


-- ============================================================
-- 01. DATABASE SETUP
-- ============================================================

CREATE DATABASE IF NOT EXISTS supply_chain_analysis;

USE supply_chain_analysis;


-- ============================================================
-- 02. TABLE CREATION
-- ============================================================

DROP TABLE IF EXISTS supply_chain_dataset;

CREATE TABLE supply_chain_dataset (
    Date DATETIME,
    SKU_ID VARCHAR(20),
    Warehouse_ID VARCHAR(20),
    Supplier_ID VARCHAR(20),
    Region VARCHAR(30),
    Units_Sold INT,
    Inventory_Level INT,
    Supplier_Lead_Time_Days INT,
    Reorder_Point INT,
    Order_Quantity INT,
    Unit_Cost DOUBLE,
    Unit_Price DOUBLE,
    Promotion_Flag INT,
    Stockout_Flag INT,
    Demand_Forecast DOUBLE
);


-- ============================================================
-- 03. DATA IMPORT
-- ============================================================

LOAD DATA LOCAL INFILE
'/Users/sayoojchandran/Desktop/Supply Chain Analysis/supply_chain_dataset.csv'
INTO TABLE supply_chain_dataset
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- ============================================================
-- 04. DATA VALIDATION
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM supply_chain_dataset;


SELECT *
FROM supply_chain_dataset
LIMIT 10;


-- ============================================================
-- 05. DATASET OVERVIEW
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT SKU_ID) AS total_skus,
    COUNT(DISTINCT Warehouse_ID) AS total_warehouses,
    COUNT(DISTINCT Supplier_ID) AS total_suppliers,
    COUNT(DISTINCT Region) AS total_regions,
    MIN(Date) AS start_date,
    MAX(Date) AS end_date
FROM supply_chain_dataset;


-- ============================================================
-- 06. DATA QUALITY - MISSING VALUES
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    SUM(Date IS NULL) AS missing_date,
    SUM(SKU_ID IS NULL) AS missing_sku,
    SUM(Warehouse_ID IS NULL) AS missing_warehouse,
    SUM(Supplier_ID IS NULL) AS missing_supplier,
    SUM(Region IS NULL) AS missing_region,
    SUM(Units_Sold IS NULL) AS missing_units_sold,
    SUM(Inventory_Level IS NULL) AS missing_inventory,
    SUM(Unit_Cost IS NULL) AS missing_unit_cost,
    SUM(Unit_Price IS NULL) AS missing_unit_price,
    SUM(Demand_Forecast IS NULL) AS missing_forecast
FROM supply_chain_dataset;


-- ============================================================
-- 07. DUPLICATE CHECK
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT Date, SKU_ID, Warehouse_ID, Supplier_ID)
        AS unique_records,
    COUNT(*) -
    COUNT(DISTINCT Date, SKU_ID, Warehouse_ID, Supplier_ID)
        AS duplicate_records
FROM supply_chain_dataset;


-- ============================================================
-- 08. OVERALL BUSINESS KPIs
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS total_revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS total_profit,

    ROUND(
        100.0 *
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        )
        /
        SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct,

    ROUND(AVG(Inventory_Level), 2)
        AS avg_inventory,

    ROUND(AVG(Supplier_Lead_Time_Days), 2)
        AS avg_lead_time_days,

    SUM(Stockout_Flag)
        AS total_stockout_days

FROM supply_chain_dataset;


-- ============================================================
-- 09. MONTHLY PERFORMANCE
-- ============================================================

SELECT
    YEAR(Date) AS year,
    MONTH(Date) AS month,
    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS profit

FROM supply_chain_dataset

GROUP BY YEAR(Date), MONTH(Date)

ORDER BY year, month;


-- ============================================================
-- 10. REGIONAL PERFORMANCE
-- ============================================================

SELECT
    Region,
    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS profit,

    ROUND(AVG(Inventory_Level), 2)
        AS avg_inventory

FROM supply_chain_dataset

GROUP BY Region

ORDER BY revenue DESC;


-- ============================================================
-- 11. WAREHOUSE PERFORMANCE
-- ============================================================

SELECT
    Warehouse_ID,
    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS profit,

    ROUND(AVG(Inventory_Level), 2)
        AS avg_inventory

FROM supply_chain_dataset

GROUP BY Warehouse_ID

ORDER BY revenue DESC;


-- ============================================================
-- 12. SUPPLIER PERFORMANCE
-- ============================================================

SELECT
    Supplier_ID,

    ROUND(
        AVG(Supplier_Lead_Time_Days), 2
    ) AS avg_lead_time_days,

    SUM(Order_Quantity)
        AS total_order_quantity,

    SUM(Units_Sold)
        AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS profit

FROM supply_chain_dataset

GROUP BY Supplier_ID

ORDER BY revenue DESC;


-- ============================================================
-- 13. SKU PERFORMANCE
-- ============================================================

SELECT
    SKU_ID,
    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS profit,

    ROUND(AVG(Inventory_Level), 2)
        AS avg_inventory

FROM supply_chain_dataset

GROUP BY SKU_ID

ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 14. SKU PROFIT MARGIN
-- ============================================================

SELECT
    SKU_ID,
    SUM(Units_Sold) AS units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS profit,

    ROUND(
        100.0 *
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        )
        /
        SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct

FROM supply_chain_dataset

GROUP BY SKU_ID

ORDER BY profit_margin_pct DESC
LIMIT 10;


-- ============================================================
-- 15. INVENTORY BUFFER ANALYSIS
-- ============================================================

SELECT
    Warehouse_ID,
    SKU_ID,

    ROUND(AVG(Inventory_Level), 2)
        AS avg_inventory,

    ROUND(AVG(Reorder_Point), 2)
        AS avg_reorder_point,

    ROUND(
        AVG(Inventory_Level - Reorder_Point),
        2
    ) AS avg_inventory_buffer

FROM supply_chain_dataset

GROUP BY Warehouse_ID, SKU_ID

ORDER BY avg_inventory_buffer DESC

LIMIT 10;


-- ============================================================
-- 16. REORDER-POINT RISK
-- ============================================================

SELECT
    Warehouse_ID,
    SKU_ID,

    COUNT(*) AS total_days,

    SUM(
        Inventory_Level < Reorder_Point
    ) AS days_below_reorder_point,

    ROUND(
        100.0 *
        SUM(Inventory_Level < Reorder_Point)
        /
        COUNT(*),
        2
    ) AS pct_days_below_reorder_point

FROM supply_chain_dataset

GROUP BY Warehouse_ID, SKU_ID

ORDER BY pct_days_below_reorder_point DESC

LIMIT 10;


-- ============================================================
-- 17. STOCKOUT ANALYSIS
-- ============================================================

SELECT
    SUM(Stockout_Flag)
        AS total_stockout_days,

    COUNT(*) AS total_records,

    ROUND(
        100.0 *
        SUM(Stockout_Flag)
        /
        COUNT(*),
        2
    ) AS stockout_rate_pct

FROM supply_chain_dataset;


-- ============================================================
-- 18. PROMOTION PERFORMANCE
-- ============================================================

SELECT
    Promotion_Flag,
    COUNT(*) AS total_records,

    SUM(Units_Sold)
        AS total_units_sold,

    ROUND(AVG(Units_Sold), 2)
        AS avg_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price), 2
    ) AS revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ), 2
    ) AS profit

FROM supply_chain_dataset

GROUP BY Promotion_Flag

ORDER BY Promotion_Flag;


-- ============================================================
-- 19. FORECAST ACCURACY
-- ============================================================

SELECT
    ROUND(
        AVG(
            ABS(
                Units_Sold - Demand_Forecast
            )
        ),
        2
    ) AS MAE,

    ROUND(
        AVG(
            ABS(
                Units_Sold - Demand_Forecast
            )
            /
            NULLIF(Units_Sold, 0)
        ) * 100,
        2
    ) AS MAPE

FROM supply_chain_dataset;


-- ============================================================
-- 20. FINAL KPI SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT SKU_ID) AS total_skus,
    COUNT(DISTINCT Warehouse_ID) AS total_warehouses,
    COUNT(DISTINCT Supplier_ID) AS total_suppliers,
    COUNT(DISTINCT Region) AS total_regions,

    MIN(Date) AS start_date,
    MAX(Date) AS end_date,

    SUM(Units_Sold) AS total_units_sold,

    ROUND(
        SUM(Units_Sold * Unit_Price),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        ),
        2
    ) AS total_profit,

    ROUND(
        100.0 *
        SUM(
            Units_Sold * (Unit_Price - Unit_Cost)
        )
        /
        SUM(Units_Sold * Unit_Price),
        2
    ) AS profit_margin_pct,

    ROUND(AVG(Inventory_Level), 2)
        AS avg_inventory,

    ROUND(AVG(Supplier_Lead_Time_Days), 2)
        AS avg_lead_time_days,

    SUM(Stockout_Flag)
        AS total_stockout_days

FROM supply_chain_dataset;



    
    
    
    
    
    



