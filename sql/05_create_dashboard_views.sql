
-- Customer Revenue Intelligence Platform
-- Phase 4: Reusable dashboard views

CREATE SCHEMA IF NOT EXISTS analytics;


-- 1. Overall business KPIs
CREATE OR REPLACE VIEW analytics.vw_sales_kpis AS
SELECT
    COUNT(*) AS total_source_rows,
    COUNT(*) FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_sales_rows,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_invoices,
    COUNT(DISTINCT "CustomerID") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS identifiable_customers,
    ROUND(
        SUM("PositiveSalesValue")::numeric, 2
    ) AS provisional_positive_sales
FROM retail.transactions;


-- 2. Monthly sales trend
CREATE OR REPLACE VIEW analytics.vw_monthly_sales AS
SELECT
    DATE_TRUNC('month', "InvoiceDate")::date AS sales_month,
    ROUND(
        SUM("PositiveSalesValue")::numeric, 2
    ) AS provisional_sales,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_invoices,
    COUNT(DISTINCT "CustomerID") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS identifiable_customers
FROM retail.transactions
GROUP BY 1;


-- 3. Country-level performance
CREATE OR REPLACE VIEW analytics.vw_country_sales AS
SELECT
    "Country",
    ROUND(
        SUM("PositiveSalesValue")::numeric, 2
    ) AS provisional_sales,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_invoices,
    COUNT(DISTINCT "CustomerID") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS identifiable_customers
FROM retail.transactions
GROUP BY "Country";


-- 4. Product-level performance
CREATE OR REPLACE VIEW analytics.vw_product_sales AS
SELECT
    "StockCode",
    "Description",
    ROUND(
        SUM("PositiveSalesValue")::numeric, 2
    ) AS provisional_sales,
    SUM("Quantity") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS units_sold
FROM retail.transactions
GROUP BY "StockCode", "Description";


-- 5. Customer-level performance
CREATE OR REPLACE VIEW analytics.vw_customer_sales AS
SELECT
    "CustomerID",
    ROUND(
        SUM("PositiveSalesValue")::numeric, 2
    ) AS provisional_sales,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_invoices,
    SUM("Quantity") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS units_purchased,
    MIN("InvoiceDate") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS first_purchase,
    MAX("InvoiceDate") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS last_purchase
FROM retail.transactions
WHERE "CustomerID" IS NOT NULL
GROUP BY "CustomerID";
