
import streamlit as st


def render_about_project():

    st.title("About AgriRecover Gaza")

    st.caption(
        "An AI-powered approach to agricultural "
        "vegetation monitoring and prediction."
    )

    st.divider()

    # Project introduction
    st.subheader("Project Overview")

    st.markdown("""
    **AgriRecover Gaza** is an academic deep learning
    project focused on monitoring agricultural vegetation
    in the Gaza Strip using satellite-derived spectral
    indicators and Artificial Neural Networks.

    The project analyzes historical vegetation data
    extracted from Sentinel-2 satellite imagery and
    uses deep learning to predict future NDVI values.
    """)

    st.divider()

    # Objectives
    st.subheader("Project Objectives")

    objectives = [
        "Monitor agricultural vegetation changes over time.",
        "Analyze six satellite-derived spectral indices.",
        "Prepare historical monthly agricultural datasets.",
        "Develop an Artificial Neural Network for NDVI prediction.",
        "Provide interactive data visualization and analysis.",
    ]

    for objective in objectives:
        st.markdown(f"- {objective}")

    st.divider()

    # Study area and data
    st.subheader("Study Area & Dataset")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Study Area**")
        st.markdown("Gaza Strip, Palestine")

        st.markdown("**Satellite Source**")
        st.markdown("Sentinel-2")

        st.markdown("**Processing Platform**")
        st.markdown("Google Earth Engine")

    with c2:
        st.markdown("**Study Period**")
        st.markdown("January 2018 – September 2026")

        st.markdown("**Agricultural Samples**")
        st.markdown("500 Sample IDs")

        st.markdown("**Dataset Records**")
        st.markdown("52,440 Records")

    st.divider()

    # Spectral indices
    st.subheader("Spectral Indices")

    indices = {
        "NDVI": "Normalized Difference Vegetation Index",
        "EVI": "Enhanced Vegetation Index",
        "NDMI": "Normalized Difference Moisture Index",
        "SAVI": "Soil-Adjusted Vegetation Index",
        "BSI": "Bare Soil Index",
        "NBR": "Normalized Burn Ratio",
    }

    for index, description in indices.items():
        with st.expander(index):
            st.write(description)

    st.divider()

    # AI technology
    st.subheader("Deep Learning Model")

    st.markdown("""
    The project uses an Artificial Neural Network (ANN)
    to estimate the next month's NDVI.

    The model receives six spectral indicators as input
    and produces one predicted NDVI value.

    The saved model and fitted StandardScaler are used
    for prediction without retraining.
    """)

    st.divider()

    # Technologies
    st.subheader("Technologies Used")

    technologies = [
        "Python",
        "Google Earth Engine",
        "Sentinel-2",
        "TensorFlow / Keras",
        "Pandas and NumPy",
        "Scikit-learn",
        "Plotly",
        "Streamlit",
    ]

    st.write(" • ".join(technologies))

    st.divider()

    # References
    st.subheader("References & Data Sources")

    st.markdown("""
    1. [European Space Agency - Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2)

    2. [Google Earth Engine - Sentinel-2 Dataset](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)

    3. [Google Earth Engine Documentation](https://developers.google.com/earth-engine)

    4. [TensorFlow Documentation](https://www.tensorflow.org/)

    5. [Scikit-learn Documentation](https://scikit-learn.org/)
    """)

    st.divider()

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:20px;
            background:#E8EEE8;
            border-radius:15px;
            color:#355B4A;
        ">
            <h3>AgriRecover Gaza 🌱</h3>
            <p>A Deep Learning Academic Project</p>
            <p>Satellite Remote Sensing • AI • Agriculture</p>
        </div>
        """,
        unsafe_allow_html=True
    )
