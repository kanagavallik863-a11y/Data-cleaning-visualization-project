"""
visualize_data.py
------------------
Creates visual reports from the cleaned sales dataset using
Matplotlib and Seaborn: revenue by category/region, trends over
time, payment method share, and a correlation heatmap.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

CLEAN_PATH = "/home/claude/data_project/outputs/cleaned_sales_data.csv"
VIS_DIR = "/home/claude/data_project/visuals"

df = pd.read_csv(CLEAN_PATH, parse_dates=["OrderDate"])
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

# 1. Revenue by Category
plt.figure(figsize=(8, 5))
cat_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
sns.barplot(x=cat_rev.values, y=cat_rev.index, hue=cat_rev.index, palette="viridis", legend=False)
plt.title("Total Revenue by Category")
plt.xlabel("Revenue (₹)")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/revenue_by_category.png", dpi=150)
plt.close()

# 2. Revenue by Region
plt.figure(figsize=(8, 5))
reg_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
sns.barplot(x=reg_rev.index, y=reg_rev.values, hue=reg_rev.index, palette="mako", legend=False)
plt.title("Total Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/revenue_by_region.png", dpi=150)
plt.close()

# 3. Monthly Revenue Trend
plt.figure(figsize=(10, 5))
monthly = df.groupby("Month")["Revenue"].sum().sort_index()
plt.plot(monthly.index, monthly.values, marker="o", color="#2563eb")
plt.title("Monthly Revenue Trend (2025)")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/monthly_revenue_trend.png", dpi=150)
plt.close()

# 4. Payment Method Share
plt.figure(figsize=(6, 6))
pay_counts = df["PaymentMethod"].value_counts()
plt.pie(pay_counts.values, labels=pay_counts.index, autopct="%1.1f%%",
        colors=sns.color_palette("pastel"))
plt.title("Payment Method Share")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/payment_method_share.png", dpi=150)
plt.close()

# 5. Customer Age Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["CustomerAge"], bins=20, kde=True, color="#059669")
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/customer_age_distribution.png", dpi=150)
plt.close()

# 6. Correlation Heatmap
plt.figure(figsize=(6, 5))
num_cols = ["Quantity", "UnitPrice", "Revenue", "CustomerAge"]
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/correlation_heatmap.png", dpi=150)
plt.close()

print("All 6 visualizations saved to", VIS_DIR)
