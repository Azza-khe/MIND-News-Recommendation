
import streamlit as st
import pandas as pd

from recommender import (
    item_interaction_counts,
    news_catalog,
    recommend_news,
    idx_to_item,
    user_to_idx
)


# ==========================================
# 1. CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Cold Start | MIND News",
    page_icon=":material/ac_unit:",
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

st.title("Cold Start Management")

st.write("""
The Cold Start problem occurs when the recommendation system
lacks sufficient interaction information to generate
personalized recommendations.

This page presents the statistics of this problem and
demonstrates the strategies implemented to address it.
""")

st.divider()


# ==========================================
# 5. WARM START / COLD START STATISTICS
# ==========================================

st.subheader("Article interaction statistics")

total_articles = len(item_interaction_counts)

warm_count = int((item_interaction_counts > 0).sum())
cold_count = int((item_interaction_counts == 0).sum())

warm_percentage = warm_count / total_articles * 100
cold_percentage = cold_count / total_articles * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Articles",
        f"{total_articles:,}"
    )

with col2:
    st.metric(
        "Warm Start Articles",
        f"{warm_count:,}",
        f"{warm_percentage:.2f}%"
    )

with col3:
    st.metric(
        "Cold Start Articles",
        f"{cold_count:,}",
        f"{cold_percentage:.2f}%"
    )


# Chart
chart_data = pd.DataFrame({
    "Type": ["Warm Start", "Cold Start"],
    "Number of Articles": [warm_count, cold_count]
}).set_index("Type")

st.write("")

with st.container(border=True):

    st.markdown("### Distribution of article interactions")

    st.bar_chart(chart_data)

    st.caption(
        "Warm Start: articles with at least one training interaction. "
        "Cold Start: articles with no training interactions."
    )


st.info(
    f"{cold_percentage:.2f}% of the articles have no interactions "
    "in the training interaction matrix. The system can still "
    "recommend these articles using their textual content."
)

st.divider()


# ==========================================
# 6. EXAMPLES OF COLD START ARTICLES
# ==========================================

st.subheader("Articles without interactions")

st.write("""
These articles have no interaction in the training matrix.
However, their textual information is available for
Content-Based recommendations using TF-IDF.
""")

# Build article IDs from the inverse mapping
cold_articles = pd.DataFrame({
    "news_id": [
        idx_to_item[i]
        for i in range(len(item_interaction_counts))
    ],
    "interaction_count": item_interaction_counts
})

# Keep only articles with zero interactions
cold_articles = cold_articles[
    cold_articles["interaction_count"] == 0
]

# Add article information
cold_articles = cold_articles.merge(
    news_catalog[["news_id", "title", "category"]],
    on="news_id",
    how="left"
)

# Display only 20 examples to keep the interface responsive
st.caption(
    f"Showing 20 examples out of {cold_count:,} Cold Start articles."
)

st.dataframe(
    cold_articles[
        ["news_id", "title", "category"]
    ].head(20),
    use_container_width=True,
    hide_index=True
)

st.divider()


# ==========================================
# 7. TEST: UNKNOWN USER
# ==========================================

st.subheader("Test: New User")

st.write("""
Enter an identifier that does not exist in the training data.
The system will use the Popularity-Based strategy to recommend
the most popular articles.
""")

unknown_user = st.text_input(
    "New user ID",
    value="U_UNKNOWN",
    key="unknown_user_input"
)

if st.button(
    "Test New User",
    icon=":material/person_search:",
    key="test_unknown_user"
):

    if not unknown_user.strip():

        st.warning("Please enter a user ID.")

    elif unknown_user.strip() in user_to_idx:

        st.warning(
            "This user already exists in the training data. "
            "Please enter an unknown user ID."
        )

    else:

        result = recommend_news(
            unknown_user.strip(),
            top_n=10
        )

        st.success(
            "Popularity-Based strategy successfully applied."
        )

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

st.divider()


# ==========================================
# 8. TEST: COLD START ARTICLES
# ==========================================

st.subheader("Test: New Articles")

st.write("""
For a known user, the system can recommend articles without
interactions by using their textual characteristics and
the user's Content-Based profile.
""")

known_user = st.text_input(
    "Known user ID",
    value="U100",
    key="known_user_input"
)

if st.button(
    "Test Cold Start Recommendations",
    icon=":material/article:",
    key="test_cold_articles"
):

    if not known_user.strip():

        st.warning("Please enter a user ID.")

    elif known_user.strip() not in user_to_idx:

        st.error(
            "This user does not exist in the training data. "
            "Please enter a known user ID."
        )

    else:

        result = recommend_news(
            known_user.strip(),
            top_n=20
        )

        cold_recommendations = result[
            result["strategy"] ==
            "Content-Based (Cold Start Article)"
        ]

        if not cold_recommendations.empty:

            st.success(
                f"{len(cold_recommendations)} Cold Start article(s) "
                "found among the recommendations."
            )

            st.dataframe(
                cold_recommendations,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No Cold Start articles were found among the "
                "top 20 recommendations for this user."
            )

st.divider()


# ==========================================
# 9. COLD START SOLUTIONS
# ==========================================

st.subheader("Strategies used to solve Cold Start")

with st.container(border=True):

    st.markdown("### Recommendation strategies")

    strategies = pd.DataFrame({
        "Situation": [
            "Unknown user",
            "Known user without history",
            "Article without interactions",
            "Known user and known article"
        ],
        "Strategy": [
            "Popularity-Based",
            "Popularity-Based",
            "Content-Based",
            "Hybrid CB + ALS"
        ]
    })

    st.dataframe(
        strategies,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### How do these strategies work?")

    st.markdown("""
    **1. Popularity-Based**

    Recommends the most popular articles based on training
    interactions when the user has no usable history.

    **2. Content-Based Filtering**

    Uses TF-IDF representations of article content and
    the user's profile to recommend articles, including
    articles without previous interactions.

    **3. Hybrid CB + ALS**

    Combines Content-Based similarity and ALS scores
    for articles with interaction history.
    """)


# ==========================================
# 10. FOOTER
# ==========================================

st.write("")
st.divider()

st.caption("MIND News Recommendation System")

st.caption(
    "Content-Based Filtering · ALS · Hybrid Recommendation"
)

st.caption(
    "Cold Start Management"
)
