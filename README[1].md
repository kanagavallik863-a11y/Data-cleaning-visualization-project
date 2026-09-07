# Data Cleaning & Visualization Project

A raw-to-insights pipeline built on a synthetic **retail sales dataset**. The dataset
was generated to intentionally include the kinds of issues real-world data has —
missing values, duplicate rows, outliers, and inconsistent text formatting — so the
full data cleaning workflow could be demonstrated end to end.

## Project Structure

```
data_project/
├── data/
│   ├── generate_raw_data.py     # Creates the raw (messy) dataset
│   └── raw_sales_data.csv       # Raw dataset (620 rows, 9 columns)
├── notebooks/
│   ├── clean_data.py            # Cleaning pipeline
│   └── visualize_data.py        # Visualization pipeline
├── outputs/
│   ├── cleaned_sales_data.csv   # Cleaned dataset (600 rows)
│   └── cleaning_summary.txt     # Log of every cleaning step & counts
├── visuals/
│   ├── revenue_by_category.png
│   ├── revenue_by_region.png
│   ├── monthly_revenue_trend.png
│   ├── payment_method_share.png
│   ├── customer_age_distribution.png
│   └── correlation_heatmap.png
└── README.md
```

## How to Run

```bash
pip install pandas numpy matplotlib seaborn

python data/generate_raw_data.py       # regenerate raw data (optional, already included)
python notebooks/clean_data.py         # clean the raw data
python notebooks/visualize_data.py     # generate all visualizations
```

## Data Cleaning Steps (Pandas)

1. **Standardized text fields** — trimmed whitespace and fixed inconsistent
   casing in `Region`, `Category`, `PaymentMethod` (e.g. `" East "`, `"north"`,
   `"credit card"` → consistent title case).
2. **Handled missing values** — 30–33 missing entries per column were filled:
   categorical columns with the mode, numeric columns with the median.
3. **Removed duplicates** — 20 exact duplicate rows dropped.
4. **Fixed invalid values** — out-of-range `CustomerAge` entries (negative or
   >100) replaced with the column median.
5. **Treated outliers** — used the IQR method to cap extreme `Revenue` values
   instead of dropping them, preserving sample size while limiting distortion.

Full step-by-step counts are in `outputs/cleaning_summary.txt`.

## Visualizations (Matplotlib + Seaborn)

| Chart | What it shows |
|---|---|
| `revenue_by_category.png` | Total revenue per product category |
| `revenue_by_region.png` | Total revenue per region |
| `monthly_revenue_trend.png` | Revenue trend across 2025 |
| `payment_method_share.png` | Share of orders by payment method |
| `customer_age_distribution.png` | Distribution of customer ages |
| `correlation_heatmap.png` | Correlation between quantity, price, revenue, age |

## Key Insights

- Total revenue across the cleaned dataset: **₹8,05,563.85**
- **Electronics** is the top-performing category by revenue.
- **North** is the highest-revenue region.
- **January 2025** was the strongest month for sales.
- **Credit Card** is the most-used payment method.
- Average customer age is **~43 years**.

## Expected Outcome (Task Goal)

This project demonstrates the full data-preprocessing → visualization →
storytelling workflow: identifying data quality issues, applying appropriate
cleaning techniques (imputation, deduplication, outlier capping), and
communicating findings through clear, labeled charts.
