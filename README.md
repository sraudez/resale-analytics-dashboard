# Depop Sales Analytics Dashboard

## Overview

This project analyzes Depop resale sales data from **October 25, 2024 through January 9, 2025**. The goal is to turn raw marketplace transaction data into useful business insights about revenue, fees, product categories, brands, sales timing, and customer location trends.

The dataset contains **125 sales records** with information such as sale date, listing date, item price, shipping cost, platform fees, brand, size, category, buyer state, payout dates, refunds, and payment type.

This project is designed to showcase data analytics skills through data cleaning, metric calculation, exploratory analysis, and dashboard visualization.

---

## Business Questions

This dashboard is built around the following questions:

- How much gross revenue did the shop generate during the sales period?
- Which product categories generated the most revenue?
- Which brands sold the most and produced the highest sales value?
- How long did items typically take to sell after being listed?
- Which sizes and categories performed best?
- How much did platform-related fees affect seller payout?
- Which states had the most buyers?
- How did monthly sales performance change over time?

---

## Dataset Summary

The raw CSV includes the following types of fields:

### Sale and Listing Information

- `Date of sale`
- `Time of sale`
- `Date of listing`
- `Estimated payout date`
- `Payout arrival date`

### Product Information

- `Brand`
- `Description`
- `Size`
- `Category`
- `Bundle`
- `Bundle - amount of items`

### Financial Information

- `Item price`
- `Buyer shipping cost`
- `Total`
- `USPS Cost`
- `Depop fee`
- `Depop Payments fee`
- `Buyer Marketplace Fee`
- `Boosting fee`
- `US Sales tax`
- `Refunded to buyer amount`
- `Fees refunded to seller`

### Buyer and Location Information

- `Buyer`
- `Name`
- `City`
- `State`
- `Country`
- Address-related fields

> **Privacy note:** The original CSV contains buyer names and addresses. These fields should be removed, anonymized, or excluded before publishing the dataset publicly on GitHub.

---

## Key Metrics from the Dataset

Based on the available sales data:

| Metric | Value |
|---|---:|
| Number of sales records | 125 |
| Sales period | Oct. 25, 2024 - Jan. 9, 2025 |
| Gross item revenue | $1,413.25 |
| Total transaction value | $2,472.49 |
| Estimated net before cost of goods | $1,154.13 |
| Seller-related fees | $151.62 |
| Average item sale price | $11.31 |
| Median item sale price | $10.00 |
| Average days to sell | 3.35 days |
| Median days to sell | 2 days |

### Important Metric Limitation

The dataset does **not** include original sourcing or purchase cost for each item. Because of that, this project can estimate net sales proceeds before cost of goods, but it cannot calculate true profit unless a `purchase_price` or `cost_of_goods` column is added.

Suggested future formula:

```text
profit = item_price - seller_fees - purchase_price
```

---

## Category Performance

| Category | Items Sold | Gross Revenue | Average Price | Average Days to Sell |
|---|---:|---:|---:|---:|
| Tops | 67 | $640.25 | $9.56 | 3.13 |
| Coats and jackets | 25 | $392.00 | $15.68 | 4.96 |
| Bottoms | 27 | $337.50 | $12.50 | 2.37 |
| Underwear | 2 | $24.00 | $12.00 | 2.00 |
| Accessories | 4 | $19.50 | $4.88 | 4.25 |

### Category Insights

- **Tops** were the highest-volume category, making up more than half of the sales records.
- **Coats and jackets** had the highest average sale price at $15.68.
- **Bottoms** sold faster than tops and jackets on average, with an average time to sell of 2.37 days.
- Accessories had lower sales volume and lower average sale prices compared to clothing categories.

---

## Brand Performance

Top brands by gross item revenue:

| Brand | Items Sold | Gross Revenue | Average Price | Average Days to Sell |
|---|---:|---:|---:|---:|
| Other | 42 | $382.50 | $9.11 | 3.17 |
| Nike | 16 | $218.00 | $13.62 | 5.81 |
| Lululemon | 5 | $111.50 | $22.30 | 1.40 |
| Polo Ralph Lauren | 6 | $86.00 | $14.33 | 1.83 |
| The North Face | 6 | $86.00 | $14.33 | 3.00 |
| Realtree | 5 | $81.00 | $16.20 | 0.80 |
| Adidas | 7 | $69.00 | $9.86 | 1.14 |
| Russell Athletic | 5 | $43.00 | $8.60 | 1.40 |
| Kappa | 1 | $40.00 | $40.00 | 4.00 |
| Supreme | 2 | $21.00 | $10.50 | 0.00 |

### Brand Insights

