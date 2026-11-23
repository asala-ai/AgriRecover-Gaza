
import pandas as pd
from .data_loader import FEATURES


def make_predictions(data, model, scaler):
    """
    Predict next-month NDVI for each sample
    using the saved ANN model and scaler.
    """

    latest = (
        data.sort_values(["sample_id", "month_dt"])
        .groupby("sample_id", as_index=False)
        .tail(1)
        .sort_values("sample_id")
        .copy()
    )

    x_latest = latest[FEATURES].astype(float)

    x_scaled = scaler.transform(x_latest)

    predicted = model.predict(
        x_scaled,
        verbose=0
    ).reshape(-1)

    result = latest[
        ["sample_id", "month", "month_dt", "NDVI"]
    ].copy()

    result["Predicted_NDVI"] = predicted

    result["Prediction_Month"] = (
        result["month_dt"].dt.to_period("M") + 1
    ).astype(str)

    result["Change_vs_Current"] = (
        result["Predicted_NDVI"] - result["NDVI"]
    )

    return result.reset_index(drop=True)
