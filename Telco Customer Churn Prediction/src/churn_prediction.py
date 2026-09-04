# ============================================
# TELCO CUSTOMER CHURN PREDICTION
# ============================================

# 1. IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    roc_curve
)

# ============================================
# 2. LOAD DATA
# ============================================

df = pd.read_csv("../Data/telco_customer_churn.csv")

print("\n========== DATASET OVERVIEW ==========")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# ============================================
# 3. DATA INFORMATION
# ============================================

print("\n========== DATA INFORMATION ==========")
print(df.info())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# ============================================
# 4. DATA CLEANING
# ============================================

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Remove rows with missing TotalCharges
df.dropna(subset=["TotalCharges"], inplace=True)

# Convert Churn into numerical format
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

print("\n========== AFTER CLEANING ==========")
print("Shape:", df.shape)

# ============================================
# 5. EXPLORATORY DATA ANALYSIS
# ============================================

# Churn distribution

plt.figure(figsize=(7, 5))

sns.countplot(
    x="Churn",
    data=df
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()


# ============================================
# 6. CHURN BY CONTRACT
# ============================================

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== CHURN RATE BY CONTRACT ==========")
print(contract_churn.round(2))

contract_churn.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Percentage")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# ============================================
# 7. TENURE VS CHURN
# ============================================

plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Churn",
    y="tenure",
    data=df
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig("../graphs/monthly_charges_vs_churn.png", dpi=300, bbox_inches="tight")

plt.show()


# ============================================
# 8. MONTHLY CHARGES VS CHURN
# ============================================

plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Churn",
    y="MonthlyCharges",
    data=df
)

plt.title("Monthly Charges vs Churn")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Monthly Charges")

plt.tight_layout()
plt.show()


# ============================================
# 9. PREPARE FEATURES AND TARGET
# ============================================

X = df.drop(
    columns=["customerID", "Churn"]
)

y = df["Churn"]

# Identify categorical and numerical columns

categorical_columns = X.select_dtypes(
    include=["str"]
).columns

numerical_columns = X.select_dtypes(
    exclude=["object"]
).columns

print("\n========== FEATURES ==========")
print("Categorical columns:")
print(list(categorical_columns))

print("\nNumerical columns:")
print(list(numerical_columns))


# ============================================
# 10. TRAIN TEST SPLIT
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================
# 11. PREPROCESSING
# ============================================

numerical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    ),
    (
        "scaler",
        StandardScaler()
    )
])

categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="most_frequent")
    ),
    (
        "encoder",
        OneHotEncoder(handle_unknown="ignore")
    )
])

preprocessor = ColumnTransformer([
    (
        "numerical",
        numerical_pipeline,
        numerical_columns
    ),
    (
        "categorical",
        categorical_pipeline,
        categorical_columns
    )
])


# ============================================
# 12. LOGISTIC REGRESSION
# ============================================

logistic_model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "model",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])

logistic_model.fit(
    X_train,
    y_train
)

logistic_prediction = logistic_model.predict(
    X_test
)

logistic_probability = logistic_model.predict_proba(
    X_test
)[:, 1]


# ============================================
# 13. RANDOM FOREST
# ============================================

random_forest_model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "model",
        RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )
    )
])

random_forest_model.fit(
    X_train,
    y_train
)

rf_prediction = random_forest_model.predict(
    X_test
)

rf_probability = random_forest_model.predict_proba(
    X_test
)[:, 1]


# ============================================
# 14. MODEL EVALUATION FUNCTION
# ============================================

def evaluate_model(
        model_name,
        y_true,
        predictions,
        probabilities
):

    accuracy = accuracy_score(
        y_true,
        predictions
    )

    precision = precision_score(
        y_true,
        predictions
    )

    recall = recall_score(
        y_true,
        predictions
    )

    f1 = f1_score(
        y_true,
        predictions
    )

    roc_auc = roc_auc_score(
        y_true,
        probabilities
    )

    print(f"\n========== {model_name} ==========")

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))
    print("ROC-AUC  :", round(roc_auc, 4))

    return [
        accuracy,
        precision,
        recall,
        f1,
        roc_auc
    ]


# ============================================
# 15. COMPARE MODELS
# ============================================

logistic_results = evaluate_model(
    "LOGISTIC REGRESSION",
    y_test,
    logistic_prediction,
    logistic_probability
)

