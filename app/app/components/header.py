
import streamlit as st


def render_header(title, subtitle):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(
                115deg, #E5EEE7, #F3F5EF
            );
            border: 1px solid #D5E0D7;
            border-radius: 18px;
            padding: 25px;
            margin-bottom: 20px;
        ">
            <div style="
                color: #657A6D;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 2px;
            ">
                AGRICULTURE • DEEP LEARNING • GAZA
            </div>

            <h1 style="
                color: #294638;
                margin: 10px 0;
                font-size: 30px;
            ">
                {title}
            </h1>

            <p style="
                color: #607168;
                font-size: 15px;
                margin-bottom: 0;
            ">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
