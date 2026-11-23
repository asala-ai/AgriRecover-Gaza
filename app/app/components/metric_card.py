
import streamlit as st


def render_metric_card(title, value, description=None):
    st.markdown(
        f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E0E7E0;
            border-radius: 14px;
            padding: 18px;
            min-height: 115px;
        ">
            <div style="
                color: #68776F;
                font-size: 14px;
                font-weight: 500;
            ">
                {title}
            </div>

            <div style="
                color: #294638;
                font-size: 28px;
                font-weight: 700;
                margin: 8px 0;
            ">
                {value}
            </div>

            <div style="
                color: #8A9890;
                font-size: 12px;
            ">
                {description or ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
