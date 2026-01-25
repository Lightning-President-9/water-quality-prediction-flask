# water-quality-prediction-flask – Interactive Dashboard

An interactive **machine learning–based dashboard** for predicting and visualizing river water quality parameters using historical monitoring data.  
This project integrates **data analysis, machine learning, and interactive visualization** to present pollutant predictions in an intuitive and responsive dashboard.

---

## Project Overview

This is a **personal project** developed to explore how machine learning models can be applied to environmental datasets.

A **multi-output Random Forest Regressor** is trained on historical river water quality data and used to predict key pollutant concentrations for selected monitoring stations and years.  
The results are presented through interactive Plotly visualizations in a web-based dashboard.

---

## Predicted Water Quality Parameters

The dashboard predicts the following pollutants:

- **O₂ (Dissolved Oxygen)**
- **NO₃ (Nitrate)**
- **NO₂ (Nitrite)**
- **SO₄ (Sulfate)**
- **PO₄ (Phosphate)**
- **Cl (Chloride)**

Each prediction is compared against standard acceptable limits.

---

## Dashboard Features

- Year-based and station-based predictions
- Station ID range limited to **1–22**
- 4-digit year validation
- Interactive visualizations:
  - Prediction summary table
  - Radar chart (normalized predicted vs limit)
  - Gauge charts for individual pollutants
  - Bullet charts comparing predicted values with safe thresholds

---

## Machine Learning Model

- **Model:** Random Forest Regressor (Multi-Output)
- **Training:** Jupyter Notebook
- **Approach:**
  - Feature engineering
  - One-hot encoding of station IDs
  - Multi-output regression
  - Prediction of multiple pollutants simultaneously

---

## Dataset

- **Source:** Kaggle  
  https://www.kaggle.com/datasets/vbmokin/wq-southern-bug-river-01052021
- **Description:** Historical water quality measurements from river monitoring stations

---

## Jupyter Notebook

Model training, exploratory data analysis, and evaluation are documented in the notebook:

https://github.com/Lightning-President-9/Water-Quality-Prediction/blob/main/Week_2/Water_Quality_Prediction.ipynb

---

## Parameter Description PDF

PDF for parameter meaning and limits:

https://github.com/Lightning-President-9/Water-Quality-Prediction/blob/main/Parameters_WQM_RMS.pdf

---

## Deployment Link

Deployed Link:

https://water-quality-prediction-flask.onrender.com

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Visualization:** Plotly
- **Machine Learning:** scikit-learn
- **Deployment:** OnRender

---

## ⚠Disclaimer

This project is a **personal academic and learning project**.

Predictions are **indicative only** and are based on historical data and machine learning models.  
They **must not be used for regulatory, health, or environmental decision-making** and should not replace certified laboratory water quality testing.