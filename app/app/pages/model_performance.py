
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_model_performance():

    st.title("Model Performance")

    st.caption(
        "Evaluation results and architecture of the "
        "AgriRecover Gaza Artificial Neural Network."
    )

    st.divider()

    # Evaluation metrics
    st.subheader("Model Evaluation Metrics")

    st.info(
        "The following values are the reported results "
        "from the completed model evaluation experiment."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "MAE",
            "0.0952",
            help="Mean Absolute Error"
        )

    with c2:
        st.metric(
            "RMSE",
            "0.1327",
            help="Root Mean Squared Error"
        )

    with c3:
        st.metric(
            "R² Score",
            "0.5675",
            help="Coefficient of Determination"
        )

    st.divider()

    # Model architecture
    st.subheader("ANN Architecture")

    architecture = [
        {
            "Layer": "Input Layer",
            "Units": 6,
            "Activation": "Input Features"
        },
        {
            "Layer": "Hidden Layer 1",
            "Units": 64,
            "Activation": "ReLU"
        },
        {
            "Layer": "Hidden Layer 2",
            "Units": 32,
            "Activation": "ReLU"
        },
        {
            "Layer": "Output Layer",
            "Units": 1,
            "Activation": "NDVI Prediction"
        }
    ]

    architecture_df = pd.DataFrame(architecture)

    st.dataframe(
        architecture_df,
        use_container_width=True,
        hide_index=True
    )

    # Architecture visualization
    st.subheader("Network Structure")

    fig = go.Figure()

    layers = [
        ("Input\n6 Features", 0),
        ("Hidden 1\n64 Neurons", 1),
        ("Hidden 2\n32 Neurons", 2),
        ("Output\n1 NDVI", 3)
    ]

    for label, x in layers:

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[0],
                mode="markers+text",
                text=[label],
                textposition="bottom center",
                marker=dict(
                    size=55,
                    color="#8FA99A",
                    line=dict(
                        color="#557C68",
                        width=2
                    )
                ),
                showlegend=False
            )
        )

    for i in range(3):

        fig.add_annotation(
            x=i + 0.5,
            y=0,
            ax=i,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            text="",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor="#829EAD"
        )

    fig.update_layout(
        template="plotly_white",
        height=280,
        xaxis=dict(
            visible=False,
            range=[-0.5, 3.5]
        ),
        yaxis=dict(
            visible=False,
            range=[-1, 1]
        ),
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=80
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # Training configuration
    st.subheader("Training Configuration")

    config = pd.DataFrame({
        "Parameter": [
            "Optimizer",
            "Loss Function",
            "Epochs",
            "Batch Size",
            "Validation Split",
            "Feature Scaling"
        ],
        "Value": [
            "Adam",
            "Mean Squared Error (MSE)",
            "30",
            "32",
            "20%",
            "StandardScaler"
        ]
    })

    st.dataframe(
        config,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Interpretation
    st.subheader("Understanding the Results")

    st.markdown("""
    **MAE (0.0952)**

    Measures the average absolute difference between
    actual and predicted NDVI values.

    **RMSE (0.1327)**

    Measures prediction error while giving greater
    weight to larger errors.

    **R² Score (0.5675)**

    Indicates how much of the variation in the target
    values is explained by the model on the evaluation set.
    """)

    st.warning(
        "The reported R² value indicates moderate "
        "explanatory performance. It is not a classification "
        "accuracy percentage."
    )

    st.caption(
        "Evaluation metrics are reported from the original "
        "experiment and are not recalculated by this page."
    )
