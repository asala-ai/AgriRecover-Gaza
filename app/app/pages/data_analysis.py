
import streamlit as st
import pandas as pd
import plotly.express as px


FEATURES = ["NDVI", "EVI", "NDMI", "SAVI", "BSI", "NBR"]

INDEX_LABELS = {
    "NDVI": "Vegetation Greenness",
    "EVI": "Enhanced Vegetation Index",
    "NDMI": "Vegetation Moisture",
    "SAVI": "Soil-Adjusted Vegetation",
    "BSI": "Bare Soil Index",
    "NBR": "Normalized Burn Ratio",
}


def render_data_analysis(df):

    st.title("Data Analysis")

    st.caption(
        "Explore agricultural spectral indicators "
        "and vegetation trends over time."
    )

    st.divider()

    # Select spectral index
    st.subheader("Spectral Index Analysis")

    selected_index = st.selectbox(
        "Select Spectral Index",
        FEATURES
    )

    sample_ids = sorted(
        df["sample_id"].dropna().unique().tolist()
    )

    selected_sample = st.selectbox(
        "Select Agricultural Sample",
        sample_ids,
        format_func=lambda x: f"Sample {x}"
    )

    sample_data = (
        df[df["sample_id"] == selected_sample]
        .sort_values("month_dt")
    )

    fig = px.line(
        sample_data,
        x="month_dt",
        y=selected_index,
        markers=True,
        title=f"{selected_index} - Sample {selected_sample}",
        labels={
            "month_dt": "Month",
            selected_index: selected_index
        }
    )

    fig.update_traces(
        line=dict(color="#557C68", width=3),
        marker=dict(size=5)
    )

    fig.update_layout(
        template="plotly_white",
        height=400,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(INDEX_LABELS[selected_index])

    st.divider()

    # Compare spectral indices
    st.subheader("Spectral Indices Comparison")

    available_months = sorted(
        df["month"].dropna().unique().tolist()
    )

    selected_month = st.selectbox(
        "Select Month for Comparison",
        available_months,
        index=len(available_months) - 1
    )

    month_data = df[
        df["month"] == selected_month
    ]

    mean_values = (
        month_data[FEATURES]
        .mean()
        .rename_axis("Index")
        .reset_index(name="Mean Value")
    )

    fig2 = px.bar(
        mean_values,
        x="Index",
        y="Mean Value",
        color="Index",
        title=f"Average Spectral Indicators - {selected_month}",
        color_discrete_sequence=[
            "#557C68",
            "#8FA99A",
            "#829EAD",
            "#C4A978",
            "#C98778",
            "#A9B6A8"
        ]
    )

    fig2.update_layout(
        template="plotly_white",
        height=380,
        showlegend=False
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # Dataset preview
    st.subheader("Dataset Preview")

    st.dataframe(
        df[
            ["month", "sample_id"] + FEATURES
        ].head(100),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Showing the first 100 records."
    )
