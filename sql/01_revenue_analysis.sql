
-- Customer Revenue Intelligence Platform
-- Phase 1: Revenue and Sales Analysis

-- 1. Overall sales KPIs
SELECT
    COUNT(*) AS total_source_rows,
    COUNT(*) FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_sales_rows,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS invoices_with_eligible_sales,
    COUNT(DISTINCT "CustomerID") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS identifiable_customers,
    ROUND(
        SUM("PositiveSalesValue")::numeric, 2
    ) AS provisional_positive_sales
FROM retail.transactions;


-- 2. Monthly sales trend
SELECT
    DATE_TRUNC('month', "InvoiceDate")::date AS sales_month,
    ROUND(SUM("PositiveSalesValue")::numeric, 2) AS provisional_sales,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_invoices,
    COUNT(DISTINCT "CustomerID") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS identifiable_customers
FROM retail.transactions
GROUP BY 1
ORDER BY 1;


-- 3. Top 10 products by provisional positive sales
SELECT
    "StockCode",
    "Description",
    ROUND(SUM("PositiveSalesValue")::numeric, 2) AS provisional_sales,
    SUM("Quantity") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS units_sold
FROM retail.transactions
GROUP BY "StockCode", "Description"
HAVING SUM("PositiveSalesValue") > 0
ORDER BY provisional_sales DESC
LIMIT 10;


-- 4. Top 10 countries by provisional positive sales
SELECT
    "Country",
    ROUND(SUM("PositiveSalesValue")::numeric, 2) AS provisional_sales,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_invoices,
    COUNT(DISTINCT "CustomerID") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS identifiable_customers
FROM retail.transactions
GROUP BY "Country"
HAVING SUM("PositiveSalesValue") > 0
ORDER BY provisional_sales DESC
LIMIT 10;


-- 5. Customer-level sales summary
SELECT
    "CustomerID",
    ROUND(SUM("PositiveSalesValue")::numeric, 2) AS provisional_sales,
    COUNT(DISTINCT "InvoiceNo") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS eligible_invoices,
    SUM("Quantity") FILTER (
        WHERE "EligiblePositiveSales" = TRUE
    ) AS units_purchased
FROM retail.transactions
WHERE "CustomerID" IS NOT NULL
GROUP BY "CustomerID"
HAVING SUM("PositiveSalesValue") > 0
ORDER BY provisional_sales DESC
LIMIT 20;
