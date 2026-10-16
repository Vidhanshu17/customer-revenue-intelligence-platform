
# Data Quality Report

## 1. Dataset Summary

- Source: UCI Online Retail
- Total records: 541,909
- Total columns: 8
- Observation start: 2010-12-01 08:26:00
- Observation end: 2011-12-09 12:50:00
- Invalid invoice dates: 0

## 2. Identified Data-Quality Issues

| Issue | Affected records | Detection method | Business impact | Proposed treatment | Final treatment |
|---|---:|---|---|---|---|
| Missing CustomerID | 135,080 | Null count | Limits customer-level analysis | Preserve records; exclude from customer-level calculations | Pending validation |
| Missing Description | 1,454 | Null count | Product descriptions may be unavailable | Preserve StockCode and investigate | Pending validation |
| Exact duplicate rows | 5,268 | Exact-row duplicate check | May inflate totals if duplicated records are removed incorrectly or counted twice | Investigate before deduplication | Pending validation |
| Negative quantities | 10,624 | Quantity < 0 | May represent returns or adjustments | Analyze separately from positive sales | Pending validation |
| Cancellation-marked rows | 9,288 | InvoiceNo begins with C | May represent cancelled transactions | Investigate invoice-level patterns | Pending validation |
| Zero unit prices | 2,515 | UnitPrice = 0 | Can distort pricing analysis | Inspect records and their descriptions | Pending validation |
| Negative unit prices | 2 | UnitPrice < 0 | May represent unusual adjustments | Inspect individual records | Pending validation |
| Invalid invoice dates | 0 | Date parsing failures | Could affect time-series analysis | No action indicated by initial inspection | No invalid dates detected |

## 3. Important Observations

1. CustomerID is missing from approximately 24.93% of records.
2. InvoiceDate was parsed without invalid dates.
3. Negative quantities and cancellation indicators may overlap.
4. Duplicate records require investigation before any removal.
5. The observation period ends on December 9, 2011, so the final
   calendar month is incomplete.
6. The initial inspection does not establish the meaning of every
   unusual transaction.

## 4. Limitations

This is an initial profiling report, not a completed cleaning report.

The proposed treatments have not yet been validated against the
underlying records.

No rows have been removed or altered as part of this initial inspection.

## 5. Next Actions

- Inspect duplicate transaction rows.
- Inspect negative-price and zero-price records.
- Examine cancellation invoices and negative quantities together.
- Define documented cleaning rules.
- Implement cleaning functions and automated tests.
- Reconcile source and cleaned record counts.
