import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("../Data/creditcard.csv")

# ==============================
# BASIC DATASET INFORMATION
# ==============================

print("Dataset Shape:", df.shape)

print("\nClass Distribution:")
print(df["Class"].value_counts())

print("\nFraud Percentage:")
fraud_percentage = (df["Class"].mean()) * 100
print(f"{fraud_percentage:.3f}%")

# ==============================
# GRAPH 1: CLASS DISTRIBUTION
# ==============================

plt.figure(figsize=(8, 5))

sns.countplot(x="Class", data=df)

plt.title("Normal vs Fraudulent Transactions")
plt.xlabel("Transaction Class")
plt.ylabel("Number of Transactions")

plt.xticks([0, 1], ["Normal", "Fraud"])

plt.savefig(
    "../graphs/class_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==============================
# GRAPH 2: TRANSACTION AMOUNT
# ==============================

plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="Amount",
    bins=50
)

plt.title("Distribution of Transaction Amounts")
plt.xlabel("Transaction Amount")
plt.ylabel("Number of Transactions")

plt.savefig(
    "../graphs/transaction_amount_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==============================
# GRAPH 3: FRAUD VS NORMAL AMOUNT
# ==============================

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="Class",
    y="Amount"
)

plt.title("Transaction Amount: Normal vs Fraud")
plt.xlabel("Transaction Class")
plt.ylabel("Transaction Amount")

plt.xticks([0, 1], ["Normal", "Fraud"])

plt.savefig(
    "../graphs/fraud_vs_normal_amount.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==============================
# GRAPH 4: CORRELATION HEATMAP
# ==============================

plt.figure(figsize=(14, 10))

correlation_matrix = df.corr()

sns.heatmap(
    correlation_matrix,
    cmap="coolwarm",
    linewidths=0.2
)

plt.title("Feature Correlation Heatmap")

plt.savefig(
    "../graphs/correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()