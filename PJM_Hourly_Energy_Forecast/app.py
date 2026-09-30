
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import timedelta


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PJM Energy Demand Forecast",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "final_xgboost_model.pkl"
DATA_PATH = BASE_DIR / "data" / "processed" / "PJMW_MW_Hourly_Cleaned.csv"


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Datetime"])
    df = df.sort_values("Datetime").reset_index(drop=True)
    return df


# ============================================================
# FEATURE CREATION
# ============================================================

def create_features(df):

    data = df.copy()

    data["Year"] = data["Datetime"].dt.year
    data["Month"] = data["Datetime"].dt.month
    data["Day"] = data["Datetime"].dt.day
    data["Hour"] = data["Datetime"].dt.hour
    data["DayOfWeek"] = data["Datetime"].dt.dayofweek
    data["IsWeekend"] = (data["DayOfWeek"] >= 5).astype(int)

    data["Lag_1H"] = data["PJMW_MW"].shift(1)
    data["Lag_24H"] = data["PJMW_MW"].shift(24)
    data["Lag_48H"] = data["PJMW_MW"].shift(48)
    data["Lag_168H"] = data["PJMW_MW"].shift(168)

    data["Rolling_Mean_24H"] = (
        data["PJMW_MW"]
        .shift(1)
        .rolling(24)
        .mean()
    )

    data["Rolling_Mean_168H"] = (
        data["PJMW_MW"]
        .shift(1)
        .rolling(168)
        .mean()
    )

    data["Rolling_Std_24H"] = (
        data["PJMW_MW"]
        .shift(1)
        .rolling(24)
        .std()
    )

    data["Hour_Sin"] = np.sin(2 * np.pi * data["Hour"] / 24)
    data["Hour_Cos"] = np.cos(2 * np.pi * data["Hour"] / 24)

    data["DayOfWeek_Sin"] = np.sin(
        2 * np.pi * data["DayOfWeek"] / 7
    )

    data["DayOfWeek_Cos"] = np.cos(
        2 * np.pi * data["DayOfWeek"] / 7
    )

    data["Month_Sin"] = np.sin(
        2 * np.pi * data["Month"] / 12
    )

    data["Month_Cos"] = np.cos(
        2 * np.pi * data["Month"] / 12
    )

    return data


# ============================================================
# FUTURE FEATURE CREATION
# ============================================================

def create_future_features(history, timestamp):

    values = history["PJMW_MW"].values

    row = {
        "Year": timestamp.year,
        "Month": timestamp.month,
        "Day": timestamp.day,
        "Hour": timestamp.hour,
        "DayOfWeek": timestamp.dayofweek,
        "IsWeekend": int(timestamp.dayofweek >= 5),

        "Lag_1H": values[-1],
        "Lag_24H": values[-24],
        "Lag_48H": values[-48],
        "Lag_168H": values[-168],

        "Rolling_Mean_24H": np.mean(values[-24:]),
        "Rolling_Mean_168H": np.mean(values[-168:]),
        "Rolling_Std_24H": np.std(values[-24:], ddof=1),

        "Hour_Sin": np.sin(2 * np.pi * timestamp.hour / 24),
        "Hour_Cos": np.cos(2 * np.pi * timestamp.hour / 24),

        "DayOfWeek_Sin": np.sin(
            2 * np.pi * timestamp.dayofweek / 7
        ),

        "DayOfWeek_Cos": np.cos(
            2 * np.pi * timestamp.dayofweek / 7
        ),

        "Month_Sin": np.sin(
            2 * np.pi * timestamp.month / 12
        ),

        "Month_Cos": np.cos(
            2 * np.pi * timestamp.month / 12
        )
    }

    return pd.DataFrame([row])


# ============================================================
# GENERATE FORECAST
# ============================================================

def generate_forecast(model, historical_data, periods=720):

    history = historical_data[
        ["Datetime", "PJMW_MW"]
    ].copy()

    history = history.sort_values("Datetime").reset_index(drop=True)

    feature_columns = [
        "Year",
        "Month",
        "Day",
        "Hour",
        "DayOfWeek",
        "IsWeekend",
        "Lag_1H",
        "Lag_24H",
        "Lag_48H",
        "Lag_168H",
        "Rolling_Mean_24H",
        "Rolling_Mean_168H",
        "Rolling_Std_24H",
        "Hour_Sin",
        "Hour_Cos",
        "DayOfWeek_Sin",
        "DayOfWeek_Cos",
        "Month_Sin",
        "Month_Cos"
    ]

    last_timestamp = history["Datetime"].iloc[-1]

    future_timestamps = pd.date_range(
        start=last_timestamp + timedelta(hours=1),
        periods=periods,
        freq="h"
    )

    forecasts = []

    for timestamp in future_timestamps:

        features = create_future_features(
            history,
            timestamp
        )

        prediction = model.predict(
            features[feature_columns]
        )[0]

        prediction = max(0, float(prediction))

        forecasts.append(prediction)

        history.loc[len(history)] = [
            timestamp,
            prediction
        ]

    forecast_df = pd.DataFrame({
        "Datetime": future_timestamps,
        "Predicted_PJMW_MW": forecasts
    })

    return forecast_df


