
import streamlit as st
import pandas as pd

from recommender import recommend_news


# ==========================================
# 1. CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Recommendation Demo | MIND News",
    page_icon=":material/newspaper:",
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

st.title("Recommendation Demo")

st.write("""
Test our recommendation system by entering a user ID.
The system analyzes the user's interaction history and
generates personalized news recommendations.
""")

st.divider()


# ==========================================
# 5. RECOMMENDATION PARAMETERS
# ==========================================

st.subheader("Recommendation parameters")

with st.container(border=True):

    col1, col2 = st.columns(2, gap="large")

    with col1:

        user_id = st.text_input(
            "User ID",
            value="U100",
            help="Example: U100. You can also enter an unknown user ID."
        )

    with col2:

        top_n = st.selectbox(
            "Number of articles to recommend",
            [5, 10, 15, 20],
            index=1
        )

    st.write("")

    alpha = st.slider(
        "Content-Based weight (alpha)",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.1,
        help="The ALS weight is equal to 1 - alpha."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Content-Based weight",
            f"{alpha:.0%}"
        )

    with col2:
        st.metric(
            "ALS weight",
            f"{1 - alpha:.0%}"
        )

    st.progress(alpha)

    st.caption(
        "Alpha controls the contribution of Content-Based Filtering "
        "in the hybrid recommendation score."
    )


# ==========================================
# 6. GENERATE RECOMMENDATIONS
# ==========================================

st.write("")

if st.button(
    "Generate Recommendations",
    type="primary",
    icon=":material/auto_awesome:",
    use_container_width=True
):

    if not user_id.strip():

        st.warning("Please enter a user ID.")

    else:

        try:

            with st.spinner("Generating personalized recommendations..."):

                recommendations = recommend_news(
                    user_id=user_id.strip(),
                    top_n=top_n,
                    alpha=alpha
                )

            st.session_state["recommendations"] = recommendations
            st.session_state["tested_user"] = user_id.strip()
            st.session_state["tested_alpha"] = alpha

        except Exception as e:

            st.error(f"An error occurred: {e}")


# ==========================================
# 7. DISPLAY RESULTS
# ==========================================

if "recommendations" in st.session_state:

    recommendations = st.session_state["recommendations"]
    tested_user = st.session_state["tested_user"]

    st.divider()

    st.subheader("Recommendation results")

    st.write(
        f"Results generated for user: **{tested_user}**"
    )

    # Identify the strategy used
    strategies = recommendations["strategy"].unique()

    if len(strategies) == 1:

        strategy = strategies[0]

        if strategy == "Popularity-Based":

            st.info(
                "Popularity-Based strategy: the user is unknown "
                "or has no interaction history."
            )

        elif strategy == "Content-Based (Cold Start Article)":

            st.info(
                "Content-Based strategy: recommendations include "
                "articles without previous interactions."
            )

        else:

            st.success(
                f"Strategy used: {strategy}"
            )

    else:

        st.success(
            "Hybrid recommendations with support for Cold Start articles."
        )

    # Results summary
    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Recommended articles",
            len(recommendations)
        )

    with col2:

        st.metric(
            "Content-Based weight",
            f"{st.session_state.get('tested_alpha', 0.8):.0%}"
        )

    # ======================================
    # Recommendation table
    # ======================================

    st.write("")

    st.subheader("Recommended articles")

    display_columns = [
        col for col in [
            "news_id",
            "title",
            "category",
            "score",
            "score_cb",
            "score_als",
            "strategy"
        ]
        if col in recommendations.columns
    ]

    st.dataframe(
        recommendations[display_columns],
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # Article details
    # ======================================

    st.write("")

    st.subheader("Recommendation details")

    for index, article in recommendations.iterrows():

        title = article.get("title", "Untitled article")

        with st.expander(
            f"{index + 1}. {title}"
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Article ID:** {article['news_id']}")
                st.write(f"**Category:** {article.get('category', 'N/A')}")
                st.write(f"**Strategy:** {article['strategy']}")

            with col2:

                st.write(
                    f"**Final score:** {article['score']:.4f}"
                )

                if pd.notna(article.get("score_cb")):

                    st.write(
                        f"**Content-Based score:** "
                        f"{article['score_cb']:.4f}"
                    )

                if pd.notna(article.get("score_als")):

                    st.write(
                        f"**ALS score:** "
                        f"{article['score_als']:.4f}"
                    )

    # ======================================
    # Download recommendations
    # ======================================

    st.write("")

    st.subheader("Export results")

    csv = recommendations.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download recommendations (CSV)",
        data=csv,
        file_name=f"recommendations_{tested_user}.csv",
        mime="text/csv",
        icon=":material/download:"
    )


# ==========================================
# 8. FOOTER
# ==========================================

st.write("")
st.divider()

st.caption("MIND News Recommendation System")

st.caption(
    "Content-Based Filtering · ALS · Hybrid Recommendation"
)

st.caption("Personalized Recommendation Demo")
