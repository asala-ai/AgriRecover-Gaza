from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------
# AgriRecover Gaza | Streamlit application
# Uses the original CSV, trained ANN model, and fitted StandardScaler.
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="AgriRecover Gaza",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
FEATURES = ["NDVI", "EVI", "NDMI", "SAVI", "BSI", "NBR"]
INDEX_LABELS = {
    "NDVI": "Normalized Difference Vegetation Index",
    "EVI": "Enhanced Vegetation Index",
    "NDMI": "Normalized Difference Moisture Index",
    "SAVI": "Soil-Adjusted Vegetation Index",
    "BSI": "Bare Soil Index",
    "NBR": "Normalized Burn Ratio",
}
COLORS = {
    "forest": "#355B4A",
    "sage": "#8FA99A",
    "mint": "#DCE8E0",
    "cream": "#F5F6F1",
    "slate": "#65736D",
    "blue": "#829EAD",
    "gold": "#C4A978",
    "coral": "#C98778",
}

# Soft, low-saturation visual style.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #F5F6F1; color: #26362F; }
    [data-testid="stSidebar"] { background: #E8EEE8; }
    [data-testid="stSidebar"] * { color: #26362F; }
    h1, h2, h3 { color: #294638; }
    .hero {
        padding: 1.35rem 1.55rem; border-radius: 18px;
        background: linear-gradient(115deg, #E5EEE7, #F3F5EF);
        border: 1px solid #D5E0D7; margin-bottom: 1rem;
    }
    .hero-kicker { color: #657A6D; font-size: .83rem; letter-spacing: .08em;
        text-transform: uppercase; font-weight: 700; }
    .hero-title { color: #294638; font-size: 2rem; font-weight: 700; margin: .25rem 0; }
    .hero-sub { color: #607168; font-size: 1rem; }
    /* Improved text readability */
.small-note {
    color: #52645A !important;
    font-size: .9rem;
    line-height: 1.6;
}

.hero-kicker {
    color: #52645A !important;
}

.hero-sub {
    color: #52645A !important;
    line-height: 1.7;
}

.stCaption,
[data-testid="stCaptionContainer"] {
    color: #52645A !important;
}

.stMarkdown p {
    color: #44564B;
}

.stSelectbox label,
.stRadio label {
    color: #44564B !important;
    font-weight: 600;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] .stCaption {
    color: #52645A !important;
}
    div[data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #E0E7E0;
        padding: 12px 14px; border-radius: 14px;
    }
    div[data-testid="stMetricLabel"] { color: #68776F; }
    div[data-testid="stMetricValue"] { color: #294638; }
    .section-card {
        background: #FFFFFF; border: 1px solid #E0E7E0;
        border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: .6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def find_first(paths):
    for path in paths:
        if path.exists():
            return path
    return None


@st.cache_data(show_spinner="Loading agricultural dataset...")
def load_dataset(csv_path, modified_time):
    data = pd.read_csv(csv_path)
    required = ["month", "sample_id"] + FEATURES
    missing_columns = [c for c in required if c not in data.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    data["month"] = data["month"].astype(str)
    data["month_dt"] = pd.to_datetime(data["month"], format="%Y-%m", errors="coerce")
    data["sample_id"] = pd.to_numeric(data["sample_id"], errors="coerce")
    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=["month_dt", "sample_id"]).copy()
    data["sample_id"] = data["sample_id"].astype(int)
    return data.sort_values(["sample_id", "month_dt"]).reset_index(drop=True)


@st.cache_resource(show_spinner="Loading the saved ANN model and scaler...")
def load_model_and_scaler(model_path, scaler_path, model_mtime, scaler_mtime):
    import tensorflow as tf

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = tf.keras.models.load_model(model_path, compile=False)
        scaler = joblib.load(scaler_path)
    return model, scaler


def make_predictions(data, model, scaler):
    """Predict one month after each sample's latest available observation."""
    latest = (
        data.sort_values(["sample_id", "month_dt"])
        .groupby("sample_id", as_index=False)
        .tail(1)
        .sort_values("sample_id")
        .copy()
    )
    x_latest = latest[FEATURES].astype(float)
    x_scaled = scaler.transform(x_latest)
    predicted = model.predict(x_scaled, verbose=0).reshape(-1)

    result = latest[["sample_id", "month", "month_dt", "NDVI"]].copy()
    result["Predicted_NDVI"] = predicted
    result["Prediction_Month"] = (
        result["month_dt"].dt.to_period("M") + 1
    ).astype(str)
    result["Change_vs_Current"] = result["Predicted_NDVI"] - result["NDVI"]
    return result.reset_index(drop=True)


def metric_card(label, value, help_text=None):
    st.metric(label, value, help=help_text)


def page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)


# ---------------------------------------------------------------------
# Locate project assets
# ---------------------------------------------------------------------
csv_file = find_first(
    [
        ROOT / "data" / "AgriRecover_Final_2018_2026 (1).csv",
        ROOT / "data" / "AgriRecover_Final_2018_2026.csv",
        ROOT / "data" / "AgriRecover_Final_2018_2026(1).csv",
        ROOT / "AgriRecover_Final_2018_2026 (1).csv",
        ROOT / "AgriRecover_Final_2018_2026.csv",
    ]
)
model_file = find_first(
    [
        ROOT / "model" / "AgriRecover_ANN_Model.keras",
        ROOT / "AgriRecover_ANN_Model.keras",
    ]
)
scaler_file = find_first(
    [
        ROOT / "model" / "AgriRecover_Scaler.pkl",
        ROOT / "AgriRecover_Scaler.pkl",
    ]
)

# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌱 AgriRecover Gaza")
    st.caption("Agricultural vegetation monitoring & prediction")
    st.divider()
    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Data Analysis",
            "AI Prediction",
            "Model Performance",
            "Data Quality",
            "About Project",
        ],
        label_visibility="visible",
    )
    st.divider()
    st.caption("Study area")
    st.markdown("**Gaza Strip, Palestine**")
    st.caption("Data source: Sentinel-2 / Google Earth Engine")
    st.caption("Project type: Deep Learning")


# ---------------------------------------------------------------------
# Load dataset safely
# ---------------------------------------------------------------------
if csv_file is None:
    st.error(
        "Dataset file was not found. Please check that the CSV is uploaded "
        "inside the repository's data/ folder and that its filename matches "
        "the expected project file."
    )
    st.stop()

try:
    df = load_dataset(str(csv_file), csv_file.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

if df.empty:
    st.error("The dataset is empty after reading and basic date validation.")
    st.stop()

first_month = df["month_dt"].min().strftime("%B %Y")
last_month = df["month_dt"].max().strftime("%B %Y")
latest_month_key = df["month_dt"].max().strftime("%Y-%m")
sample_count = int(df["sample_id"].nunique())
record_count = int(len(df))
month_count = int(df["month_dt"].nunique())

# Load model only for pages that need it.
model = scaler = None
model_error = None
if page == "AI Prediction":
    if model_file is None or scaler_file is None:
        model_error = (
            "The saved ANN model or StandardScaler was not found. "
            "Check model/AgriRecover_ANN_Model.keras and "
            "model/AgriRecover_Scaler.pkl."
        )
    else:
        try:
            model, scaler = load_model_and_scaler(
                str(model_file),
                str(scaler_file),
                model_file.stat().st_mtime,
                scaler_file.stat().st_mtime,
            )
        except Exception as exc:
            model_error = (
                "The saved model/scaler could not be loaded. "
                "Check the TensorFlow and scikit-learn versions in "
                f"requirements.txt. Technical detail: {exc}"
            )


# ---------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------
if page == "Overview":
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-kicker">Deep Learning • Remote Sensing • Gaza</div>
          <div class="hero-title">AgriRecover Gaza</div>
          <div class="hero-sub">
            A data-driven platform for monitoring agricultural vegetation
            and forecasting the next month's NDVI using Sentinel-2 indicators.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Project at a glance")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total records", f"{record_count:,}")
    with c2:
        metric_card("Sample points", f"{sample_count:,}")
    with c3:
        metric_card("Monthly observations", f"{month_count:,}")
    with c4:
        metric_card("Spectral indices", "6")

    st.caption(
        f"Available data period: {first_month} – {last_month}. "
        "Forecasts are generated for the month immediately following each "
        "sample's latest available observation."
    )

    left, right = st.columns([1.55, 1])
    with left:
        st.subheader("Monthly vegetation trend")
        monthly = df.groupby("month_dt", as_index=False)["NDVI"].mean()
        fig = px.line(
            monthly,
            x="month_dt",
            y="NDVI",
            markers=False,
            labels={"month_dt": "Month", "NDVI": "Mean NDVI"},
        )
        fig.update_traces(line=dict(color=COLORS["forest"], width=3))
        fig.update_layout(
            template="plotly_white",
            height=340,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Spectral indicators")
        st.markdown(
            """
            <div class="section-card">
              <b>NDVI</b><br><span class="small-note">Vegetation greenness and density</span>
            </div>
            <div class="section-card">
              <b>EVI</b><br><span class="small-note">Enhanced vegetation response</span>
            </div>
            <div class="section-card">
              <b>NDMI</b><br><span class="small-note">Vegetation moisture-related response</span>
            </div>
            <div class="section-card">
              <b>SAVI · BSI · NBR</b><br><span class="small-note">Soil-adjusted vegetation, bare soil, and burn-related spectral response</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Project workflow")
    steps = st.columns(5)
    workflow = [
        ("01", "Sentinel-2", "Satellite imagery"),
        ("02", "Google Earth Engine", "Processing & indices"),
        ("03", "Dataset", "Monthly sample records"),
        ("04", "ANN model", "Next-month NDVI"),
        ("05", "Dashboard", "Interactive results"),
    ]
    for col, (number, title, desc) in zip(steps, workflow):
        with col:
            st.markdown(
                f"""
                <div class="section-card" style="min-height:125px">
                  <div style="color:{COLORS['sage']};font-weight:700">{number}</div>
                  <b>{title}</b><br>
                  <span class="small-note">{desc}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------
# Data Analysis
# ---------------------------------------------------------------------
elif page == "Data Analysis":
    page_header(
        "Data Analysis",
        "Explore monthly spectral indicators and sample-level vegetation trends.",
    )

    selected_index = st.selectbox("Select spectral index", FEATURES, index=0)
    sample_options = sorted(df["sample_id"].unique().tolist())
    selected_sample = st.selectbox(
        "Select sample ID",
        sample_options,
        index=0,
        format_func=lambda x: f"Sample {x}",
    )

    sample_df = df[df["sample_id"] == selected_sample].sort_values("month_dt")
    fig = px.line(
        sample_df,
        x="month_dt",
        y=selected_index,
        markers=True,
        labels={
            "month_dt": "Month",
            selected_index: selected_index,
        },
        title=f"{selected_index} over time — Sample {selected_sample}",
    )
    fig.update_traces(line=dict(color=COLORS["forest"], width=2), marker=dict(size=4))
    fig.update_layout(template="plotly_white", height=390)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Compare spectral indices")
    compare_month = st.selectbox(
        "Choose month",
        sorted(df["month"].unique()),
        index=len(sorted(df["month"].unique())) - 1,
    )
    month_data = df[df["month"] == compare_month]
    mean_values = month_data[FEATURES].mean().rename_axis("Index").reset_index(name="Mean")
    fig2 = px.bar(
        mean_values,
        x="Index",
        y="Mean",
        color="Index",
        color_discrete_sequence=[
            COLORS["forest"], COLORS["sage"], COLORS["blue"],
            COLORS["gold"], COLORS["coral"], "#A9B6A8",
        ],
        title=f"Mean spectral index values — {compare_month}",
    )
    fig2.update_layout(
        template="plotly_white",
        showlegend=False,
        height=350,
        xaxis_title="Spectral index",
        yaxis_title="Mean value",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Dataset preview")
    st.dataframe(
        df[["month", "sample_id"] + FEATURES].head(100),
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Preview limited to the first 100 rows for readability.")


# ---------------------------------------------------------------------
# AI Prediction
# ---------------------------------------------------------------------
elif page == "AI Prediction":
    page_header(
        "AI Prediction",
        "Use the saved ANN model and its original fitted scaler to forecast NDVI.",
    )

    if model_error:
        st.error(model_error)
        st.info(
            "The prediction interface is ready, but inference is unavailable "
            "until the model dependencies and saved files load successfully."
        )
        st.stop()

    try:
        predictions = make_predictions(df, model, scaler)
    except Exception as exc:
        st.error(f"Prediction could not be completed: {exc}")
        st.stop()

    forecast_month = predictions["Prediction_Month"].mode().iloc[0]
    st.info(
        f"Forecast horizon: **{forecast_month}**, based on the latest available "
        f"observation for each sample. Latest dataset month: **{latest_month_key}**."
    )

    mode = st.radio(
        "Prediction mode",
        ["Single sample", "All available samples"],
        horizontal=True,
    )

    if mode == "Single sample":
        chosen_id = st.selectbox(
            "Choose Sample ID",
            sorted(predictions["sample_id"].unique().tolist()),
        )
        row = predictions[predictions["sample_id"] == chosen_id].iloc[0]
        a, b, c = st.columns(3)
        with a:
            metric_card("Current NDVI", f"{row['NDVI']:.4f}")
        with b:
            metric_card("Predicted NDVI", f"{row['Predicted_NDVI']:.4f}")
        with c:
            metric_card("Change", f"{row['Change_vs_Current']:+.4f}")

        st.subheader(f"Sample {chosen_id} — one-step-ahead forecast")
        history = df[df["sample_id"] == chosen_id].sort_values("month_dt")
        hist_fig = go.Figure()
        hist_fig.add_trace(
            go.Scatter(
                x=history["month_dt"],
                y=history["NDVI"],
                mode="lines",
                name="Historical NDVI",
                line=dict(color=COLORS["forest"], width=2.5),
            )
        )
        prediction_date = pd.Period(row["Prediction_Month"], freq="M").to_timestamp()
        hist_fig.add_trace(
            go.Scatter(
                x=[history["month_dt"].max(), prediction_date],
                y=[row["NDVI"], row["Predicted_NDVI"]],
                mode="lines+markers",
                name="Forecast connection",
                line=dict(color=COLORS["coral"], width=2, dash="dash"),
                marker=dict(size=9),
            )
        )
        hist_fig.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Month",
            yaxis_title="NDVI",
            legend_title="",
        )
        st.plotly_chart(hist_fig, use_container_width=True)
        st.caption(
            "The forecast is a model estimate, not a satellite observation. "
            "It is based on the six spectral indicators from the sample's "
            "latest available month."
        )

    else:
        st.subheader(f"Predictions for {len(predictions):,} samples")
        st.dataframe(
            predictions[
                [
                    "sample_id",
                    "month",
                    "Prediction_Month",
                    "NDVI",
                    "Predicted_NDVI",
                    "Change_vs_Current",
                ]
            ].rename(
                columns={
                    "sample_id": "Sample ID",
                    "month": "Latest observed month",
                    "Prediction_Month": "Forecast month",
                    "NDVI": "Current NDVI",
                    "Predicted_NDVI": "Predicted NDVI",
                    "Change_vs_Current": "Change",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
        
        csv_bytes = predictions.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download predictions as CSV",
            data=csv_bytes,
            file_name=f"AgriRecover_NDVI_Predictions_{forecast_month}.csv",
            mime="text/csv",
            use_container_width=False,
        )

        dist_fig = px.histogram(
            predictions,
            x="Predicted_NDVI",
            nbins=25,
            title="Distribution of predicted NDVI values",
            labels={"Predicted_NDVI": "Predicted NDVI"},
        )
        dist_fig.update_traces(marker_color=COLORS["sage"])
        dist_fig.update_layout(template="plotly_white", height=340)
        st.plotly_chart(dist_fig, use_container_width=True)

    st.caption(
        "Model inference uses the saved AgriRecover_ANN_Model.keras and "
        "AgriRecover_Scaler.pkl files. The model is not retrained in this app."
    )


# ---------------------------------------------------------------------
# Model Performance
# ---------------------------------------------------------------------
elif page == "Model Performance":
    page_header(
        "Model Performance",
        "Reported evaluation results from the completed model experiment.",
    )

    st.info(
        "The metrics below are copied from the model evaluation output in the "
        "project notebook. They are not recalculated when this page opens."
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("MAE", "0.0952", "Mean Absolute Error")
    with m2:
        metric_card("RMSE", "0.1327", "Root Mean Squared Error")
    with m3:
        metric_card("R²", "0.5675", "Coefficient of determination")

    st.subheader("ANN architecture")
    arch = st.columns(4)
    architecture = [
        ("Input", "6 features", "NDVI, EVI, NDMI, SAVI, BSI, NBR"),
        ("Hidden layer 1", "64 neurons", "ReLU activation"),
        ("Hidden layer 2", "32 neurons", "ReLU activation"),
        ("Output", "1 value", "Next-month NDVI"),
    ]
    for col, (title, value, detail) in zip(arch, architecture):
        with col:
            st.markdown(
                f"""
                <div class="section-card" style="min-height:135px;text-align:center">
                  <div class="small-note">{title}</div>
                  <h3 style="margin:.4rem 0">{value}</h3>
                  <div class="small-note">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("Training configuration")
    config = pd.DataFrame(
        {
            "Setting": [
                "Optimizer",
                "Loss function",
                "Epochs",
                "Batch size",
                "Validation split",
                "Input scaling",
            ],
            "Value": [
                "Adam",
                "Mean Squared Error (MSE)",
                "30",
                "32",
                "20% of training data",
                "StandardScaler",
            ],
        }
    )
    st.dataframe(config, hide_index=True, use_container_width=True)

    st.subheader("How to interpret the metrics")
    st.markdown(
        """
        - **MAE** measures the average absolute difference between actual and predicted NDVI.
        - **RMSE** gives greater weight to larger prediction errors.
        - **R²** describes the proportion of target variance explained by the model on the evaluation set.
        """
    )
    st.warning(
        "The R² value of 0.5675 indicates moderate explanatory performance, "
        "not a classification accuracy percentage. Training/validation loss "
        "curves and the saved test predictions are not included in the current "
        "GitHub repository, so this page does not fabricate those plots."
    )


# ---------------------------------------------------------------------
# Data Quality
# ---------------------------------------------------------------------
elif page == "Data Quality":
    page_header(
        "Data Quality",
        "Inspect completeness, duplicate records, monthly coverage, and values requiring review.",
    )

    missing_total = int(df[["month", "sample_id"] + FEATURES].isna().sum().sum())
    duplicate_total = int(df.duplicated(subset=["month", "sample_id"]).sum())
    evi_high = int((df["EVI"] > 1).sum())
    expected_records = sample_count * month_count
    absent_pairs = max(expected_records - record_count, 0)

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        metric_card("Missing values", f"{missing_total:,}")
    with q2:
        metric_card("Duplicate sample-month pairs", f"{duplicate_total:,}")
    with q3:
        metric_card("EVI values > 1", f"{evi_high:,}")
    with q4:
        metric_card("Unobserved sample-month pairs*", f"{absent_pairs:,}")

    st.caption(
        "*Calculated as sample count × observed month count minus the number "
        "of rows. This is a coverage gap count, not a count of null cells."
    )

    st.subheader("Records per month")
    monthly_counts = df.groupby("month", as_index=False).size()
    count_fig = px.bar(
        monthly_counts,
        x="month",
        y="size",
        labels={"month": "Month", "size": "Records"},
    )
    count_fig.update_traces(marker_color=COLORS["sage"])
    count_fig.update_layout(template="plotly_white", height=340)
    st.plotly_chart(count_fig, use_container_width=True)

    st.subheader("Values flagged for review")
    flagged = df[df["EVI"] > 1][["month", "sample_id", "EVI"]].sort_values(
        ["month", "sample_id"]
    )
    if flagged.empty:
        st.success("No EVI values above 1 were found in the current dataset.")
    else:
        st.warning(
            f"{len(flagged)} EVI values are greater than 1. They are displayed "
            "for review and are not silently deleted or modified by this app."
        )
        st.dataframe(flagged, use_container_width=True, hide_index=True)

    st.subheader("Geographic data availability")
    has_coordinates = {"latitude", "longitude"}.issubset(
        {c.lower() for c in df.columns}
    )
    if has_coordinates:
        st.success("Latitude and longitude columns are available in the dataset.")
    else:
        st.info(
            "The current final CSV contains month, sample_id, and six spectral "
            "indices, but no latitude/longitude columns. A geographic map of "
            "the 500 sample points will be added after the original sample "
            "coordinates are exported from Google Earth Engine and matched "
            "to sample_id. No random locations are generated."
        )


# ---------------------------------------------------------------------
# About Project
# ---------------------------------------------------------------------
elif page == "About Project":
    page_header(
        "About AgriRecover Gaza",
        "Project overview, data sources, methods, and current implementation scope.",
    )

    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">Academic Deep Learning Project</div>
          <div class="hero-title">Agricultural Vegetation Monitoring & Prediction</div>
          <div class="hero-sub">
            AgriRecover Gaza explores how satellite-derived spectral indicators
            and an Artificial Neural Network can support monitoring of
            agricultural vegetation in the Gaza Strip.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Project objective")
    st.write(
        "To analyze historical agricultural vegetation indicators derived "
        "from Sentinel-2 imagery and estimate the next month's NDVI using a "
        "trained Artificial Neural Network."
    )

    st.subheader("Data and technologies")
    st.markdown(
        """
        - **Study area:** Gaza Strip, Palestine.
        - **Satellite source:** Sentinel-2.
        - **Processing platform:** Google Earth Engine.
        - **Dataset period:** January 2018 – September 2026.
        - **Samples:** 500 agricultural sample IDs.
        - **Indicators:** NDVI, EVI, NDMI, SAVI, BSI, and NBR.
        - **Prediction model:** Artificial Neural Network (ANN).
        - **Application framework:** Streamlit.
        """
    )

    st.subheader("Project workflow")
    st.write(
        "Sentinel-2 imagery → Google Earth Engine processing → spectral "
        "indices → monthly dataset → data preparation → ANN training and "
        "evaluation → interactive Streamlit application."
    )

    st.subheader("Current scope and limitations")
    st.markdown(
        """
        - The saved model predicts a numeric NDVI value for the month after
          the latest available observation for each sample.
        - The model does not directly classify land as damaged, healthy,
          recovered, or unrecovered.
        - Geographic sample mapping requires the original coordinates
          exported from Google Earth Engine.
        - Live satellite imagery and live Google Earth Engine authentication
          are not connected in this application version.
        """
    )

    st.subheader("Data sources")
    st.markdown(
        """
        - [European Space Agency — Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2)
        - [Google Earth Engine — Sentinel-2 SR Harmonized](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
        - [TensorFlow / Keras documentation](https://www.tensorflow.org/guide/keras)
        - [Scikit-learn StandardScaler documentation](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
        """
    )

    st.caption(
        "AgriRecover Gaza — Academic project for deep learning and agricultural "
        "vegetation monitoring."
    )


# ---------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------
st.divider()
st.caption(
    "AgriRecover Gaza • Deep Learning for Agricultural Vegetation Prediction • "
    "Forecasts are model estimates and should be interpreted with the "
    "documented data and model limitations."
  )
