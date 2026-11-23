
import streamlit as st


PAGES = [
    "Overview",
    "Data Analysis",
    "AI Prediction",
    "Model Performance",
    "Data Quality",
    "About Project",
]


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <h2 style="color:#294638;">
                🌱 AgriRecover Gaza
            </h2>
            <p style="color:#657A6D; font-size:13px;">
                Agricultural Monitoring & Prediction
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        selected_page = st.radio(
            "NAVIGATION",
            PAGES,
            label_visibility="visible"
        )

        st.divider()

        st.caption("STUDY AREA")
        st.markdown("**Gaza Strip, Palestine**")

        st.caption("DATA SOURCE")
        st.markdown("Sentinel-2 / Google Earth Engine")

        return selected_page
