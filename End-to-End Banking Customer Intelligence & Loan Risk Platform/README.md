# End-to-End Banking Customer Intelligence & Loan Risk Platform

An end-to-end data science platform that combines customer segmentation, credit default prediction, explainable AI, banking analytics, and marketing campaign intelligence.

## Project Overview

This project analyzes multiple banking datasets to provide actionable insights across three major business areas:

1. Customer Intelligence
2. Credit Risk Assessment
3. Marketing Campaign Intelligence

The project uses Python, SQL-oriented analytical thinking, machine learning, clustering, and explainable AI to transform raw banking data into business-ready insights.

---

## Business Objectives

### Customer Intelligence
- Segment customers using behavioral transaction patterns
- Identify high-value, dormant, active, and at-risk customer groups
- Analyze customer spending and transaction behavior

### Credit Risk
- Predict probability of credit-card default
- Compare multiple machine learning models
- Assign customers to risk categories
- Explain model predictions using SHAP

### Marketing Intelligence
- Analyze bank campaign conversion rates
- Identify high-converting customer profiles
- Evaluate campaign contact effectiveness
- Analyze previous campaign outcomes
- Study customer engagement through call duration

---

# Project Architecture

```text
Banking Data
     |
     +----------------------+
     |                      |
     v                      v
Customer Transactions    Credit History
     |                      |
     v                      v
RFM Feature Engineering  Feature Engineering
     |                      |
     v                      v
K-Means Clustering       ML Models
     |                      |
     v                      v
Customer Segments        Risk Prediction
                            |
                            v
                         SHAP
                            |
                            +----------------+
                                             |
Bank Marketing Data                           |
     |                                        |
     v                                        |
Campaign Analysis                             |
     |                                        |
     +----------------+-----------------------+
                      |
                      v
             Executive Analytics
                  Dashboard
