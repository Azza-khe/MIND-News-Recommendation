
import streamlit as st
import pandas as pd
from pathlib import Path


# ==========================================
# 1. CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Model Evaluation | MIND News",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent.parent
METRICS_PATH = BASE_DIR / "artifacts" / "model_metrics.csv"


# ==========================================
# 2. STYLE CSS
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F5F7FB;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Titles */
h1, h2, h3 {
    color: #173B68 !important;
    font-family: Arial, sans-serif;
}

h1 {
    font-weight: 750 !important;
    letter-spacing: -1px;
}

h2 {
    font-weight: 700 !important;
}

h3 {
    font-weight: 650 !important;
}

/* Paragraphs */
p {
    color: #64748B;
    line-height: 1.7;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E8EDF4;
}

[data-testid="stSidebar"] h1 {
    color: #173B68 !important;
    font-size: 25px;
    font-weight: 800;
}

[data-testid="stSidebar"] p {
    color: #8290A5;
}

/* Sidebar navigation */
[data-testid="stSidebar"] a {
    border-radius: 8px;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E8EDF4;
}

/* Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: white;
    border-radius: 14px;
    border-color: #E3EAF3;
}

/* Buttons */
.stButton > button {
    background-color: #E3EAF3;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #173B68;
    color: white;
}

/* Dividers */
hr {
    border-color: #E4EAF2;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. SIDEBAR
# ==========================================

with st.sidebar:

    st.title("MIND NEWS")

    st.caption("INTELLIGENT RECOMMENDATION SYSTEM")

    st.divider()

    st.markdown("##### NAVIGATION")

    st.page_link(
        "app.py",
        label="Dashboard",
        icon=":material/dashboard:"
    )

    st.page_link(
        "pages/1_Model_Evaluation.py",
        label="Model Evaluation",
        icon=":material/analytics:"
    )

    st.page_link(
        "pages/2_Recommendation_Demo.py",
        label="Recommendation Demo",
        icon=":material/newspaper:"
    )

    st.page_link(
        "pages/3_Cold_Start.py",
        label="Cold Start",
        icon=":material/ac_unit:"
    )

    st.divider()

    st.caption("MIND News Recommendation")
    st.caption("Hybrid Recommendation System")


# ==========================================
# 4. PAGE HEADER
# ==========================================

st.title("Model Evaluation")

st.write("""
This page presents the evaluation and comparison of the three
recommendation approaches using validation data.

The objective is to measure recommendation quality and identify
the strengths of each model.
""")

st.divider()


# ==========================================
# 5. LOAD MODEL METRICS
# ==========================================

@st.cache_data
def load_metrics():
    return pd.read_csv(METRICS_PATH)


try:

    metrics = load_metrics()

    required_columns = [
        "Model",
        "Precision@10",
        "Recall@10",
        "NDCG@10"
    ]

    if not all(
        col in metrics.columns
        for col in required_columns
    ):

        st.error(
            "The model_metrics.csv file does not contain "
            "all the required columns."
        )

        st.stop()

    if metrics.empty:
        st.error("The metrics file is empty.")
        st.stop()

except FileNotFoundError:

    st.error("The model_metrics.csv file was not found.")
    st.stop()

except Exception as e:

    st.error(f"Unable to load model metrics: {e}")
    st.stop()


# ==========================================
# 6. MODEL PERFORMANCE TABLE
# ==========================================

st.subheader("Model performance results")

with st.container(border=True):

    st.write(
        "Comparison of the three recommendation approaches "
        "using Precision@10, Recall@10 and NDCG@10."
    )

    st.dataframe(
        metrics.style.format({
            "Precision@10": "{:.4f}",
            "Recall@10": "{:.4f}",
            "NDCG@10": "{:.4f}"
        }),
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ==========================================
# 7. BEST MODEL PER METRIC
# ==========================================

st.subheader("Best model for each metric")

best_precision = metrics.loc[
    metrics["Precision@10"].idxmax()
]

best_recall = metrics.loc[
    metrics["Recall@10"].idxmax()
]

best_ndcg = metrics.loc[
    metrics["NDCG@10"].idxmax()
]

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        label="Best Precision@10",
        value=f"{best_precision['Precision@10']:.4f}",
        delta=str(best_precision["Model"])
    )

with col2:

    st.metric(
        label="Best Recall@10",
        value=f"{best_recall['Recall@10']:.4f}",
        delta=str(best_recall["Model"])
    )

with col3:

    st.metric(
        label="Best NDCG@10",
        value=f"{best_ndcg['NDCG@10']:.4f}",
        delta=str(best_ndcg["Model"])
    )


st.divider()


# ==========================================
# 8. INDIVIDUAL METRIC COMPARISON
# ==========================================

st.subheader("Individual metric comparison")

metric_choice = st.selectbox(
    "Select an evaluation metric",
    [
        "Precision@10",
        "Recall@10",
        "NDCG@10"
    ]
)

chart_data = metrics.set_index("Model")[
    [metric_choice]
]

with st.container(border=True):

    st.markdown(f"### {metric_choice} comparison")

    st.bar_chart(
        chart_data,
        y=metric_choice,
        use_container_width=True
    )


st.divider()


# ==========================================
# 9. GLOBAL PERFORMANCE COMPARISON
# ==========================================

st.subheader("Global model comparison")

comparison_chart = metrics.set_index("Model")[
    [
        "Precision@10",
        "Recall@10",
        "NDCG@10"
    ]
]

with st.container(border=True):

    st.markdown("### Comparison of all evaluation metrics")

    st.bar_chart(
        comparison_chart,
        use_container_width=True
    )


st.divider()


# ==========================================
# 10. METRIC INTERPRETATION
# ==========================================

st.subheader("Understanding the evaluation metrics")

with st.container(border=True):

    st.markdown("### Precision@10")

    st.write("""
    Measures the proportion of relevant articles among
    the 10 recommended articles.

    A higher value means that recommendations are
    more likely to be relevant.
    """)

    st.divider()

    st.markdown("### Recall@10")

    st.write("""
    Measures the proportion of relevant articles that
    the system successfully retrieves among the first
    10 recommendations.

    A higher value means that the system retrieves
    more of the relevant articles.
    """)

    st.divider()

    st.markdown("### NDCG@10")

    st.write("""
    Measures the quality of the recommendation ranking.
    Relevant articles placed higher in the list receive
    greater importance.

    A higher value indicates a better ranking.
    """)


st.divider()


# ==========================================
# 11. FINAL INTERPRETATION
# ==========================================

st.subheader("Evaluation conclusion")

best_overall = metrics.loc[
    metrics[
        ["Precision@10", "Recall@10", "NDCG@10"]
    ].mean(axis=1).idxmax()
]

st.success(
    f"Among the evaluated models, {best_overall['Model']} "
    f"has the highest average value across the three metrics."
)

st.write("""
The evaluation results allow us to compare the strengths
of Content-Based Filtering, Collaborative Filtering (ALS)
and the Hybrid approach.

The best model depends on the evaluation metrics and
the validation dataset. The hybrid approach combines
both recommendation strategies to benefit from their
complementary characteristics.
""")


# ==========================================
# 12. FOOTER
# ==========================================

st.write("")
st.divider()

st.caption("MIND News Recommendation System")

st.caption(
    "Content-Based Filtering · ALS · Hybrid Recommendation"
)

st.caption("Model Evaluation")
