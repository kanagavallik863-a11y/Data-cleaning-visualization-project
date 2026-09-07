"""
clean_data.py
-------------
Cleans the raw retail sales dataset:
  1. Standardizes text fields (casing, whitespace)
  2. Handles missing values
  3. Removes duplicate rows
  4. Detects & treats outliers (IQR method)
Outputs a cleaned CSV + a cleaning summary log.
"""

import pandas as pd
import numpy as np

RAW_PATH = "/home/claude/data_project/data/raw_sales_data.csv"
CLEAN_PATH = "/home/claude/data_project/outputs/cleaned_sales_data.csv"
LOG_PATH = "/home/claude/data_project/outputs/cleaning_summary.txt"

log_lines = []


def log(msg):
    print(msg)
    log_lines.append(msg)


df = pd.read_csv(RAW_PATH, parse_dates=["OrderDate"])
log(f"Raw shape: {df.shape}")

# --- 1. Standardize text columns ---
for col in ["Region", "Category", "PaymentMethod"]:
    df[col] = df[col].astype(str).str.strip().str.title()
    df.loc[df[col].isin(["Nan", ""]), col] = np.nan

log("\nStep 1: Standardized text casing/whitespace in Region, Category, PaymentMethod")

# --- 2. Handle missing values ---
missing_before = df.isna().sum()
log("\nStep 2: Missing values before cleaning:\n" + missing_before[missing_before > 0].to_string())

# Categorical -> fill with mode
for col in ["Region", "Category", "PaymentMethod"]:
    mode_val = df[col].mode()[0]
    df[col] = df[col].fillna(mode_val)

# Numeric -> fill with median
for col in ["Quantity", "UnitPrice", "CustomerAge"]:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)

log("\nFilled categorical NaNs with mode, numeric NaNs with median.")

# --- 3. Remove duplicates ---
dupes_count = df.duplicated().sum()
df = df.drop_duplicates()
log(f"\nStep 3: Removed {dupes_count} duplicate rows.")

# --- 4. Fix invalid ages ---
invalid_age = df[(df["CustomerAge"] < 0) | (df["CustomerAge"] > 100)].shape[0]
df.loc[(df["CustomerAge"] < 0) | (df["CustomerAge"] > 100), "CustomerAge"] = df["CustomerAge"].median()
log(f"\nStep 4: Fixed {invalid_age} invalid CustomerAge values (out of 0-100 range).")

# --- 5. Outlier treatment on Revenue (IQR method) ---
Q1 = df["Revenue"].quantile(0.25)
Q3 = df["Revenue"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df["Revenue"] < lower) | (df["Revenue"] > upper)].shape[0]
df["Revenue"] = df["Revenue"].clip(lower=lower, upper=upper)
log(f"\nStep 5: Capped {outliers} Revenue outliers using IQR bounds "
    f"[{lower:.2f}, {upper:.2f}].")

# --- Recompute derived columns for consistency ---
df["Quantity"] = df["Quantity"].round().astype(int)
df["UnitPrice"] = df["UnitPrice"].round(2)
df["Revenue"] = df["Revenue"].round(2)
df["CustomerAge"] = df["CustomerAge"].round().astype(int)

log(f"\nFinal cleaned shape: {df.shape}")
log(f"Remaining missing values: {df.isna().sum().sum()}")

df.to_csv(CLEAN_PATH, index=False)

with open(LOG_PATH, "w") as f:
    f.write("\n".join(log_lines))

print(f"\nCleaned data saved to {CLEAN_PATH}")
print(f"Cleaning summary saved to {LOG_PATH}")
