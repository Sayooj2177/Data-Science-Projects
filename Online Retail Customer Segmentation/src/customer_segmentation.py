import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("../Data/online_retail.csv")

# ==========================================
# 2. DATA CLEANING
# ==========================================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove cancelled transactions
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
df = df[~cancelled].copy()

# Remove invalid quantities and prices
df = df[df["Quantity"] > 0].copy()
df = df[df["UnitPrice"] > 0].copy()

# Remove missing Customer IDs
df = df.dropna(subset=["CustomerID"]).copy()

# Convert CustomerID to integer
df["CustomerID"] = df["CustomerID"].astype(int)

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# ==========================================
# 3. CREATE RFM DATASET
# ==========================================

analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

print("RFM Dataset Shape:", rfm.shape)

# ==========================================
# 4. LOG TRANSFORMATION
# ==========================================

rfm_features = rfm[
    ["Recency", "Frequency", "Monetary"]
].copy()

rfm_log = np.log1p(rfm_features)

# ==========================================
# 5. STANDARDIZE FEATURES
# ==========================================

scaler = StandardScaler()

rfm_scaled = scaler.fit_transform(rfm_log)

# ==========================================
# 6. FIND OPTIMAL NUMBER OF CLUSTERS
# ==========================================

silhouette_scores = []

for k in range(2, 9):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(rfm_scaled)

    score = silhouette_score(
        rfm_scaled,
        labels
    )

    silhouette_scores.append(score)

    print(
        f"Clusters: {k} | "
        f"Silhouette Score: {score:.4f}"
    )

# ==========================================
# 7. SILHOUETTE SCORE GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    range(2, 9),
    silhouette_scores,
    marker="o"
)

plt.title("Silhouette Score for Different Cluster Counts")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")

plt.xticks(range(2, 9))

plt.tight_layout()

plt.savefig(
    "../graphs/silhouette_scores.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 8. TRAIN FINAL K-MEANS MODEL
# ==========================================

# Choose 4 clusters for customer segmentation
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

# ==========================================
# 9. CLUSTER SUMMARY
# ==========================================

cluster_summary = rfm.groupby("Cluster").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean")
).round(2)

print("\n" + "=" * 50)
print("CUSTOMER SEGMENTATION RESULTS")
print("=" * 50)

print(cluster_summary)

# ==========================================
# 10. ASSIGN CUSTOMER SEGMENT NAMES
# ==========================================

segment_names = {
    0: "Recent / Occasional",
    1: "High-Value Loyal",
    2: "Regular Customers",
    3: "At-Risk Customers"
}

rfm["Segment"] = rfm["Cluster"].map(segment_names)

# ==========================================
# 11. FINAL SEGMENT SUMMARY
# ==========================================

segment_summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean")
).round(2)

print("\n" + "=" * 60)
print("FINAL CUSTOMER SEGMENT SUMMARY")
print("=" * 60)

print(segment_summary)

# ==========================================
# 12. CUSTOMER COUNT BY SEGMENT
# ==========================================

plt.figure(figsize=(10, 6))

segment_counts = (
    rfm["Segment"]
    .value_counts()
)

sns.barplot(
    x=segment_counts.values,
    y=segment_counts.index
)

plt.title("Number of Customers by Segment")
plt.xlabel("Number of Customers")
plt.ylabel("Customer Segment")

plt.tight_layout()

plt.savefig(
    "../graphs/customer_segments.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 13. MONETARY VALUE BY SEGMENT
# ==========================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=rfm,
    x="Segment",
    y="Monetary"
)

plt.title("Customer Spending by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Monetary Value (£)")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    "../graphs/customer_spending_by_segment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 14. RECENCY VS MONETARY VALUE
# ==========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=rfm,
    x="Recency",
    y="Monetary",
    hue="Segment",
    alpha=0.6
)

plt.title("Customer Recency vs Monetary Value")
plt.xlabel("Recency (Days)")
plt.ylabel("Monetary Value (£)")

plt.tight_layout()

plt.savefig(
    "../graphs/recency_vs_monetary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 11. FINAL SEGMENT SUMMARY
# ==========================================

segment_summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean")
).round(2)



# ==========================================
# 12. CUSTOMER COUNT BY SEGMENT
# ==========================================

plt.figure(figsize=(10, 6))

segment_counts = (
    rfm["Segment"]
    .value_counts()
)

sns.barplot(
    x=segment_counts.values,
    y=segment_counts.index
)

plt.title("Number of Customers by Segment")
plt.xlabel("Number of Customers")
plt.ylabel("Customer Segment")

plt.tight_layout()

plt.savefig(
    "../graphs/customer_segments.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 13. MONETARY VALUE BY SEGMENT
# ==========================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=rfm,
    x="Segment",
    y="Monetary"
)

plt.title("Customer Spending by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Monetary Value (£)")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    "../graphs/customer_spending_by_segment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 14. RECENCY VS MONETARY VALUE
# ==========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=rfm,
    x="Recency",
    y="Monetary",
    hue="Segment",
    alpha=0.6
)

plt.title("Customer Recency vs Monetary Value")
plt.xlabel("Recency (Days)")
plt.ylabel("Monetary Value (£)")

plt.tight_layout()

plt.savefig(
    "../graphs/recency_vs_monetary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()