🌱 AgriRecover Gaza

Deep Learning for Agricultural Vegetation Monitoring and Prediction in Gaza

<p align="center">
  <a href="https://agrirecover-gaza-dgyt2m7hxcwnje35rbaagj.streamlit.app/">
    <strong>🚀 Open the Live Interactive Application</strong>
  </a>
</p><p align="center">
  An academic deep learning project using Sentinel-2 satellite data and Artificial Neural Networks (ANN) to monitor agricultural vegetation and predict future NDVI values in the Gaza Strip, Palestine.
</p>---

🌍 Project Overview

AgriRecover Gaza is an academic deep learning project designed to analyze agricultural vegetation conditions in the Gaza Strip using satellite-derived spectral indicators.

The project uses Sentinel-2 satellite imagery processed through Google Earth Engine (GEE) to create a monthly agricultural dataset. An Artificial Neural Network (ANN) is then trained to predict the next month's Normalized Difference Vegetation Index (NDVI).

The project provides an interactive Streamlit dashboard for exploring vegetation trends, analyzing spectral indicators, reviewing data quality, and viewing AI-based predictions.

🎯 Project Objectives

- Monitor agricultural vegetation using satellite-derived data.
- Analyze historical vegetation trends across agricultural sample locations.
- Examine six spectral indicators to understand vegetation and soil conditions.
- Develop an ANN model to predict next-month NDVI values.
- Provide an interactive platform for data exploration and model evaluation.

📊 Dataset Overview

Description| Details
Study Area| Gaza Strip, Palestine
Satellite Source| Sentinel-2
Processing Platform| Google Earth Engine
Data Period| January 2018 – September 2026
Total Records| 52,440
Agricultural Samples| 500
Spectral Indicators| 6
Dataset Format| CSV

Spectral Indicators

The dataset includes six spectral indicators:

- NDVI: Normalized Difference Vegetation Index.
- EVI: Enhanced Vegetation Index.
- NDMI: Normalized Difference Moisture Index.
- SAVI: Soil-Adjusted Vegetation Index.
- BSI: Bare Soil Index.
- NBR: Normalized Burn Ratio.

🧠 Deep Learning Model

The project uses an Artificial Neural Network (ANN) to estimate the next month's NDVI.

Model Architecture

Layer| Configuration
Input Layer| 6 Features
Hidden Layer 1| 64 Neurons – ReLU
Hidden Layer 2| 32 Neurons – ReLU
Output Layer| 1 Value – Predicted NDVI

Training Configuration

- Optimizer: Adam
- Loss Function: Mean Squared Error (MSE)
- Epochs: 30
- Batch Size: 32
- Validation Split: 20%
- Input Scaling: StandardScaler

The trained model and fitted scaler are saved and reused by the interactive application.

📈 Model Evaluation

The ANN model was evaluated against a persistence baseline.

Metric| ANN Model| Baseline
MAE| 0.0859| 0.0874
RMSE| 0.1283| 0.1452
R²| 0.5850| 0.4683

Performance Improvement

- MAE Reduction: 1.72%
- RMSE Reduction: 11.64%
- R² Improvement: +0.1167

The ANN model achieved better results than the persistence baseline across all three reported evaluation metrics.

Note: R² measures explanatory performance, not classification accuracy. Further validation is needed before operational use.

🖥️ Interactive Application Features

The Streamlit dashboard includes six main sections:

1. Overview: Project statistics, vegetation trends, spectral indicators, and workflow.
2. Data Analysis: Interactive charts for exploring spectral indices and individual agricultural samples.
3. AI Prediction: Single-sample and multi-sample next-month NDVI predictions.
4. Model Performance: ANN architecture, training configuration, and baseline comparison.
5. Data Quality: Missing values, duplicate records, monthly coverage, and potential data issues.
6. About Project: Project objectives, methodology, technologies, and limitations.

⚙️ Technologies Used

- Python
- TensorFlow / Keras
- NumPy
- Pandas
- Scikit-learn
- Joblib
- Plotly
- Streamlit
- Google Earth Engine
- Sentinel-2 Satellite Data

📁 Project Structure

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
│   └── AgriRecover_Final_2018_2026(1).csv
│
├── model/
│   ├── AgriRecover_ANN_Model.keras
│   └── AgriRecover_Scaler.pkl
│
├── gee/
│   ├── AgriRecover_GEE.js
│   └── Sample_Coordinates.js
│
├── assets/
│
├── docs/
│
├── requirements.txt
│
└── README.md

🚀 Run the Application Locally

1. Clone the repository

git clone https://github.com/asala-ai/AgriRecover-Gaza.git
cd AgriRecover-Gaza

2. Install dependencies

pip install -r requirements.txt

3. Run Streamlit

streamlit run app.py

The application will open in your local browser.

⚠️ Scope and Limitations

- The model predicts a numerical NDVI value for the month following each sample's latest available observation.
- The model does not directly classify agricultural land as damaged, healthy, recovered, or unrecovered.
- Geographic mapping requires the original sample coordinates exported from Google Earth Engine.
- Live satellite imagery and live Google Earth Engine authentication are not connected to the current application version.
- Predictions are model estimates and should not be interpreted as actual satellite observations.

📚 Data Sources and Documentation

- "European Space Agency – Sentinel-2" (https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2)
- "Google Earth Engine – Sentinel-2 SR Harmonized" (https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
- "TensorFlow / Keras Documentation" (https://www.tensorflow.org/guide/keras)
- "Scikit-learn StandardScaler" (https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)

---

🌱 Project Access

Live Interactive Dashboard:

https://agrirecover-gaza-dgyt2m7hxcwnje35rbaagj.streamlit.app/

Project Repository:

https://github.com/asala-ai/AgriRecover-Gaza

---

<p align="center">
  <strong>AgriRecover Gaza</strong><br/>
  Deep Learning • Remote Sensing • Agricultural Vegetation Monitoring<br/>
  Gaza Strip, Palestine
</p>
