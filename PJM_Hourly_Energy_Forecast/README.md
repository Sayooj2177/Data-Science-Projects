# PJM Hourly Energy Demand Forecasting

## Project Overview

This project focuses on forecasting hourly electricity demand using the PJM energy consumption dataset.

The project follows an end-to-end machine learning and time-series forecasting workflow, including data cleaning, exploratory data analysis, feature engineering, model development, model comparison, model selection, and 30-day future forecasting.

The final selected model is an **XGBoost Regressor**.

---

## Objectives

- Clean and preprocess hourly energy-demand data
- Handle timestamp issues, duplicate timestamps, missing hourly observations, and abnormal values
- Perform comprehensive Exploratory Data Analysis (EDA)
- Identify daily, weekly, monthly, and seasonal demand patterns
- Perform time-series analysis
- Create lag, rolling, and cyclic time features
- Compare multiple forecasting models
- Select the best-performing hourly forecasting model
- Generate a 30-day hourly energy-demand forecast
- Build an interactive Streamlit forecasting application

---

## Dataset

The dataset contains hourly PJM electricity demand data with the following columns:

- `Datetime` — Timestamp of the observation
- `PJMW_MW` — Electricity demand in megawatts (MW)

### Dataset after cleaning

- Records: **143,232**
- Frequency: **Hourly**
- Start: **2002-04-01**
- End: **2018-08-03**
- Missing target values: **0**
- Duplicate timestamps: **0**

---

## Data Cleaning

The following data-quality issues were addressed:

1. Converted the datetime column to the correct datetime format.
2. Converted energy-demand values to numeric format.
3. Sorted the data chronologically.
4. Identified and handled duplicate timestamps.
5. Reindexed the dataset to a continuous hourly timeline.
6. Handled missing hourly observations associated with daylight-saving-time transitions.
7. Identified an isolated abnormal energy-demand value.
8. Corrected the isolated abnormal value using time-based interpolation.
9. Verified that the final dataset contains continuous one-hour intervals.

The cleaned dataset was saved as:

`data/processed/PJMW_MW_Hourly_Cleaned.csv`

---

## Exploratory Data Analysis

The EDA examined:

- Overall energy-demand trends
- Yearly demand patterns
- Monthly demand patterns
- Hourly demand patterns
- Day-of-week patterns
- Weekend vs weekday demand
- Seasonal demand
- Rolling mean and rolling standard deviation
- Autocorrelation
- Stationarity
- Time-series decomposition
- Residual analysis
- Potential outliers

The analysis identified strong daily and weekly patterns and significant temporal dependence in electricity demand.

---

## Feature Engineering

The following features were created for forecasting:

### Calendar Features

- Year
- Month
- Day
- Hour
- DayOfWeek
- IsWeekend

### Lag Features

- Lag_1H
- Lag_24H
- Lag_48H
- Lag_168H

### Rolling Features

- Rolling_Mean_24H
- Rolling_Mean_168H
- Rolling_Std_24H

### Cyclic Features

- Hour_Sin
- Hour_Cos
- DayOfWeek_Sin
- DayOfWeek_Cos
- Month_Sin
- Month_Cos

---

## Models Evaluated

The following hourly forecasting approaches were evaluated:

- Seasonal Naive
- Random Forest
- XGBoost
- LightGBM

Classical time-series models were also evaluated on the daily aggregated series:

- ARIMA
- SARIMA
- SARIMAX
- Holt-Winters

---

## Hourly Model Comparison

| Model | MAE (MW) | RMSE (MW) | R² | MAPE |
|---|---:|---:|---:|---:|
| Seasonal Naive | 584.98 | 779.93 | 0.3852 | 10.34% |
| Random Forest | 81.03 | 108.15 | 0.9882 | 1.45% |
| **XGBoost** | **53.05** | **70.93** | **0.9949** | **0.95%** |
| LightGBM | 56.75 | 74.21 | 0.9944 | 1.02% |

---

## Final Model

### XGBoost

XGBoost was selected as the final hourly forecasting model based on the evaluation results.

### Test-set Performance

- **MAE:** 53.05 MW
- **RMSE:** 70.93 MW
- **R²:** 0.9949
- **MAPE:** 0.95%

The final model was subsequently trained using the complete feature-engineered dataset.

The trained model is stored at:

`models/final_xgboost_model.pkl`

---

## 30-Day Forecast

The final XGBoost model was used to generate a recursive 30-day hourly forecast.

### Forecast Details

- Forecast horizon: **30 days**
- Forecast points: **720 hours**
- Minimum predicted demand: **3,970.61 MW**
- Maximum predicted demand: **7,953.56 MW**
- Average predicted demand: **5,964.46 MW**
- Peak forecast: **7,953.56 MW**
- Peak forecast timestamp: **2018-08-17 17:00:00**

The forecast was saved to:

`outputs/forecasts/pjm_30_day_hourly_forecast.csv`

---

## Project Structure

```text
PJM_Hourly_Energy_Forecast/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│       └── PJMW_MW_Hourly_Cleaned.csv
│
├── models/
│   └── final_xgboost_model.pkl
│
├── outputs/
│   ├── eda/
│   ├── modeling/
│   └── forecasts/
│
└── notebook/
    └── PJM_Hourly_Energy_Forecast.ipynb
```

---

## Streamlit Application

The project includes a Streamlit application that provides:

- Historical dataset information
- XGBoost model information
- 30-day hourly forecast
- Hourly forecast visualization
- Daily forecast visualization
- Daily forecast summary
- Forecast CSV download
- Model performance metrics

The Streamlit application is contained in:

`app.py`

---

## Conclusion

The PJM hourly energy consumption dataset was successfully cleaned, analyzed, and prepared for time-series forecasting.

The analysis identified strong daily, weekly, monthly, and seasonal patterns in energy demand. Multiple forecasting approaches were evaluated, and XGBoost achieved the strongest results among the evaluated hourly forecasting models.

The final XGBoost model achieved an MAE of **53.05 MW**, RMSE of **70.93 MW**, R² of **0.9949**, and MAPE of **0.95%** on the chronological test set.

The final model was then used to generate a 30-day hourly forecast containing 720 predictions.

This project demonstrates an end-to-end energy-demand forecasting workflow from raw data cleaning and exploratory analysis through machine-learning model development, evaluation, future forecasting, and Streamlit application development.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- XGBoost
- LightGBM
- Statsmodels
- Joblib
- Streamlit
- Google Colab
- GitHub

---

## Author

**Sayooj Chandran P.**