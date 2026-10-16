
# Customer Revenue Intelligence Platform

## 1. Business Context

Retail businesses generate transaction data containing information about
orders, products, customers, prices, quantities, and purchase dates.

However, transaction records alone do not automatically explain which
products drive sales, how customer purchasing behavior changes over time,
or which previously active customers deserve further investigation.

This project develops an end-to-end analytics workflow that converts
retail transaction records into validated business metrics and
decision-support outputs.

## 2. Problem Statement

Build a reproducible analytics platform that identifies revenue patterns,
customer purchasing behavior, repeat purchasing, cohort retention, and
customer inactivity using transaction-level retail data.

The platform should enable analysts and business stakeholders to identify
important patterns, investigate potential retention opportunities, and
evaluate hypothetical intervention scenarios.

The available data does not establish why customers stop purchasing.
Inactivity must not be treated as confirmed churn.

## 3. Business Objectives

1. Measure historical sales performance over time.
2. Identify high-performing products and geographic markets.
3. Understand customer spending and purchasing frequency.
4. Measure repeat purchasing and observed cohort retention.
5. Identify customers who have not purchased within a defined period.
6. Quantify historical revenue associated with relevant customer groups.
7. Support transparent, assumption-based retention scenarios.
8. Deliver validated results through SQL, Python, and Power BI.

## 4. Stakeholders

- Business managers: understand sales performance and business priorities.
- Sales analysts: investigate product and geographic performance.
- Customer relationship teams: investigate customer inactivity and
  potential retention opportunities.
- Data analysts: validate metrics, investigate patterns, and communicate
  evidence-based findings.
- BI developers: maintain the analytical model and reporting layer.

These are intended stakeholder groups, not confirmed users of an
existing business system.

## 5. Business Questions

### Revenue and Products

- How does sales revenue change monthly?
- Which products contribute most to historical sales?
- Which countries generate the greatest sales value?
- How concentrated is revenue among top products?
- How do returns and cancellations affect reported sales?

### Customer Behavior

- How many customers have identifiable transaction histories?
- What proportion of identified customers purchase more than once?
- How frequently do customers purchase?
- Which customers have the highest historical monetary value?
- How does purchasing activity differ across customer groups?

### Retention

- How many customers return after their first observed purchase month?
- How does observed cohort retention change over time?
- Which previously active customers have become inactive under a
  documented threshold?
- How much historical revenue is associated with those customers?
- Which segments merit further investigation?

### Decision Support

- How do hypothetical retention rates affect scenario outcomes?
- What happens when the number of contacted customers changes?
- How do assumed revenue and contact costs affect estimated net
  contribution?
- Which assumptions need evidence before an intervention is attempted?

## 6. Dataset Overview

Primary dataset: UCI Online Retail.

Source:
https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains transaction-level records for a UK-based,
non-store online retailer. The published observation period is
December 2010 through December 2011.

The source fields include:

- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

The dataset includes transaction identifiers that indicate cancellations,
negative quantities associated with returns or adjustments, and potentially
missing customer identifiers. Their actual frequency and treatment must
be determined during data inspection.

The business represented by the dataset is historical. The analysis
does not describe a current retailer's performance.

## 7. Proposed Analytical Approach

1. Inspect the original data and document data-quality issues.
2. Develop reproducible Python cleaning functions.
3. Preserve raw records and document excluded or transformed records.
4. Load source and analytical data into PostgreSQL.
5. Implement validated SQL views and analytical queries.
6. Reproduce important metrics in Python.
7. Analyze revenue, customers, cohorts, RFM segments, and inactivity.
8. Reconcile key results across analytical layers.
9. Build four Power BI report pages.
10. Develop a Streamlit simulator for hypothetical retention scenarios.
11. Publish verified findings, limitations, and recommendations.

## 8. Expected Deliverables

- Business requirements and metric dictionary.
- Data dictionary and data-quality report.
- Reusable Python data-processing pipeline.
- PostgreSQL schema and SQL analytics.
- Exploratory and customer analytics notebooks.
- Automated tests and reconciliation checks.
- Four-page Power BI report.
- Interactive Streamlit retention simulator.
- Executive summary and evidence-based findings report.
- Reproducible GitHub repository and README.
- Resume bullets and technical interview preparation material.

## 9. Scope Exclusions

Unless suitable additional data becomes available, this project does not
claim to measure:

- Product profit or gross margin.
- Customer acquisition cost.
- Marketing campaign effectiveness.
- Actual intervention costs or campaign ROI.
- Confirmed customer churn.
- Actual retention improvement caused by a campaign.
- Future customer behavior with proven predictive accuracy.

A predictive model is optional and must be justified by a valid
time-based prediction design.

## 10. Risks and Limitations

- Missing customer identifiers limit customer-level analysis.
- Cancellation and return records require explicit treatment.
- Duplicate-looking records may represent legitimate transaction lines.
- The dataset covers a limited historical observation period.
- The final observed month may be incomplete.
- First observed purchase is not necessarily the customer's true
  acquisition date.
- Inactivity does not establish the reason for reduced purchasing.
- Revenue is not equivalent to profit.
- Historical associations do not establish causal impact.
- Simulated retention outcomes depend on user-supplied assumptions.

## 11. Assumptions Requiring Validation

- InvoiceNo identifies an invoice or purchase occasion, subject to
  cancellation handling and data-quality checks.
- InvoiceDate can be parsed consistently.
- UnitPrice and Quantity can be converted to appropriate numeric types.
- Positive quantities on eligible, non-cancelled invoices represent
  candidate sales lines, subject to validation.
- Negative quantities require separate return or adjustment analysis.
- Customer-level metrics require valid CustomerID values.
- The reference date for recency will be derived consistently from
  the observed data.
- Retention cohorts will use each identified customer's first observed
  eligible purchase month.
- RFM frequency will count distinct eligible purchase invoices.
- Inactivity thresholds are analytical rules, not confirmed churn labels.
- Simulator outputs are hypothetical, not observed business outcomes.

## 12. Definition of Success

The project is successful when its documented workflow can be reproduced,
its major metrics pass validation, its analytical outputs reconcile across
Python and PostgreSQL, and its Power BI measures agree with the chosen
metric definitions.

Every business finding must be supported by calculated results.

No unverified business impact, model performance, or intervention outcome
will be presented as fact.