rf_results = evaluate_model(
    "RANDOM FOREST",
    y_test,
    rf_prediction,
    rf_probability
)


# ============================================
# 16. MODEL COMPARISON TABLE
# ============================================

comparison = pd.DataFrame({

    "Model": [
        "Logistic Regression",
        "Random Forest"
    ],

    "Accuracy": [
        logistic_results[0],
        rf_results[0]
    ],

    "Precision": [
        logistic_results[1],
        rf_results[1]
    ],

    "Recall": [
        logistic_results[2],
        rf_results[2]
    ],

    "F1 Score": [
        logistic_results[3],
        rf_results[3]
    ],

    "ROC-AUC": [
        logistic_results[4],
        rf_results[4]
    ]

})

print("\n========== MODEL COMPARISON ==========")
print(comparison.round(4))


# ============================================
# 17. SELECT BEST MODEL
# ============================================

if rf_results[4] > logistic_results[4]:

    best_model = random_forest_model
    best_prediction = rf_prediction
    best_probability = rf_probability
    best_model_name = "Random Forest"

else:

    best_model = logistic_model
    best_prediction = logistic_prediction
    best_probability = logistic_probability
    best_model_name = "Logistic Regression"


print("\nBest Model:", best_model_name)


# ============================================
# 18. CLASSIFICATION REPORT
# ============================================

print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        best_prediction,
        target_names=[
            "No Churn",
            "Churn"
        ]
    )
)


# ============================================
# 19. CONFUSION MATRIX
# ============================================

cm = confusion_matrix(
    y_test,
    best_prediction
)

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=[
        "No Churn",
        "Churn"
    ],
    yticklabels=[
        "No Churn",
        "Churn"
    ]
)

plt.title(
    f"Confusion Matrix - {best_model_name}"
)

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()
plt.show()


# ============================================
# 20. ROC CURVE
# ============================================

logistic_fpr, logistic_tpr, _ = roc_curve(
    y_test,
    logistic_probability
)

rf_fpr, rf_tpr, _ = roc_curve(
    y_test,
    rf_probability
)

plt.figure(figsize=(8, 6))

plt.plot(
    logistic_fpr,
    logistic_tpr,
    label="Logistic Regression"
)

plt.plot(
    rf_fpr,
    rf_tpr,
    label="Random Forest"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve Comparison")

plt.legend()

plt.tight_layout()
plt.show()


# ============================================
# 21. FEATURE IMPORTANCE
# ============================================

if best_model_name == "Random Forest":

    fitted_preprocessor = (
        best_model
        .named_steps["preprocessor"]
    )

    fitted_rf = (
        best_model
        .named_steps["model"]
    )

    feature_names = (
        fitted_preprocessor
        .get_feature_names_out()
    )

    feature_importance = pd.Series(
        fitted_rf.feature_importances_,
        index=feature_names
    )

    feature_importance = (
        feature_importance
        .sort_values(ascending=False)
        .head(15)
    )

    print("\n========== TOP FEATURES ==========")
    print(feature_importance)

    plt.figure(figsize=(10, 6))

    feature_importance.sort_values().plot(
        kind="barh"
    )

    plt.title(
        "Top 15 Features Influencing Churn"
    )

    plt.xlabel("Importance")

    plt.tight_layout()
    plt.show()


# ============================================
# 22. SAMPLE CUSTOMER PREDICTION
# ============================================

sample_customer = X_test.iloc[[0]]

sample_probability = (
    best_model
    .predict_proba(sample_customer)[0][1]
)

print("\n========== SAMPLE CUSTOMER ==========")

print(
    "Churn Probability:",
    round(sample_probability * 100, 2),
    "%"
)

if sample_probability >= 0.50:

    print("Prediction: LIKELY TO CHURN")

else:

    print("Prediction: LIKELY TO STAY")


# ============================================
# 23. FINAL SUMMARY
# ============================================

print("\n============================================")
print("PROJECT COMPLETED")
print("============================================")

print(
    "Best Model:",
    best_model_name
)

print(
    "ROC-AUC:",
    round(
        roc_auc_score(
            y_test,
            best_probability
        ),
        4
    )
)

print(
    "\nThe model can help identify customers "
    "who are at higher risk of churn."
)