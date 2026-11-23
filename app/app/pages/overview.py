
import streamlit as st
import plotly.express as px

from ..components.header import render_header
from ..components.metric_card import render_metric_card


def render_overview(df):

    render_header(
        "AgriRecover Gaza",
        "Agricultural Vegetation Monitoring and Prediction"
    )

    st.subheader("Project Overview")

    total_records = len(df)
    total_samples = df["sample_id"].nunique()
    total_months = df["month"].nunique()

    c1, c2, c3 = st.columns(3)

    with c1:
        render_metric_card(
            "Total Records",
            f"{total_records:,}",
            "Agricultural observations"
        )

    with c2:
        render_metric_card(
            "Sample Points",
            f"{total_samples:,}",
            "Agricultural samples"
        )

    with c3:
        render_metric_card(
            "Monthly Observations",
            f"{total_months:,}",
            "Available months"
        )

    st.divider()

    st.subheader("Monthly Vegetation Trend")

    monthly = (
        df.groupby("month_dt", as_index=False)["NDVI"]
        .mean()
        .sort_values("month_dt")
    )

    fig = px.line(
        monthly,
        x="month_dt",
        y="NDVI",
        title="Average Monthly NDVI",
        labels={
            "month_dt": "Month",
            "NDVI": "Mean NDVI"
        }
    )

    fig.update_traces(
        line=dict(color="#557C68", width=3)
    )

    fig.update_layout(
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Data source: Sentinel-2 satellite imagery "
        "processed using Google Earth Engine."
    )
