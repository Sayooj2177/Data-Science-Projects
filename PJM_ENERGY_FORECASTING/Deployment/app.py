import os
import json

import holidays
import pandas as pd
import streamlit as st

st.set_page_config(page_title="PJM Energy Forecast", page_icon="⚡", layout="wide")

MODEL_PREFIX = {"XGBoost": "pjm_xgboost", "SARIMAX": "pjm_sarimax"}
PAGES = ["Overview", "Model Performance", "30-Day Forecast", "Forecast Data"]

# ---------------- Sidebar ----------------
st.sidebar.markdown("## ⚡ PJM Energy Forecast")
model_name = st.sidebar.radio("Select model:", list(MODEL_PREFIX), key="model")
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", PAGES, key="page")

prefix = MODEL_PREFIX[model_name]
FILES = [
    f"{prefix}_hourly_forecast.csv",
    f"{prefix}_daily_forecast.csv",
    f"{prefix}_model_results.csv",
    f"{prefix}_actual_vs_predicted.csv",
    f"{prefix}_metadata.json",
]
missing = [f for f in FILES if not os.path.exists(f)]
if missing:
    st.error(f"Missing files for {model_name}: " + ", ".join(missing) +
             ". Please re-run the notebook cells that save the deployment files.")
    st.stop()


@st.cache_data
def load_data(prefix):
    hourly = pd.read_csv(f"{prefix}_hourly_forecast.csv", parse_dates=["Datetime"])
    daily = pd.read_csv(f"{prefix}_daily_forecast.csv", parse_dates=["Date"])
    results = pd.read_csv(f"{prefix}_model_results.csv")
    avp = pd.read_csv(f"{prefix}_actual_vs_predicted.csv", parse_dates=["Datetime"])
    with open(f"{prefix}_metadata.json") as f:
        meta = json.load(f)
    return hourly, daily, results, avp, meta


hourly, daily, results, avp, meta = load_data(prefix)

# ---------------- Page 1: Overview ----------------
if page == "Overview":
    st.title(f"⚡ PJM Hourly Energy Consumption Forecast: {model_name}")
    st.write(f"{model_name} based forecasting of PJM electricity consumption for the next 30 days.")

    st.header("Project Overview")
    st.write("The objective of this project is to analyze historical PJM electricity consumption "
             "data and forecast future energy consumption.")
    for para in meta["overview"]:
        st.write(para)
    st.write(f"{meta['model_label']} is the model used for the forecast shown on these pages.")

    st.header("Forecast Summary")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Forecast Hours", len(hourly))
    c2.metric("Forecast Days", len(hourly) // 24)
    c3.metric("Average MW", f"{hourly['Predicted_MW'].mean():.2f}")
    c4.metric("Maximum MW", f"{hourly['Predicted_MW'].max():.2f}")
    c5.metric("Minimum MW", f"{hourly['Predicted_MW'].min():.2f}")

    st.header("Daily Forecast")
    st.line_chart(daily.set_index("Date")["Average_Predicted_MW"])

# ---------------- Page 2: Model Performance ----------------
elif page == "Model Performance":
    st.title(f"📊 Model Performance: {model_name}")
    st.write(f"Evaluation results of the {model_name} model.")

    metric_cols = ["Evaluation", "MAE", "RMSE", "MAPE (%)", "R2 (%)"]
    st.dataframe(results[metric_cols])
    if meta.get("results_note"):
        st.caption(meta["results_note"])

    st.header(meta.get("avp_title", "Actual vs Predicted"))
    st.line_chart(avp.set_index("Datetime")[["Actual_MW", "Predicted_MW"]])

    if meta.get("feature_importance"):
        st.header("Feature Importance")
        fi = (pd.Series(meta["feature_importance"], name="Importance")
              .sort_values(ascending=False).to_frame())
        st.bar_chart(fi)

    st.header("Final Model")
    st.success(f"{meta['model_label']} is the model used for this forecast.")
    for _, r in results.iterrows():
        st.markdown(f"**{r['Evaluation']}**")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("MAE", f"{r['MAE']:.2f} MW")
        m2.metric("RMSE", f"{r['RMSE']:.2f} MW")
        m3.metric("MAPE", f"{r['MAPE (%)']:.2f}%")
        m4.metric("R²", f"{r['R2 (%)']:.2f}%")

    st.header("Model Information")
    for k, v in meta["details"].items():
        st.write(f"**{k}:** {v}")
    for note in meta.get("notes", []):
        st.info(note)

# ---------------- Page 3: 30-Day Forecast ----------------
elif page == "30-Day Forecast":
    st.title(f"📈 30-Day Energy Consumption Forecast: {model_name}")

    st.header("Hourly Forecast")
    st.line_chart(hourly.set_index("Datetime")["Predicted_MW"])

    st.header("Daily Average Forecast")
    st.line_chart(daily.set_index("Date")["Average_Predicted_MW"])

# ---------------- Page 4: Forecast Data ----------------
else:
    st.title(f"📋 Forecast Data: {model_name}")
    st.write("Hourly energy consumption predictions for the next 30 days.")

    us_holidays = holidays.US()
    table = hourly.copy()
    table["Hour"] = table["Datetime"].dt.hour
    table["DayOfWeek"] = table["Datetime"].dt.dayofweek
    table["Month"] = table["Datetime"].dt.month
    table["Year"] = table["Datetime"].dt.year
    table["IsWeekend"] = (table["DayOfWeek"] >= 5).astype(int)
    table["IsHoliday"] = table["Datetime"].dt.date.apply(lambda d: d in us_holidays).astype(int)
    table["Predicted_MW"] = table["Predicted_MW"].round(2)
    table = table[["Datetime", "Hour", "DayOfWeek", "Month", "Year",
                   "IsWeekend", "IsHoliday", "Predicted_MW"]]

    st.dataframe(table)
    st.download_button(
        "Download forecast as CSV",
        table.to_csv(index=False).encode("utf-8"),
        file_name=f"{prefix}_30_day_forecast.csv",
        mime="text/csv",
        key=f"download_{prefix}",
    )