- Items labeled as **Other** produced the most total revenue, but this category may need further cleaning because it groups many unbranded or uncategorized items together.
- **Nike** was the strongest named brand by total revenue.
- **Lululemon** had the highest average sale price among brands with multiple sales.
- **Realtree**, **Adidas**, **Lululemon**, and **Polo Ralph Lauren** sold quickly on average, suggesting strong resale demand in this dataset.

---

## Monthly Sales Performance

| Month | Items Sold | Gross Revenue | Estimated Net Before COGS | Average Days to Sell |
|---|---:|---:|---:|---:|
| 2024-10 | 11 | $145.50 | $125.60 | 2.36 |
| 2024-11 | 61 | $543.25 | $450.23 | 2.18 |
| 2024-12 | 49 | $680.50 | $541.15 | 4.98 |
| 2025-01 | 4 | $44.00 | $37.15 | 4.00 |

### Monthly Insights

- **November 2024** had the highest sales volume with 61 sales.
- **December 2024** had the highest gross revenue at $680.50, even with fewer sales than November.
- Items sold fastest on average in November.
- January only includes partial-month data, so it should not be compared directly to full months.

---

## Buyer Location Insights

Top buyer states by number of sales:

| State | Items Sold | Gross Revenue |
|---|---:|---:|
| CA | 17 | $197.50 |
| TX | 14 | $169.50 |
| FL | 9 | $106.00 |
| NY | 6 | $66.50 |
| PA | 6 | $44.00 |
| IN | 5 | $50.00 |
| NC | 5 | $27.60 |
| NJ | 4 | $41.00 |
| IL | 4 | $24.75 |
| GA | 4 | $46.50 |

### Location Insights

- California, Texas, and Florida were the top buyer states by number of sales.
- This information could be used to understand where demand is strongest, although buyer location may also be influenced by Depop's recommendation and search algorithms.

---

## Suggested Dashboard Features

The dashboard should include:

### KPI Cards

- Total sales records
- Gross item revenue
- Estimated net before cost of goods
- Average sale price
- Median sale price
- Average days to sell
- Total seller fees

### Charts

- Monthly gross revenue trend
- Monthly items sold
- Gross revenue by category
- Average days to sell by category
- Top brands by revenue
- Top brands by average sale price
- Buyer state distribution
- Fee breakdown
- Size distribution

### Filters

- Date range
- Category
- Brand
- Size
- Buyer state
- Bundle status
- Payment type

---

## Data Cleaning Steps

The raw CSV requires cleaning before analysis. Key cleaning tasks include:

1. Convert currency columns from strings into numeric values.
   - Example: `$8.50` → `8.50`
   - Example: `="-"` → `0.00`

2. Convert date columns into datetime values.
   - `Date of sale`
   - `Date of listing`
   - `Estimated payout date`
   - `Payout arrival date`

3. Create a `days_to_sell` column.

```text
days_to_sell = date_of_sale - date_of_listing
```

4. Create a `seller_fees` column.

```text
seller_fees = depop_fee + depop_payments_fee + boosting_fee - fees_refunded_to_seller
```

5. Create an estimated net proceeds column.

```text
estimated_net_before_cogs = item_price - seller_fees - refunded_to_buyer_amount
```

6. Remove or anonymize personally identifiable information before sharing.

Fields to remove before publishing include:

- Buyer names
- Full names
- Street addresses
- City combined with address fields
- Post codes

---

## Recommended Clean Architecture Structure

```text
depop-sales-analytics/
│
├── data/
│   ├── raw/
│   │   └── depop_sales_raw.csv
│   ├── processed/
│   │   └── depop_sales_cleaned.csv
│   └── README.md
│
├── domain/
│   ├── sale.py
│   └── metrics.py
│
├── application/
│   ├── clean_sales_data.py
│   ├── calculate_metrics.py
│   └── generate_dashboard_data.py
│
├── infrastructure/
│   └── csv_sales_repository.py
│
├── interface/
│   ├── streamlit_app.py
│   └── charts.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── tests/
│   ├── test_metrics.py
│   └── test_cleaning.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

### Layer Responsibilities

| Layer | Purpose |
|---|---|
| `domain` | Core business logic, such as fee, revenue, and days-to-sell calculations |
| `application` | Use cases, such as cleaning the dataset and preparing dashboard summaries |
| `infrastructure` | CSV loading, saving, and future database or API connections |
| `interface` | Streamlit dashboard, filters, charts, and user-facing layout |
| `tests` | Unit tests for calculations and cleaning logic |

---

## Tools Used

Recommended tools for this project:

- Python
- Pandas
- Plotly
- Streamlit
- Jupyter Notebook
- GitHub

Optional additions:

- SQL for querying cleaned sales data
- Tableau or Power BI for an alternate dashboard version
- Scikit-learn for future sales prediction or pricing analysis

---

