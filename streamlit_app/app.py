
import streamlit as st

# ==========================================
# 1. CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MIND News | Recommendation System",
    page_icon=":material/auto_awesome:",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
    background-color: #245D91;
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
# 4. HERO SECTION
# ==========================================

with st.container(border=True):

    st.caption("ARTIFICIAL INTELLIGENCE · NEWS PERSONALIZATION")

    st.title("MIND News Recommendation")

    st.write("""
    An intelligent news recommendation platform designed
    to deliver personalized articles by combining
    Content-Based Filtering and Collaborative Filtering.
    """)


# ==========================================
# 5. INTRODUCTION
# ==========================================

st.header("Discover our recommendation system")

st.write("""
This platform demonstrates an intelligent recommendation system
developed using the MIND news dataset. It combines textual analysis
and user interaction patterns to provide relevant and personalized
news recommendations.
""")


# ==========================================
# 6. RECOMMENDATION APPROACHES
# ==========================================

st.subheader("Recommendation approaches")

col1, col2 = st.columns(2, gap="large")

with col1:

    with st.container(border=True):

        st.markdown(
            ":material/article:",
            help="Content-Based Filtering"
        )

        st.subheader("Content-Based Filtering")

        st.write("""
        Analyzes the textual characteristics of news articles
        using TF-IDF representations.

        It recommends articles similar to the content previously
        interacted with by the user.
        """)


with col2:

    with st.container(border=True):

        st.markdown(
            ":material/hub:",
            help="Collaborative Filtering"
        )

        st.subheader("Collaborative Filtering — ALS")

        st.write("""
        Learns latent relationships between users and articles
        from their interaction history.

        It identifies recommendation patterns shared by users
        with similar interests.
        """)


# ==========================================
# 7. HYBRID MODEL
# ==========================================

st.write("")

st.subheader("Our Hybrid Recommendation Model")

with st.container(border=True):

    st.markdown("### Combining the strengths of two approaches")

    st.write("""
    Our hybrid model combines Content-Based Filtering and
    Collaborative Filtering to improve recommendation quality
    and address different recommendation scenarios.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Content-Based",
            value="80%"
        )

    with col2:
        st.metric(
            label="Collaborative Filtering",
            value="20%"
        )

    st.progress(0.8)

    st.caption(
        "Alpha = 0.8 : 80% Content-Based and 20% ALS."
    )


# ==========================================
# 8. PLATFORM FEATURES
# ==========================================

st.write("")

st.subheader("Explore the platform")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:

    with st.container(border=True):

        st.markdown(":material/analytics:")

        st.markdown("**Model Evaluation**")

        st.write("""
        Compare model performance using Precision@10,
        Recall@10 and NDCG@10.
        """)


with col2:

    with st.container(border=True):

        st.markdown(":material/newspaper:")

        st.markdown("**Personalized News**")

        st.write("""
        Enter a user ID and explore personalized
        news recommendations.
        """)


with col3:

    with st.container(border=True):

        st.markdown(":material/ac_unit:")

        st.markdown("**Cold Start Management**")

        st.write("""
        Explore the strategies used for new users
        and articles without interactions.
        """)


# ==========================================
# 9. FOOTER
# ==========================================

st.write("")
st.divider()

st.caption("MIND News Recommendation System")

st.caption(
    "Content-Based Filtering · ALS · Hybrid Recommendation"
)
