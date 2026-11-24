🌱 AgriRecover Gaza

Deep Learning for Agricultural Vegetation Monitoring and Prediction

🚀 Live Interactive Application

"Open AgriRecover Gaza Dashboard" (https://agrirecover-gaza-dgyt2m7hxcwnje35rbaagj.streamlit.app/)

---

1.  Project Overview

AgriRecover Gaza is an academic deep learning project that uses Sentinel-2 satellite data and Artificial Neural Networks (ANN) to monitor agricultural vegetation and predict future NDVI values in the Gaza Strip, Palestine.

The project analyzes historical agricultural vegetation indicators extracted from Sentinel-2 imagery using Google Earth Engine (GEE). The processed data is used to train an ANN model for next-month NDVI prediction.

An interactive Streamlit dashboard provides tools for data analysis, visualization, prediction, and model evaluation.

2.  Project Objectives

- Monitor agricultural vegetation using satellite data.
- Analyze historical vegetation changes.
- Explore spectral indicators related to vegetation and soil conditions.
- Develop a deep learning model for next-month NDVI prediction.
- Provide an interactive platform for exploring and evaluating results.

3.  Dataset Overview

Property| Description
Study Area| Gaza Strip, Palestine
Satellite Source| Sentinel-2
Processing Platform| Google Earth Engine
Data Period| January 2018 – September 2026
Total Records| 52,440
Agricultural Samples| 500
Spectral Indicators| 6
Dataset Format| CSV

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

Model Architecture

Layer| Configuration
Input Layer| 6 Features
Hidden Layer 1| 64 Neurons – ReLU
Hidden Layer 2| 32 Neurons – ReLU
Output Layer| 1 Predicted NDVI Value

Training Configuration

- Optimizer: Adam
- Loss Function: Mean Squared Error (MSE)
- Epochs: 30
- Batch Size: 32
- Validation Split: 20%
- Input Scaling: StandardScaler

5. Model Evaluation

The ANN model was evaluated against a persistence baseline.

Metric| ANN Model| Baseline
MAE| 0.0859| 0.0874
RMSE| 0.1283| 0.1452
R²| 0.5850| 0.4683

Performance Improvement

- MAE Reduction: 1.72%
- RMSE Reduction: 11.64%
- R² Improvement: +0.1167

The ANN model achieved better results than the persistence baseline across all three evaluation metrics.

6. Interactive Dashboard

The Streamlit application includes six main sections:

1. Overview: Project statistics, vegetation trends, and spectral indicators.
2. Data Analysis: Interactive analysis of spectral indices and agricultural samples.
3. AI Prediction: Single-sample and multiple-sample NDVI predictions.
4. Model Performance: Evaluation metrics, model architecture, and baseline comparison.
5. Data Quality: Missing values, duplicate records, and dataset coverage.
6. About Project: Project objectives, methodology, technologies, and limitations.

7. Technologies Used

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

8. Run the Application Locally

Step 1: Clone the repository

git clone https://github.com/asala-ai/AgriRecover-Gaza.git

Step 2: Navigate to the project directory

cd AgriRecover-Gaza

Step 3: Install dependencies

pip install -r requirements.txt

Step 4: Run the application

streamlit run app.py

The application will open in your default web browser.

9. Scope and Limitations

- The model predicts a numerical NDVI value for the month following each sample's latest available observation.
- The model does not directly classify agricultural land as damaged, healthy, recovered, or unrecovered.
- Geographic mapping requires the original sample coordinates exported from Google Earth Engine.
- Live satellite imagery and live Google Earth Engine authentication are not connected to the current application version.
- Predictions are model estimates and should not be interpreted as actual satellite observations.

10. Data Sources and References

- "European Space Agency – Sentinel-2" (https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2)
- "Google Earth Engine – Sentinel-2 SR Harmonized" (https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
- "TensorFlow / Keras Documentation" (https://www.tensorflow.org/guide/keras)
- "Scikit-learn StandardScaler" (https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)

---

<p align="center">
  **AgriRecover Gaza**<br>
  Deep Learning • Remote Sensing • Agricultural Vegetation Monitoring<br>
  Gaza Strip, Palestine
</p>
