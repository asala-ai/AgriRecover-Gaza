
# 🌱 AgriRecover Gaza

**Deep Learning for Agricultural Vegetation Monitoring and Prediction**

AgriRecover Gaza is an academic deep learning project that uses Sentinel-2 satellite data and an Artificial Neural Network (ANN) to monitor agricultural vegetation and estimate future vegetation conditions in the Gaza Strip, Palestine.

---

## 🚀 Live Interactive Application

Explore the dashboard:

[**Open AgriRecover Gaza Dashboard**](https://agrirecover-gaza-dgyt2m7hxcwnje35rbaagj.streamlit.app/)

---

## 🎯 Project Overview

The project analyzes historical agricultural vegetation indicators extracted from Sentinel-2 satellite imagery using Google Earth Engine (GEE).

The processed monthly dataset is used to train an Artificial Neural Network that predicts the **next month's NDVI** for each agricultural sample, based on its latest available spectral observations.

The interactive Streamlit application provides data exploration, visualization, prediction, and model evaluation.

## 🎯 Project Objectives

- Monitor agricultural vegetation using satellite-derived data.
- Analyze monthly changes in vegetation and spectral indicators.
- Explore differences between agricultural sample locations.
- Predict the next month's NDVI using a trained ANN model.
- Present dataset and model results through an interactive dashboard.

## 🛰️ Dataset

The dataset was derived from **Sentinel-2 satellite imagery** and processed using **Google Earth Engine**.

| Dataset Detail | Description |
|---|---|
| Study Area | Gaza Strip, Palestine |
| Data Period | January 2018 – September 2026 |
| Agricultural Samples | 500 sample IDs |
| Temporal Resolution | Monthly observations |
| Satellite Source | Sentinel-2 |
| Processing Platform | Google Earth Engine |
| Dataset File | `AgriRecover_Final_2018_2026(1).csv` |

### Spectral Indicators

The dataset includes six spectral indicators:

| Indicator | Description |
|---|---|
| **NDVI** | Normalized Difference Vegetation Index |
| **EVI** | Enhanced Vegetation Index |
| **NDMI** | Normalized Difference Moisture Index |
| **SAVI** | Soil-Adjusted Vegetation Index |
| **BSI** | Bare Soil Index |
| **NBR** | Normalized Burn Ratio |

## 🧠 Deep Learning Model

An **Artificial Neural Network (ANN)** is used to estimate the next month's NDVI.

### Model Architecture

| Layer | Configuration |
|---|---|
| Input Layer | 6 spectral features |
| Hidden Layer 1 | 64 neurons, ReLU |
| Hidden Layer 2 | 32 neurons, ReLU |
| Output Layer | 1 predicted NDVI value |

### Training Configuration

| Setting | Value |
|---|---|
| Optimizer | Adam |
| Loss Function | Mean Squared Error (MSE) |
| Epochs | 30 |
| Batch Size | 32 |
| Validation Split | 20% |
| Feature Scaling | StandardScaler |

The application uses the saved trained ANN model and its fitted StandardScaler for prediction.

## 📊 Model Evaluation

The reported evaluation results compare the ANN model with a persistence baseline.

| Metric | ANN Model | Baseline |
|---|---:|---:|
| MAE | 0.0859 | 0.0874 |
| RMSE | 0.1283 | 0.1452 |
| R² | 0.5850 | 0.4683 |

The ANN achieved lower MAE and RMSE values and a higher R² score than the persistence baseline.

- **MAE:** Mean Absolute Error.
- **RMSE:** Root Mean Squared Error.
- **R²:** Coefficient of determination.

These metrics describe regression performance; R² is not classification accuracy.

## 🖥️ Dashboard Features

The interactive application includes:

- **Overview:** Dataset statistics and overall vegetation trends.
- **Data Analysis:** Sample-level spectral trends, monthly index comparisons, and dataset preview.
- **AI Prediction:** Single-sample and all-sample NDVI predictions, with CSV export.
- **Model Performance:** Evaluation metrics, baseline comparison, model architecture, and training configuration.
- **Data Quality:** Missing values, duplicate records, monthly coverage gaps, and EVI values requiring review.
- **About Project:** Project objectives, workflow, data sources, and limitations.

## ⚙️ Technologies Used

- Python
- Streamlit
- TensorFlow / Keras
- NumPy
- Pandas
- Scikit-learn
- Joblib
- Plotly
- Google Earth Engine
- Sentinel-2 Satellite Data

## 🔄 Project Workflow

1. Obtain Sentinel-2 satellite imagery.
2. Process imagery and calculate spectral indicators using Google Earth Engine.
3. Prepare the monthly agricultural dataset.
4. Prepare and scale model input features.
5. Train and evaluate the ANN model.
6. Save the trained model and fitted scaler.
7. Integrate the dataset and saved model into the Streamlit dashboard.

## ⚠️ Scope and Limitations

- The model estimates a numeric NDVI value for the month following each sample's latest available observation.
- Predictions are model estimates, not actual satellite observations.
- The application does not classify land as damaged, healthy, recovered, or unrecovered.
- Geographic sample mapping requires the original sample coordinates exported from Google Earth Engine.
- Live satellite imagery and live Google Earth Engine authentication are not connected to the current application.

## 📚 Data Sources and References

- [European Space Agency – Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2)
- [Google Earth Engine – Sentinel-2 SR Harmonized](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
- [TensorFlow / Keras Documentation](https://www.tensorflow.org/guide/keras)
- [Scikit-learn StandardScaler Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)

---

## 🔗 Project Links

- **Live Application:** [AgriRecover Gaza Dashboard](https://agrirecover-gaza-dgyt2m7hxcwnje35rbaagj.streamlit.app/)
- **GitHub Repository:** [asala-ai/AgriRecover-Gaza](https://github.com/asala-ai/AgriRecover-Gaza)

---

**AgriRecover Gaza**

*An academic project for deep learning and agricultural vegetation monitoring in the Gaza Strip.*
