
# Metric Dictionary

## 1. General Conventions

- Transaction-line value = Quantity * UnitPrice.
- Preserve the original invoice identifier and source values.
- Treat cancellation invoices separately from eligible purchase invoices.
- Analyze negative-quantity lines as returns or adjustments until their
  meaning has been validated.
- Customer-level metrics require a valid CustomerID.
- Use one documented observation window and reference date.
- Do not describe historical revenue as profit.
- Do not label inactive customers as confirmed churned customers.

## 2. Sales and Transaction Metrics

### Gross sales

Sum of positive line values from eligible, non-cancelled purchase
invoices.

Formula:
SUM(Quantity * UnitPrice)

Eligibility requires a positive quantity, a positive unit price,
and an invoice that passes the documented cancellation policy.

### Returns and adjustments

Report negative-quantity lines separately using their absolute value
for a positive presentation of the associated return or adjustment value.

Do not automatically assume every negative line is a confirmed refund.

### Cancellations

Count distinct invoice identifiers identified as cancellations.
Report cancellation-associated line values separately from eligible
purchase sales.

### Net sales

For this project, net sales means eligible positive sales value less
eligible negative-quantity return or adjustment value.

Formula:
Eligible positive sales value + eligible negative line value

This is an analytical net-sales measure, not accounting-recognized
revenue. Reconcile cancellation and adjustment treatment before
finalizing the implementation.

### Invoice count

Count distinct eligible, non-cancelled purchase invoice identifiers
within the selected period.

This is not the number of transaction lines.

### Average order value

Eligible positive sales value divided by distinct eligible purchase
invoices in the same period.

This definition excludes returns from the numerator. Net sales and
average order value must therefore be reported as separate measures.

### Distinct identified customers

Count distinct non-null, valid CustomerID values among eligible
purchase records within the stated observation window.

### Revenue by product or country

Sum eligible positive line values grouped by product or country.
Show returns and adjustments separately where relevant.

### Revenue concentration

Revenue from the selected top products divided by total eligible
positive sales value for the same period.

## 3. Customer Metrics

### Repeat-customer rate

Identified customers with at least two distinct eligible purchase
invoices divided by identified customers with at least one eligible
purchase invoice.

Report as a percentage.

### Purchase frequency

Number of distinct eligible purchase invoices per identified customer
during the defined observation window.

Do not count invoice lines as separate purchases.

### Recency

Number of calendar days between the customer's most recent eligible
purchase date and the selected reference date.

The reference date must be after the latest eligible purchase date.
Recency must be nonnegative.

### Frequency (RFM)

Number of distinct eligible purchase invoices per customer within the
RFM observation window.

### Monetary value (RFM)

Sum of eligible positive sales line values per customer within the
RFM observation window.

This definition uses positive historical sales, not profit.

### First-time versus returning customer revenue

Classify eligible purchase invoices using the customer's first observed
eligible purchase date.

Document the rule for identifying first-time invoices and ensure that
the calculation is consistent across SQL and Python.

## 4. Cohort Metrics

### Customer cohort

Calendar month of a customer's first observed eligible purchase.

This may differ from the true acquisition month because the dataset
does not necessarily contain the customer's entire history.

### Cohort retention

Customers from a cohort with at least one eligible purchase in a
subsequent cohort-relative month, divided by the original cohort size.

Cohort month 0 represents the first observed purchase month.

Report incomplete observation periods and the final partial month
explicitly.

## 5. Inactivity Metrics

### Inactive customer count

Number of identified customers whose most recent eligible purchase
occurred more than the selected inactivity threshold before the
reference date.

Test thresholds of 60, 90, and 120 days where supported by the data.

### Revenue associated with inactive customers

Eligible positive historical sales associated with the customers
classified as inactive, over an explicitly stated historical period.

This is historical revenue, not estimated future revenue or revenue
that would necessarily be lost.

## 6. Retention Simulator Metrics

### Estimated customers retained

Customers targeted * assumed incremental retention rate.

### Estimated revenue preserved

Estimated customers retained * assumed revenue per retained customer
over the stated period.

### Estimated intervention cost

Customers targeted * assumed cost per customer contacted.

### Estimated net contribution

Estimated revenue preserved - estimated intervention cost.

### Revenue-to-cost ratio

Estimated revenue preserved / estimated intervention cost, when
intervention cost is greater than zero.

This is a hypothetical scenario ratio, not a verified campaign ROI.

## 7. Consistency Requirements

- Use the same eligible-sales definition in SQL, Python, and Power BI.
- Use the same observation window for compared customer metrics.
- Count distinct invoices for purchase frequency.
- Keep cancellations and returns separately identifiable.
- Document all exclusions and assumptions.
- Reconcile important metrics before publishing results.
- Never substitute simulated outcomes for observed findings.
