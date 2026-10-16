
-- Customer Revenue Intelligence Platform
-- Phase 2: Customer Analysis

-- 1. Customer purchase frequency and value
WITH customer_metrics AS (
    SELECT
        "CustomerID",
        SUM("PositiveSalesValue") AS customer_sales,
        COUNT(DISTINCT "InvoiceNo") FILTER (
            WHERE "EligiblePositiveSales" = TRUE
        ) AS invoice_count,
        MIN("InvoiceDate") FILTER (
            WHERE "EligiblePositiveSales" = TRUE
        ) AS first_purchase,
        MAX("InvoiceDate") FILTER (
            WHERE "EligiblePositiveSales" = TRUE
        ) AS last_purchase
    FROM retail.transactions
    WHERE "CustomerID" IS NOT NULL
    GROUP BY "CustomerID"
    HAVING SUM("PositiveSalesValue") > 0
)
SELECT
    "CustomerID",
    ROUND(customer_sales::numeric, 2) AS customer_sales,
    invoice_count,
    first_purchase,
    last_purchase,
    CASE
        WHEN invoice_count = 1 THEN 'One-time purchaser'
        WHEN invoice_count BETWEEN 2 AND 5 THEN 'Occasional purchaser'
        ELSE 'Repeat purchaser'
    END AS purchase_segment
FROM customer_metrics
ORDER BY customer_sales DESC
LIMIT 25;


-- 2. Distribution of customers by purchase frequency

WITH customer_frequency AS (
    SELECT
        "CustomerID",
        COUNT(DISTINCT "InvoiceNo") FILTER (
            WHERE "EligiblePositiveSales" = TRUE
        ) AS invoice_count
    FROM retail.transactions
    WHERE "CustomerID" IS NOT NULL
    GROUP BY "CustomerID"
    HAVING SUM("PositiveSalesValue") > 0
),
segmented_customers AS (
    SELECT
        CASE
            WHEN invoice_count = 1 THEN '1 invoice'
            WHEN invoice_count BETWEEN 2 AND 5 THEN '2-5 invoices'
            WHEN invoice_count BETWEEN 6 AND 10 THEN '6-10 invoices'
            ELSE '11+ invoices'
        END AS purchase_frequency_segment,
        CASE
            WHEN invoice_count = 1 THEN 1
            WHEN invoice_count BETWEEN 2 AND 5 THEN 2
            WHEN invoice_count BETWEEN 6 AND 10 THEN 3
            ELSE 4
        END AS segment_order
    FROM customer_frequency
)
SELECT
    purchase_frequency_segment,
    COUNT(*) AS customers
FROM segmented_customers
GROUP BY purchase_frequency_segment, segment_order
ORDER BY segment_order;


-- 3. Repeat-customer sales contribution

WITH customer_metrics AS (
    SELECT
        "CustomerID",
        SUM("PositiveSalesValue") AS customer_sales,
        COUNT(DISTINCT "InvoiceNo") FILTER (
            WHERE "EligiblePositiveSales" = TRUE
        ) AS invoice_count
    FROM retail.transactions
    WHERE "CustomerID" IS NOT NULL
    GROUP BY "CustomerID"
    HAVING SUM("PositiveSalesValue") > 0
),
customer_types AS (
    SELECT
        CASE
            WHEN invoice_count = 1 THEN 'One-time purchaser'
            ELSE 'Repeat purchaser'
        END AS customer_type,
        customer_sales
    FROM customer_metrics
)
SELECT
    customer_type,
    COUNT(*) AS customers,
    ROUND(SUM(customer_sales)::numeric, 2) AS provisional_sales,
    ROUND(
        (
            100.0 * SUM(customer_sales)
            / NULLIF(SUM(SUM(customer_sales)) OVER (), 0)
        )::numeric,
        2
    ) AS sales_share_pct
FROM customer_types
GROUP BY customer_type
ORDER BY provisional_sales DESC;