# ============================================================
# APPLICATION
# ============================================================

st.title("⚡ PJM Energy Demand Forecast")

st.write(
    "30-day hourly electricity demand forecasting "
    "using an XGBoost time-series machine learning model."
)


# Load model and data

try:

    model = load_model()
    historical_data = load_data()

except Exception as e:

    st.error(f"Error loading project files: {e}")
    st.stop()


# ============================================================
# PROJECT INFORMATION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Historical Records",
        f"{len(historical_data):,}"
    )

with col2:
    st.metric(
        "Model",
        "XGBoost"
    )

with col3:
    st.metric(
        "Forecast Horizon",
        "30 Days"
    )

with col4:
    st.metric(
        "Forecast Points",
        "720"
    )


# ============================================================
# GENERATE FORECAST
# ============================================================

with st.spinner("Generating 30-day forecast..."):

    forecast_df = generate_forecast(
        model,
        historical_data,
        periods=720
    )


# ============================================================
# FORECAST SUMMARY
# ============================================================

st.subheader("30-Day Forecast Summary")

avg_demand = forecast_df["Predicted_PJMW_MW"].mean()
min_demand = forecast_df["Predicted_PJMW_MW"].min()
max_demand = forecast_df["Predicted_PJMW_MW"].max()

peak_row = forecast_df.loc[
    forecast_df["Predicted_PJMW_MW"].idxmax()
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Demand",
        f"{avg_demand:,.0f} MW"
    )

with col2:
    st.metric(
        "Minimum Demand",
        f"{min_demand:,.0f} MW"
    )

with col3:
    st.metric(
        "Maximum Demand",
        f"{max_demand:,.0f} MW"
    )

with col4:
    st.metric(
        "Peak Forecast",
        peak_row["Datetime"].strftime("%d %b %Y %H:%M")
    )


# ============================================================
# HOURLY FORECAST GRAPH
# ============================================================

st.subheader("Hourly Energy Demand Forecast")

chart_data = forecast_df.set_index("Datetime")[
    ["Predicted_PJMW_MW"]
]

st.line_chart(chart_data)


# ============================================================
# DAILY FORECAST
# ============================================================

daily_forecast = (
    forecast_df
    .set_index("Datetime")
    .resample("D")["Predicted_PJMW_MW"]
    .agg(
        Average_Demand="mean",
        Minimum_Demand="min",
        Maximum_Demand="max"
    )
)

st.subheader("Daily Forecast")

st.line_chart(
    daily_forecast[["Average_Demand"]]
)


# ============================================================
# DAILY FORECAST TABLE
# ============================================================

st.subheader("Daily Forecast Summary")

display_daily = daily_forecast.reset_index()

display_daily["Datetime"] = (
    display_daily["Datetime"]
    .dt.strftime("%Y-%m-%d")
)

st.dataframe(
    display_daily,
    width='stretch',
    hide_index=True
)


# ============================================================
# DOWNLOAD FORECAST
# ============================================================

csv_data = forecast_df.to_csv(index=False)

st.download_button(
    label="Download 30-Day Forecast CSV",
    data=csv_data,
    file_name="pjm_30_day_hourly_forecast.csv",
    mime="text/csv"
)


# ============================================================
# MODEL INFORMATION
# ============================================================

st.subheader("Model Information")

st.write(
    "The final XGBoost model was selected after comparing "
    "multiple hourly forecasting models."
)

st.write(
    "**Test-set performance:**"
)

st.write(
    "- MAE: 53.05 MW"
)

st.write(
    "- RMSE: 70.93 MW"
)

st.write(
    "- R²: 0.9949"
)

st.write(
    "- MAPE: 0.95%"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "PJM Hourly Energy Demand Forecasting Project | "
    "XGBoost Time-Series Forecasting"
)
