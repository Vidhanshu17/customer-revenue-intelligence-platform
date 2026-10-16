
# Customer Revenue Intelligence Platform

**An end-to-end retail analytics project using Python, PostgreSQL, SQL, and Power BI to transform raw transaction data into actionable business insights.**

---

## Overview

The Customer Revenue Intelligence Platform is an end-to-end business intelligence project designed to analyze retail transactions, understand customer purchasing behavior, identify high-performing products and markets, and support data-driven business decisions.

The project combines Python-based data profiling and quality checks, PostgreSQL for analytical data storage and SQL transformations, and Power BI for interactive business reporting.

Rather than treating retail data as a simple visualization exercise, this project emphasizes data quality, transparent cleaning decisions, reusable analytical views, and validation of reported metrics.

## Business Objectives

The platform addresses five core business questions:

- **Sales Performance:** How do provisional sales change over time?
- **Geographic Performance:** Which countries contribute the most sales?
- **Product Performance:** Which products and stock codes generate the highest sales?
- **Customer Intelligence:** Which customers contribute the most value?
- **Customer Segmentation:** How do customer groups differ in purchasing behavior and sales contribution?

The goal is to demonstrate how raw transactional data can be transformed into structured analytics that support business reporting and customer-focused decisions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data profiling, cleaning, investigation, and validation |
| Pandas | Data manipulation and transaction processing |
| NumPy | Numerical operations |
| Jupyter Notebook | Exploratory data analysis |
| PostgreSQL | Analytical database and data storage |
| SQL | Aggregations, analytical views, and business metrics |
| SQLAlchemy | Python-to-PostgreSQL connectivity |
| Power BI Desktop | Interactive dashboards and reporting |
| Matplotlib / Seaborn | Data exploration and visualization |
| pytest | Automated testing of data-cleaning logic |
| Git / GitHub | Version control and project documentation |

## Dataset

This project uses the **UCI Online Retail dataset**, containing transactional records from a UK-based online retailer.

