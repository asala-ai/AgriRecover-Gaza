
import plotly.express as px
import plotly.graph_objects as go

from .data_loader import FEATURES


COLORS = {
    "forest": "#355B4A",
    "sage": "#8FA99A",
    "blue": "#829EAD",
    "gold": "#C4A978",
    "coral": "#C98778",
}


def create_index_trend(data, index, sample_id=None):

    if index not in FEATURES:
        raise ValueError(f"Unknown spectral index: {index}")

    chart_data = data.copy()

    if sample_id is not None:
        chart_data = chart_data[
            chart_data["sample_id"] == sample_id
        ]

    chart_data = chart_data.sort_values("month_dt")

    fig = px.line(
        chart_data,
        x="month_dt",
        y=index,
        markers=True,
        title=f"{index} Trend",
        labels={
            "month_dt": "Month",
            index: index
        }
    )

    fig.update_traces(
        line=dict(color=COLORS["forest"], width=2.5)
    )

    fig.update_layout(
        template="plotly_white",
        height=380
    )

    return fig


def create_monthly_ndvi_trend(data):

    monthly = (
        data.groupby("month_dt", as_index=False)["NDVI"]
        .mean()
        .sort_values("month_dt")
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["month_dt"],
            y=monthly["NDVI"],
            mode="lines",
            name="Mean NDVI",
            line=dict(
                color=COLORS["forest"],
                width=3
            )
        )
    )

    fig.update_layout(
        title="Monthly Average NDVI",
        xaxis_title="Month",
        yaxis_title="Mean NDVI",
        template="plotly_white",
        height=380
    )

    return fig


def create_prediction_distribution(predictions):

    fig = px.histogram(
        predictions,
        x="Predicted_NDVI",
        nbins=25,
        title="Predicted NDVI Distribution"
    )

    fig.update_traces(
        marker_color=COLORS["sage"]
    )

    fig.update_layout(
        template="plotly_white",
        height=350
    )

    return fig
