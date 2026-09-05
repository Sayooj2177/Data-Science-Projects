import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("../Data/creditcard.csv")

print("Dataset Shape:", df.shape)

# Separate features and target
X = df.drop("Class", axis=1)
y = df["Class"]

# ==========================================
# 2. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# 3. SCALE FEATURES
# ==========================================

scaler = StandardScaler()

X_train = X_train.copy()
X_test = X_test.copy()

X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)

# ==========================================
# 4. LOGISTIC REGRESSION
# ==========================================

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(X_train, y_train)

lr_pred = logistic_model.predict(X_test)
lr_probability = logistic_model.predict_proba(X_test)[:, 1]

print("\n" + "=" * 50)
print("LOGISTIC REGRESSION RESULTS")
print("=" * 50)

print("\nClassification Report:")
print(classification_report(y_test, lr_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, lr_pred))

print("\nROC-AUC Score:")
lr_auc = roc_auc_score(y_test, lr_probability)
print(round(lr_auc, 4))

# ==========================================
# 5. BALANCED LOGISTIC REGRESSION
# ==========================================

balanced_model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight="balanced"
)

balanced_model.fit(X_train, y_train)

balanced_pred = balanced_model.predict(X_test)
balanced_probability = balanced_model.predict_proba(X_test)[:, 1]

print("\n" + "=" * 50)
print("BALANCED LOGISTIC REGRESSION RESULTS")
print("=" * 50)

print("\nClassification Report:")
print(classification_report(y_test, balanced_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, balanced_pred))

print("\nROC-AUC Score:")
balanced_auc = roc_auc_score(
    y_test,
    balanced_probability
)
print(round(balanced_auc, 4))

# ==========================================
# 6. RANDOM FOREST
# ==========================================

random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

random_forest.fit(X_train, y_train)

rf_pred = random_forest.predict(X_test)
rf_probability = random_forest.predict_proba(X_test)[:, 1]

print("\n" + "=" * 50)
print("RANDOM FOREST RESULTS")
print("=" * 50)

print("\nClassification Report:")
print(classification_report(y_test, rf_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, rf_pred))

print("\nROC-AUC Score:")
rf_auc = roc_auc_score(y_test, rf_probability)
print(round(rf_auc, 4))

# ==========================================
# 7. MODEL COMPARISON
# ==========================================

comparison = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Balanced Logistic Regression",
        "Random Forest"
    ],
    "Precision": [
        precision_score(y_test, lr_pred),
        precision_score(y_test, balanced_pred),
        precision_score(y_test, rf_pred)
    ],
    "Recall": [
        recall_score(y_test, lr_pred),
        recall_score(y_test, balanced_pred),
        recall_score(y_test, rf_pred)
    ],
    "F1 Score": [
        f1_score(y_test, lr_pred),
        f1_score(y_test, balanced_pred),
        f1_score(y_test, rf_pred)
    ],
    "ROC-AUC": [
        lr_auc,
        balanced_auc,
        rf_auc
    ]
})

print("\n" + "=" * 50)
print("MODEL COMPARISON")
print("=" * 50)

print(comparison.to_string(index=False))

# ==========================================
# 8. MODEL COMPARISON GRAPH
# ==========================================

comparison_plot = comparison.set_index("Model")

comparison_plot.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Fraud Detection Model Comparison")
plt.xlabel("Model")
plt.ylabel("Score")
plt.ylim(0, 1)

plt.xticks(rotation=15)

plt.legend(
    title="Metrics",
    loc="lower right"
)

plt.tight_layout()

plt.savefig(
    "../graphs/model_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 9. RANDOM FOREST CONFUSION MATRIX
# ==========================================

rf_cm = confusion_matrix(y_test, rf_pred)

plt.figure(figsize=(7, 5))

sns.heatmap(
    rf_cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Normal", "Fraud"],
    yticklabels=["Normal", "Fraud"]
)

plt.title("Random Forest Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig(
    "../graphs/random_forest_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 10. ROC CURVE COMPARISON
# ==========================================

from sklearn.metrics import roc_curve

# Calculate ROC curves
lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probability)

balanced_fpr, balanced_tpr, _ = roc_curve(
    y_test,
    balanced_probability
)

rf_fpr, rf_tpr, _ = roc_curve(
    y_test,
    rf_probability
)

# Create ROC curve
plt.figure(figsize=(10, 7))

plt.plot(
    lr_fpr,
    lr_tpr,
    label=f"Logistic Regression (AUC = {lr_auc:.4f})"
)

plt.plot(
    balanced_fpr,
    balanced_tpr,
    label=f"Balanced Logistic Regression (AUC = {balanced_auc:.4f})"
)

plt.plot(
    rf_fpr,
    rf_tpr,
    label=f"Random Forest (AUC = {rf_auc:.4f})"
)

# Random classifier reference line
plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)

plt.title("ROC Curve - Fraud Detection Models")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.legend()
plt.grid(alpha=0.3)

plt.savefig(
    "../graphs/roc_curve_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 11. RANDOM FOREST FEATURE IMPORTANCE
# ==========================================

feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": random_forest.feature_importances_
})

# Sort features by importance
feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n" + "=" * 50)
print("TOP 10 FEATURE IMPORTANCE")
print("=" * 50)

print(feature_importance.head(10).to_string(index=False))

# ==========================================
# FEATURE IMPORTANCE GRAPH
# ==========================================

top_features = feature_importance.head(10)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=top_features,
    x="Importance",
    y="Feature"
)

plt.title("Top 10 Features - Random Forest")
plt.xlabel("Importance")
plt.ylabel("Feature")

plt.tight_layout()

plt.savefig(
    "../graphs/feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()