**Dataset source:** [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains invoice numbers, stock codes, product descriptions, quantities, invoice timestamps, unit prices, customer identifiers, and countries.

### Initial Dataset Profile

| Attribute | Value |
|---|---:|
| Original records | 541,909 |
| Original columns | 8 |
| Distinct invoices | 25,900 |
| Distinct product codes | 4,070 |
| Distinct non-null customer IDs | 4,372 |
| Countries represented | 38 |
| Earliest transaction | December 1, 2010 |
| Latest transaction | December 9, 2011 |

The dataset contains missing values, duplicate records, cancellation invoices, negative quantities, and unusual price entries. These issues require investigation before meaningful sales metrics can be calculated.

> **Data note:** This dataset is used for analytical and educational purposes. Results describe the analyzed historical data and do not represent the retailer's current business performance.

## Project Architecture

The project follows a layered analytical workflow:

1. **Raw Data:** Preserve the original dataset.
2. **Data Profiling:** Inspect missing values, duplicates, dates, quantities, prices, and cancellation patterns.
3. **Record Investigation:** Identify suspicious records and document data-quality issues.
4. **Transaction Classification:** Apply quality flags and provisional sales eligibility rules.
5. **PostgreSQL Analytics:** Store classified transactions and create analytical views.
6. **Power BI Reporting:** Visualize business metrics through interactive dashboards.
7. **Validation:** Compare row counts, classifications, and sales calculations against expected results.

```text
UCI Online Retail Dataset
          |
          v
Python Data Profiling
          |
          v
Record Investigation
          |
          v
Transaction Classification
          |
          v
PostgreSQL Database
          |
          v
SQL Analytical Views
          |
          v
Power BI Dashboards
          |
          v
Business Insights
```

## Data Quality and Preprocessing

The preprocessing pipeline preserves the original transaction rows while classifying records according to explicit quality rules.

### Data Quality Findings

| Data Quality Issue | Records Flagged |
|---|---:|
| Excess exact duplicate rows | 5,268 |
| Cancellation invoice rows | 9,288 |
| Negative quantity rows | 10,624 |
| Zero unit-price rows | 2,515 |
| Negative unit-price rows | 2 |
| Missing customer identifiers | 135,080 |
| Missing product descriptions | 1,454 |

These checks may overlap. Their counts should not be added together to calculate the total number of affected transactions.

### Classification Rules

The preprocessing pipeline:

- Parses invoice dates and numeric transaction fields.
- Identifies cancellation invoices using invoice numbers beginning with `C`.
- Flags negative quantities and zero or negative unit prices.
- Flags missing customer identifiers and product descriptions.
- Identifies excess exact duplicates using the required source columns.
- Calculates transaction line values using quantity multiplied by unit price.
- Marks eligible positive-sales records using documented conditions.
- Preserves excluded records and classification flags for further investigation.

### Provisional Sales Definition

A transaction qualifies as eligible positive sales when it has:

- A positive quantity.
- A positive unit price.
- No cancellation-invoice flag.
- No excess exact-duplicate flag.

The pipeline calculates each line value and includes it in provisional sales only when these conditions are met.

This is an analytical classification rule, not a final accounting policy. Returns, accounting adjustments, and unusual transactions should be reconciled before interpreting the result as official net revenue.

## Data Quality Validation

The preprocessing pipeline was validated against the source data and expected classification behavior.

| Validation Metric | Result |
|---|---:|
| Source rows | 541,909 |
| Classified output rows | 541,909 |
| Eligible positive-sales rows | 524,878 |
| Excess exact duplicates flagged | 5,268 |
| Cancellation rows flagged | 9,288 |
| Provisional positive-sales value | 10,642,110.80 |

The provisional sales value is expressed in the source dataset's price units and is not independently reconciled accounting revenue.

### Automated Testing

- **8 pytest tests passed.**
- **6 pipeline validation checks passed.**

The tests cover row preservation, duplicate classification, positive-sales calculations, cancellation handling, negative quantities, invalid prices, missing customer identifiers, and required columns.

## PostgreSQL Analytics

The classified transaction dataset was loaded into PostgreSQL using Python and SQLAlchemy.

| Configuration | Value |
|---|---|
| Database | `customer_revenue_intelligence` |
| Transaction schema | `retail` |
| Transaction table | `retail.transactions` |
| Analytics schema | `analytics` |
| Expected imported rows | 541,909 |
| Imported columns | 19 |

The imported table was validated against the classified CSV.

### Analytical SQL Views

Six analytical views support reporting in Power BI.

| View | Analytical Purpose |
|---|---|
| `analytics.vw_sales_kpis` | Overall sales and transaction KPIs |
| `analytics.vw_monthly_sales` | Monthly sales trends |
| `analytics.vw_country_sales` | Country-level sales performance |
| `analytics.vw_product_sales` | Product and stock-code performance |
| `analytics.vw_customer_sales` | Customer-level sales metrics |
| `analytics.vw_customer_rfm` | RFM-style customer segmentation |

These views separate reporting logic from dashboard design, allowing analytical results to be inspected and validated directly in PostgreSQL.

## Power BI Dashboard

The Power BI report contains three pages, each designed for a different analytical purpose.

### 1. Executive Overview

Provides a high-level summary of retail performance.

**Key components:**

- Provisional sales KPI.
- Eligible sales rows.
- Eligible invoices.
- Identifiable customers.
- Monthly provisional sales trend.
- Top 10 countries by provisional sales.
- Top 10 products by provisional sales.

The monthly trend shows November 2011 as the highest-sales month among the displayed months.

December 2011 contains only partial-month data and should not be compared directly with complete months.

### 2. Customer Intelligence

Focuses on customer value and purchasing behavior.

**Key components:**

- Customer distribution by RFM segment.
- Provisional sales by customer segment.
- Top customers ranked by provisional sales.
- Customer identifiers.
- Eligible invoice counts.
- Last purchase timestamps.

The RFM-style segmentation identifies groups such as:

- Champions
- Loyal Customers
- At Risk
- Needs Attention
- Potential Loyalists
- Recent Customers

This page demonstrates how customer-level analytics can help prioritize retention efforts and support customer relationship management.

### 3. Product & Geography

Explores geographic and product-level performance.

**Key components:**

- Country count KPI.
- Product-code count KPI.
- Provisional sales KPI.
- Top 10 countries by provisional sales.
- Top 10 products by provisional sales.
- Country-level invoice and identifiable customer details.

The country analysis identifies the United Kingdom as the dominant sales market in the analyzed dataset.

The product ranking includes entries such as postage and manual adjustments. These should be distinguished from ordinary merchandise when interpreting product performance.

## Key Analytical Observations

The validated outputs support the following descriptive observations:

1. **Geographic Concentration:** The United Kingdom contributes the largest share of provisional sales in the country-level results.
2. **Seasonal Pattern:** Monthly provisional sales peak in November 2011 within the observed period.
3. **Customer Concentration:** The Champions segment has the largest provisional sales contribution among the reported customer segments.
4. **Customer Diversity:** The RFM summary identifies six customer segments with different customer counts and sales contributions.
5. **Data Quality Matters:** Duplicate records, cancellations, missing identifiers, and unusual prices require explicit treatment to reduce misleading conclusions.
6. **Product Interpretation Requires Context:** Postage and manual entries appear among highly ranked stock codes, demonstrating the importance of business context when interpreting aggregated results.

These findings describe the analyzed historical dataset. They are not causal conclusions or forecasts.

## Project Structure

The repository is organized around data processing, analytical SQL, testing, notebooks, documentation, and reporting.

```text
customer-revenue-intelligence-platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── business_problem.md
│   └── metric_dictionary.md
│
├── notebooks/
│   └── 01_data_quality_and_preprocessing.ipynb
│
├── reports/
│   ├── initial_data_profile.txt
│   └── record_investigation/
│
├── src/
│   ├── data_quality.py
│   ├── investigate_records.py
│   ├── cleaning.py
│   ├── validate_pipeline.py
│   ├── test_db_connection.py
│   └── load_to_postgres.py
│
├── tests/
│   └── test_cleaning.py
│
├── sql/
│   └── SQL scripts for analytical views
│
├── requirements.txt
├── .gitignore
└── README.md
```

> **Note:** Adjust the structure above to match the files actually present in the repository. Include the Power BI `.pbix` file if it is part of the published project.

## Getting Started

### Prerequisites

Install the following tools:

- Python 3.13 or another compatible Python environment.
- PostgreSQL.
- Power BI Desktop.
- Git.
- Visual Studio Code or another Python editor.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/customer-revenue-intelligence-platform.git
cd customer-revenue-intelligence-platform
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Download the Dataset

Download the Online Retail dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail).

