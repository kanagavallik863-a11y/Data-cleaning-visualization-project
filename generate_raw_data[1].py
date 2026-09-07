"""
generate_raw_data.py
---------------------
Generates a synthetic, intentionally messy "Retail Sales" dataset
(missing values, duplicates, outliers, inconsistent text) to use as
the raw input for the Data Cleaning & Visualization Project.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 600

regions = ["North", "South", "East", "West", "north", "SOUTH", " East "]
categories = ["Electronics", "Clothing", "Grocery", "Furniture", "Toys"]
payment_methods = ["Credit Card", "UPI", "Cash", "Debit Card", "credit card", "cash "]

dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")

rows = []
for i in range(N):
    order_id = f"ORD{1000 + i}"
    date = np.random.choice(dates)
    region = np.random.choice(regions)
    category = np.random.choice(categories)
    payment = np.random.choice(payment_methods)

    quantity = np.random.randint(1, 10)
    unit_price = round(np.random.uniform(5, 500), 2)
    revenue = round(quantity * unit_price, 2)

    customer_age = np.random.randint(18, 70)

    rows.append([order_id, date, region, category, payment,
                 quantity, unit_price, revenue, customer_age])

df = pd.DataFrame(rows, columns=[
    "OrderID", "OrderDate", "Region", "Category", "PaymentMethod",
    "Quantity", "UnitPrice", "Revenue", "CustomerAge"
])

# --- Inject messiness ---

# 1. Missing values
for col in ["Region", "Category", "PaymentMethod", "Quantity", "UnitPrice", "CustomerAge"]:
    missing_idx = np.random.choice(df.index, size=int(0.05 * N), replace=False)
    df.loc[missing_idx, col] = np.nan

# 2. Duplicate rows
dupes = df.sample(20, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# 3. Outliers
outlier_idx = np.random.choice(df.index, size=8, replace=False)
df.loc[outlier_idx, "Revenue"] = df.loc[outlier_idx, "Revenue"] * np.random.uniform(15, 40)
df.loc[np.random.choice(df.index, 5, replace=False), "CustomerAge"] = np.random.choice([120, -5, 150], 5)

# 4. Inconsistent formatting already introduced via region/payment casing

# Shuffle rows
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("/home/claude/data_project/data/raw_sales_data.csv", index=False)
print("Raw dataset generated:", df.shape)
