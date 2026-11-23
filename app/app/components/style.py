
import streamlit as st

COLORS = {
    "forest": "#355B4A",
    "sage": "#8FA99A",
    "mint": "#DCE8E0",
    "cream": "#F5F6F1",
    "slate": "#65736D",
    "blue": "#829EAD",
    "gold": "#C4A978",
    "coral": "#C98778",
    "white": "#FFFFFF",
}


def apply_custom_style():
    st.markdown(
        """
        <style>
        @import url(
          'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap'
        );

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background-color: #F5F6F1;
            color: #26362F;
        }

        [data-testid="stSidebar"] {
            background-color: #E8EEE8;
        }

        h1, h2, h3 {
            color: #294638;
        }

        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E0E7E0;
            padding: 14px;
            border-radius: 14px;
        }

        .section-card {
            background: #FFFFFF;
            border: 1px solid #E0E7E0;
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: .6rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
