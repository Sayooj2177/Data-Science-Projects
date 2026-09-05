import pandas as pd

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("../Data/online_retail.csv")

print("Original Dataset Shape:", df.shape)

# ==========================================
# 2. CONVERT INVOICE DATE
# ==========================================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# ==========================================
# 3. CHECK CANCELLED TRANSACTIONS
# ==========================================

cancelled_transactions = df["InvoiceNo"].astype(str).str.startswith("C")

print("\nCancelled Transactions:", cancelled_transactions.sum())

# ==========================================
# 4. REMOVE CANCELLED TRANSACTIONS
# ==========================================

df = df[~cancelled_transactions].copy()

# ==========================================
# 5. REMOVE INVALID QUANTITIES
# ==========================================

df = df[df["Quantity"] > 0].copy()

# ==========================================
# 6. REMOVE INVALID PRICES
# ==========================================

df = df[df["UnitPrice"] > 0].copy()

# ==========================================
# 7. REMOVE MISSING CUSTOMER IDs
# ==========================================

df = df.dropna(subset=["CustomerID"]).copy()

# Convert CustomerID to integer
df["CustomerID"] = df["CustomerID"].astype(int)

# ==========================================
# 8. CREATE REVENUE COLUMN
# ==========================================

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# ==========================================
# 9. DISPLAY CLEANED DATA
# ==========================================

print("\nCleaned Dataset Shape:", df.shape)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nFirst 5 Cleaned Rows:")
print(df.head())

print("\nTotal Revenue:")
print(f"£{df['Revenue'].sum():,.2f}")

print("\nNumber of Customers:")
print(df["CustomerID"].nunique())

print("\nNumber of Countries:")
print(df["Country"].nunique())

import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 10. MONTHLY REVENUE ANALYSIS
# ==========================================

df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index()
)

monthly_revenue["YearMonth"] = monthly_revenue["YearMonth"].astype(str)

print("\nMonthly Revenue:")
print(monthly_revenue)

# ==========================================
# MONTHLY REVENUE GRAPH
# ==========================================

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly_revenue,
    x="YearMonth",
    y="Revenue",
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "../graphs/monthly_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 11. TOP 10 PRODUCTS BY REVENUE
# ==========================================

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

print("\nTop 10 Products by Revenue:")
print(top_products.sort_values(ascending=False))

# ==========================================
# TOP PRODUCTS GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

top_products.plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "../graphs/top_10_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 13. RFM CUSTOMER ANALYSIS
# ==========================================

# Set the analysis date as one day after the
# last transaction in the dataset
analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

# ==========================================
# DISPLAY RFM DATA
# ==========================================

print("\n" + "=" * 50)
print("RFM CUSTOMER ANALYSIS")
print("=" * 50)

print("\nRFM Dataset Shape:")
print(rfm.shape)

print("\nFirst 10 Customers:")
print(rfm.head(10))

print("\nRFM Statistics:")
print(rfm[["Recency", "Frequency", "Monetary"]].describe())

# ==========================================
# 14. RFM DISTRIBUTION GRAPHS
# ==========================================

# Recency distribution
plt.figure(figsize=(10, 6))

sns.histplot(
    data=rfm,
    x="Recency",
    bins=50
)

plt.title("Customer Recency Distribution")
plt.xlabel("Days Since Last Purchase")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "../graphs/recency_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Frequency distribution
plt.figure(figsize=(10, 6))

sns.histplot(
    data=rfm,
    x="Frequency",
    bins=50
)

plt.title("Customer Purchase Frequency Distribution")
plt.xlabel("Number of Purchases")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "../graphs/frequency_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Monetary distribution
plt.figure(figsize=(10, 6))

sns.histplot(
    data=rfm,
    x="Monetary",
    bins=50
)

plt.title("Customer Monetary Value Distribution")
plt.xlabel("Total Spending (£)")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "../graphs/monetary_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# TOP 10 COUNTRIES BY REVENUE
# ==========================================

top_countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

print("\nTop 10 Countries by Revenue:")
print(top_countries.sort_values(ascending=False))

plt.figure(figsize=(10, 6))

top_countries.plot(kind="barh")

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    "../graphs/top_10_countries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

