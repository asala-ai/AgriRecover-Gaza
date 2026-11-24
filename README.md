🌱 AgriRecover Gaza

Deep Learning for Agricultural Vegetation Monitoring and Prediction

<p align="center">
  <a href="https://agrirecover-gaza-dgyt2m7hxcwnje35rbaagj.streamlit.app/">
    <strong>🚀 OPEN LIVE INTERACTIVE DASHBOARD</strong>
  </a>
</p>AgriRecover Gaza is an academic deep learning project that uses Sentinel-2 satellite data and Artificial Neural Networks (ANN) to monitor agricultural vegetation and forecast future NDVI values in the Gaza Strip, Palestine.

---

1. Project Overview

The project analyzes historical agricultural vegetation indicators extracted from Sentinel-2 satellite imagery using Google Earth Engine (GEE).

A monthly dataset is used to train an Artificial Neural Network that predicts the next month's Normalized Difference Vegetation Index (NDVI).

The project also provides an interactive Streamlit dashboard for data analysis, visualization, prediction, and model evaluation.

2. Project Objectives

- Monitor agricultural vegetation using satellite data.
- Analyze historical vegetation changes.
- Explore spectral indicators related to vegetation and soil conditions.
- Develop a deep learning model for next-month NDVI prediction.
- Provide an interactive platform for exploring results.

3. Dataset

Property| Description
Study Area| Gaza Strip, Palestine
Satellite| Sentinel-2
Processing Platform| Google Earth Engine
Data Period| January 2018 – September 2026
Total Records| 52,440
Sample Points| 500
Spectral Indicators| 6
Format| CSV

Spectral Indicators

Indicator| Description
NDVI| Vegetation greenness and density
EVI| Enhanced Vegetation Index
NDMI| Vegetation moisture
SAVI| Soil-Adjusted Vegetation Index
BSI| Bare Soil Index
NBR| Normalized Burn Ratio

4. Deep Learning Model

The project uses an Artificial Neural Network (ANN) to predict the next month's NDVI.

Architecture

Layer| Configuration
Input| 6 Features
Hidden Layer 1| 64 Neurons – ReLU
Hidden Layer 2| 32 Neurons – ReLU
Output| 1 Predicted NDVI Value

Training Configuration

- Optimizer: Adam
- Loss Function: Mean Squared Error (MSE)
- Epochs: 30
- Batch Size: 32
- Validation Split: 20%
- Input Scaling: StandardScaler

5. Model Evaluation

The ANN model was compared with a persistence baseline.

Metric| ANN| Baseline
MAE| 0.0859| 0.0874
RMSE| 0.1283| 0.1452
R²| 0.5850| 0.4683

Performance Improvement

- MAE Reduction: 1.72%
- RMSE Reduction: 11.64%
- R² Improvement: +0.1167

The ANN achieved better results than the baseline across all three evaluation metrics.

6. Interactive Dashboard

The Streamlit application provides six main sections:

1. Overview: Project statistics and vegetation trends.
2. Data Analysis: Interactive spectral index and sample-level analysis.
3. AI Prediction: Single-sample and multiple-sample NDVI forecasts.
4. Model Performance: Evaluation metrics and ANN architecture.
5. Data Quality: Missing values, duplicate records, and data coverage.
6. About Project: Objectives, technologies, and project limitations.

7. Technologies

- Python
- TensorFlow / Keras
- NumPy and Pandas
- Scikit-learn
- Joblib
- Plotly
- Streamlit
- Google Earth Engine
- Sentinel-2 Satellite Data

8. Project Structure

AgriRecover-Gaza/
│
├── app.py
│
├── app/
│   └── app/
│       ├── components/
│       ├── pages/
│       └── utils/
│
├── data/
│   ├── AgriRecover_Final_2018_2026(1).csv
│   └── README.md
│
├── model/
│   ├── AgriRecover_ANN_Model.keras
│   ├── AgriRecover_Scaler.pkl
│   └── README.md
│
├── gee/
│   ├── AgriRecover_GEE.js
│   ├── Sample_Coordinates.js
│   └── README.md
│
├── assets/
│   └── README.md
│
├── docs/
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── README.md

9. Run Locally

Clone the repository:

git clone https://github.com/asala-ai/AgriRecover-Gaza.git
cd AgriRecover-Gaza

Install the required packages:

pip install -r requirements.txt

Run the application:

streamlit run app.py

10. Scope and Limitations

- The model predicts a numerical NDVI value for the month following each sample's latest available observation.
- It does not directly classify land as damaged, healthy, recovered, or unrecovered.
- Geographic mapping requires the original sample coordinates.
- Live satellite imagery and live Google Earth Engine authentication are not connected to the current application.
- Predictions are model estimates, not actual satellite observations.

11. Data Sources

- "European Space Agency – Sentinel-2" (https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2)
- "Google Earth Engine – Sentinel-2 SR Harmonized" (https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
- "TensorFlow / Keras" (https://www.tensorflow.org/guide/keras)
- "Scikit-learn StandardScaler" (https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)

---

<p align="center">
  <strong>AgriRecover Gaza</strong><br>
  Deep Learning • Remote Sensing • Agricultural Vegetation Monitoring<br>
  Gaza Strip, Palestine
</p>
