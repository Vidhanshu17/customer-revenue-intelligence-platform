
WITH reference_date AS (
    SELECT MAX("InvoiceDate")::date + 1 AS analysis_date
    FROM retail.transactions
),
customer_rfm AS (
    SELECT
        t."CustomerID",
        (SELECT analysis_date FROM reference_date)
            - MAX(t."InvoiceDate")::date AS recency_days,
        COUNT(DISTINCT t."InvoiceNo") FILTER (
            WHERE t."EligiblePositiveSales" = TRUE
        ) AS frequency,
        SUM(t."PositiveSalesValue") AS monetary_value
    FROM retail.transactions t
    WHERE t."CustomerID" IS NOT NULL
    GROUP BY t."CustomerID"
    HAVING SUM(t."PositiveSalesValue") > 0
),
rfm_scores AS (
    SELECT
        *,
        NTILE(5) OVER (
            ORDER BY recency_days DESC
        ) AS recency_score,
        NTILE(5) OVER (
            ORDER BY frequency ASC
        ) AS frequency_score,
        NTILE(5) OVER (
            ORDER BY monetary_value ASC
        ) AS monetary_score
    FROM customer_rfm
),
segmented AS (
    SELECT
        *,
        CASE
            WHEN recency_score >= 4
             AND frequency_score >= 4
             AND monetary_score >= 4
                THEN 'Champions'
            WHEN recency_score >= 3
             AND frequency_score >= 3
                THEN 'Loyal Customers'
            WHEN recency_score >= 4
             AND frequency_score <= 2
                THEN 'Recent Customers'
            WHEN recency_score <= 2
             AND frequency_score >= 3
                THEN 'At Risk'
            WHEN recency_score <= 2
             AND frequency_score <= 2
                THEN 'Needs Attention'
            ELSE 'Potential Loyalists'
        END AS customer_segment
    FROM rfm_scores
)
SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(monetary_value)::numeric, 2)
        AS provisional_sales,
    ROUND(
        (
            100.0 * COUNT(*)
            / SUM(COUNT(*)) OVER ()
        )::numeric,
        2
    ) AS customer_share_pct
FROM segmented
GROUP BY customer_segment
ORDER BY customers DESC;
