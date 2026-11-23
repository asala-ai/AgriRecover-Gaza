
import streamlit as st
import pandas as pd
import plotly.express as px


def render_data_quality(df):

    st.title("Data Quality")

    st.caption(
        "Inspect dataset completeness, duplicate records, "
        "monthly coverage, and potential data issues."
    )

    st.divider()

    features = [
        "NDVI", "EVI", "NDMI",
        "SAVI", "BSI", "NBR"
    ]

    required_columns = ["month", "sample_id"] + features

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(
            f"Missing required columns: {missing_columns}"
        )
        return

    # Data quality calculations
    missing_values = int(
        df[required_columns].isna().sum().sum()
    )

    duplicate_records = int(
        df.duplicated(
            subset=["month", "sample_id"]
        ).sum()
    )

    sample_count = df["sample_id"].nunique()
    month_count = df["month"].nunique()
    record_count = len(df)

    expected_records = sample_count * month_count

    coverage_gaps = max(
        expected_records - record_count, 0
    )

    evi_above_one = int(
        (df["EVI"] > 1).sum()
    )

    # Quality overview
    st.subheader("Dataset Quality Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

    c2.metric(
        "Duplicate Records",
        f"{duplicate_records:,}"
    )

    c3.metric(
        "EVI Values > 1",
        f"{evi_above_one:,}"
    )

    c4.metric(
        "Coverage Gaps*",
        f"{coverage_gaps:,}"
    )

    st.caption(
        "*Estimated missing sample-month combinations "
        "using the total sample count and observed months."
    )

    st.divider()

    # Monthly coverage
    st.subheader("Monthly Data Coverage")

    monthly_counts = (
        df.groupby("month")
        .size()
        .reset_index(name="Records")
        .sort_values("month")
    )

    fig = px.bar(
        monthly_counts,
        x="month",
        y="Records",
        title="Number of Records per Month",
        labels={
            "month": "Month",
            "Records": "Number of Records"
        }
    )

    fig.update_traces(
        marker_color="#8FA99A"
    )

    fig.update_layout(
        template="plotly_white",
        height=380
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # Missing values by column
    st.subheader("Missing Values by Feature")

    missing_by_column = (
        df[required_columns]
        .isna()
        .sum()
        .reset_index()
    )

    missing_by_column.columns = [
        "Feature", "Missing Count"
    ]

    fig2 = px.bar(
        missing_by_column,
        x="Feature",
        y="Missing Count",
        title="Missing Values Distribution",
        color_discrete_sequence=["#829EAD"]
    )

    fig2.update_layout(
        template="plotly_white",
        height=330
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # EVI review
    st.subheader("Potential Values Requiring Review")

    flagged = df[
        df["EVI"] > 1
    ][["month", "sample_id", "EVI"]]

    if flagged.empty:

        st.success(
            "No EVI values above 1 were found."
        )

    else:

        st.warning(
            f"{len(flagged):,} EVI records are above 1. "
            "These records require review."
        )

        st.dataframe(
            flagged,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # Geographic availability
    st.subheader("Geographic Data Availability")

    coordinate_columns = {
        col.lower() for col in df.columns
    }

    has_coordinates = (
        "latitude" in coordinate_columns
        and "longitude" in coordinate_columns
    )

    if has_coordinates:

        st.success(
            "Geographic coordinates are available "
            "in the dataset."
        )

    else:

        st.info(
            "Latitude and longitude are not available "
            "in the current dataset. Geographic mapping "
            "will require the original sample coordinates "
            "exported from Google Earth Engine."
        )

    st.divider()

    # Dataset summary
    st.subheader("Dataset Summary")

    summary = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Unique Samples",
            "Observed Months",
            "Spectral Indicators"
        ],
        "Value": [
            f"{record_count:,}",
            f"{sample_count:,}",
            f"{month_count:,}",
            len(features)
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "AgriRecover Gaza | Dataset Quality Assessment"
    )