Place the downloaded Excel file at:

```text
data/raw/Online Retail.xlsx
```

The raw dataset does not need to be committed to GitHub. Follow the dataset provider's terms and your repository's storage policy.

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```text
customer_revenue_intelligence
```

Configure the database credentials locally using environment variables. For example, create a `.env` file in the project root:

```ini
PGHOST=localhost
PGPORT=5432
PGDATABASE=customer_revenue_intelligence
PGUSER=your_postgres_username
PGPASSWORD=your_local_password
```

**Security requirements:**

- Never commit `.env` or database passwords to GitHub.
- Ensure `.env` is listed in `.gitignore`.
- Verify that the Python database connection code reads the same variable names.

### 5. Run Data Profiling and Classification

Run the profiling script:

```powershell
.\.venv\Scripts\python.exe src\data_quality.py
```

Investigate unusual records:

```powershell
.\.venv\Scripts\python.exe src\investigate_records.py
```

Run the classification pipeline:

```powershell
.\.venv\Scripts\python.exe src\cleaning.py
```

Validate the classified dataset:

```powershell
.\.venv\Scripts\python.exe src\validate_pipeline.py
```

These commands assume the scripts and paths match the published repository. Adjust their configuration if necessary.

### 6. Run Automated Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

The implemented cleaning tests previously passed with eight successful tests.

### 7. Load Data into PostgreSQL

Verify the database connection:

```powershell
.\.venv\Scripts\python.exe src\test_db_connection.py
```

Load the classified dataset:

```powershell
.\.venv\Scripts\python.exe src\load_to_postgres.py
```

Execute the SQL scripts in the repository to create the analytical views. Ensure the required schemas and transaction table exist before creating the views.

### 8. Open the Power BI Report

Open the project's `.pbix` file in Power BI Desktop.

When using a new environment:

1. Configure the PostgreSQL server and database.
2. Enter the appropriate authentication credentials.
3. Configure data source permissions.
4. Confirm that the analytical views exist.
5. Refresh the Power BI model.
6. Validate key dashboard metrics against PostgreSQL query results.

## Limitations and Future Improvements

The current implementation provides a data-classification pipeline, PostgreSQL analytics, and a three-page Power BI dashboard.

Potential extensions include:

- Reconcile provisional sales with a documented accounting treatment for returns, cancellations, and adjustments.
- Investigate the difference between raw distinct stock-code counts and the Product Codes KPI.
- Add month-over-month growth and average order value after defining their calculation rules.
- Develop cohort-based customer retention analysis.
- Add reusable SQL data-quality checks.
- Expand automated testing to database queries and end-to-end data refreshes.
- Document deployment and dashboard refresh procedures.

These are proposed enhancements, not features claimed as already implemented.

## Skills Demonstrated

This project demonstrates practical experience with:

- Exploratory data analysis and data-quality investigation.
- Python-based data processing and classification.
- SQL aggregations and analytical database design.
- PostgreSQL connectivity and data loading.
- Business KPI definition and metric validation.
- Customer segmentation and product performance analysis.
- Power BI dashboard development and reporting.
- Automated testing and reproducible project organization.
- Communicating analytical findings with appropriate caveats.

## Author

**Vidhanshu Singh**

B.Tech Information Technology | Aspiring Data Analyst

Interested in data analytics, business intelligence, SQL, Python, and turning transactional data into actionable business insights.

- **GitHub:** [YOUR_GITHUB_PROFILE](https://github.com/YOUR_USERNAME)
- **LinkedIn:** [YOUR_LINKEDIN_PROFILE](https://www.linkedin.com/)

Replace the placeholder profile links with your actual URLs before publishing.

---

*Built as a portfolio project to demonstrate an end-to-end analytics workflow, from raw transactional data to validated SQL metrics and interactive business intelligence reporting.*
