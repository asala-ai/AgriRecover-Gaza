
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


FEATURES = ["NDVI", "EVI", "NDMI", "SAVI", "BSI", "NBR"]


def generate_predictions(df, model, scaler):

    latest = (
        df.sort_values(["sample_id", "month_dt"])
        .groupby("sample_id", as_index=False)
        .tail(1)
        .sort_values("sample_id")
        .copy()
    )

    if latest[FEATURES].isna().any().any():
        raise ValueError(
            "Missing spectral values were found. "
            "Please review the dataset before prediction."
        )

    x_latest = latest[FEATURES].astype(float)

    # Use the original fitted scaler
    x_scaled = scaler.transform(x_latest)

    # Predict using the saved ANN model
    predicted = model.predict(
        x_scaled,
        verbose=0
    ).reshape(-1)

    results = latest[
        ["sample_id", "month", "month_dt", "NDVI"]
    ].copy()

    results["Predicted_NDVI"] = predicted

    results["Prediction_Month"] = (
        results["month_dt"].dt.to_period("M") + 1
    ).astype(str)

    results["Change_vs_Current"] = (
        results["Predicted_NDVI"] - results["NDVI"]
    )

    return results.reset_index(drop=True)


def render_ai_prediction(df, model, scaler):

    st.title("AI Prediction")

    st.caption(
        "Forecast agricultural vegetation using "
        "the saved Artificial Neural Network model."
    )

    st.divider()

    st.subheader("Prediction Settings")

    mode = st.radio(
        "Choose Prediction Mode",
        [
            "Single Sample",
            "All Available Samples"
        ],
        horizontal=True
    )

    try:
        predictions = generate_predictions(
            df, model, scaler
        )

    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
        return

    if predictions.empty:
        st.warning("No available samples for prediction.")
        return

    forecast_month = predictions[
        "Prediction_Month"
    ].mode().iloc[0]

    st.info(
        f"Forecast month: {forecast_month}"
    )

    st.divider()

    # Single sample prediction
    if mode == "Single Sample":

        selected_id = st.selectbox(
            "Select Sample ID",
            sorted(
                predictions["sample_id"].unique()
            )
        )

        row = predictions[
            predictions["sample_id"] == selected_id
        ].iloc[0]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Current NDVI",
                f"{row['NDVI']:.4f}"
            )

        with c2:
            st.metric(
                "Predicted NDVI",
                f"{row['Predicted_NDVI']:.4f}"
            )

        with c3:
            st.metric(
                "NDVI Change",
                f"{row['Change_vs_Current']:+.4f}"
            )

        st.divider()

        st.subheader(
            f"Sample {selected_id} Prediction"
        )

        history = (
            df[df["sample_id"] == selected_id]
            .sort_values("month_dt")
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=history["month_dt"],
                y=history["NDVI"],
                mode="lines+markers",
                name="Historical NDVI",
                line=dict(
                    color="#557C68",
                    width=3
                )
            )
        )

        prediction_date = pd.Period(
            row["Prediction_Month"],
            freq="M"
        ).to_timestamp()

        fig.add_trace(
            go.Scatter(
                x=[
                    history["month_dt"].max(),
                    prediction_date
                ],
                y=[
                    row["NDVI"],
                    row["Predicted_NDVI"]
                ],
                mode="lines+markers",
                name="Predicted NDVI",
                line=dict(
                    color="#C98778",
                    width=2,
                    dash="dash"
                ),
                marker=dict(size=9)
            )
        )

        fig.update_layout(
            template="plotly_white",
            height=420,
            xaxis_title="Month",
            yaxis_title="NDVI",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption(
            "The predicted value is a model estimate, "
            "not an actual satellite observation."
        )

    # All samples prediction
    else:

        st.subheader(
            f"Predictions for {len(predictions):,} Samples"
        )

        display_data = predictions[
            [
                "sample_id",
                "month",
                "Prediction_Month",
                "NDVI",
                "Predicted_NDVI",
                "Change_vs_Current"
            ]
        ].rename(
            columns={
                "sample_id": "Sample ID",
                "month": "Latest Observed Month",
                "Prediction_Month": "Forecast Month",
                "NDVI": "Current NDVI",
                "Predicted_NDVI": "Predicted NDVI",
                "Change_vs_Current": "NDVI Change"
            }
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        csv_data = predictions.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="Download Predictions CSV",
            data=csv_data,
            file_name=(
                f"AgriRecover_Predictions_"
                f"{forecast_month}.csv"
            ),
            mime="text/csv"
        )

        st.divider()

        st.subheader(
            "Predicted NDVI Distribution"
        )

        fig = go.Figure(
            data=[
                go.Histogram(
                    x=predictions["Predicted_NDVI"],
                    nbinsx=25,
                    marker_color="#8FA99A"
                )
            ]
        )

        fig.update_layout(
            template="plotly_white",
            height=350,
            xaxis_title="Predicted NDVI",
            yaxis_title="Number of Samples"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.caption(
        "Model: Saved AgriRecover ANN | "
        "Input features: NDVI, EVI, NDMI, SAVI, BSI, NBR | "
        "Forecast horizon: One month ahead."
    )
