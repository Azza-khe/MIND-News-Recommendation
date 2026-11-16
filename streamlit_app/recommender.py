
import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st

from pathlib import Path
from scipy.sparse import load_npz


# ==========================================
# 1. Chargement des fichiers sauvegardés
# ==========================================

BASE_DIR = Path(__file__).parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

@st.cache_resource
def load_artifacts():

    # Modèle ALS
    als_model = joblib.load(ARTIFACTS_DIR / "als_model.pkl")

    # Matrices
    user_item = load_npz(ARTIFACTS_DIR / "user_item.npz")
    tfidf_matrix = load_npz(ARTIFACTS_DIR / "tfidf_matrix.npz")
    user_profiles = load_npz(ARTIFACTS_DIR / "user_profiles.npz")

    # Mappings
    with open(ARTIFACTS_DIR / "mappings.json", "r") as f:
        mappings = json.load(f)

    user_to_idx = mappings["user_to_idx"]
    item_to_idx = mappings["item_to_idx"]

    # Catalogue des articles
    news_catalog = pd.read_csv(
        ARTIFACTS_DIR / "news_catalog.csv"
    )

    # Popularité
    popularity_df = pd.read_csv(
        ARTIFACTS_DIR / "popularity.csv"
    )

    # Nombre d'interactions par article
    item_interaction_counts = np.load(
        ARTIFACTS_DIR / "item_interaction_counts.npy"
    )

    return (
        als_model,
        user_item,
        tfidf_matrix,
        user_profiles,
        user_to_idx,
        item_to_idx,
        news_catalog,
        popularity_df,
        item_interaction_counts
    )


# Chargement des données
(
    als_model,
    user_item,
    tfidf_matrix,
    user_profiles,
    user_to_idx,
    item_to_idx,
    news_catalog,
    popularity_df,
    item_interaction_counts
) = load_artifacts()


# Mapping inverse : indice vers ID article
idx_to_item = {
    index: item
    for item, index in item_to_idx.items()
}


# ==========================================
# 2. Normalisation Min-Max
# ==========================================

def min_max_normalize(scores):

    min_score = scores.min()
    max_score = scores.max()

    if max_score == min_score:
        return np.zeros(len(scores))

    return (scores - min_score) / (max_score - min_score)


# ==========================================
# 3. Fonction de recommandation
# ==========================================

def recommend_news(user_id, top_n=10, alpha=0.8):

    # CAS 1 : utilisateur inconnu
    if user_id not in user_to_idx:

        result = popularity_df.head(top_n).merge(
            news_catalog[["news_id", "title", "category"]],
            on="news_id",
            how="left"
        )

        result["strategy"] = "Popularity-Based"
        result = result.rename(
            columns={"popularity": "score"}
        )

        return result[
            ["news_id", "title", "category", "score", "strategy"]
        ]

    user_idx = user_to_idx[user_id]

    # CAS 2 : utilisateur sans historique
    if user_item[user_idx].nnz == 0:

        result = popularity_df.head(top_n).merge(
            news_catalog[["news_id", "title", "category"]],
            on="news_id",
            how="left"
        )

        result["strategy"] = "Popularity-Based"
        result = result.rename(
            columns={"popularity": "score"}
        )

        return result[
            ["news_id", "title", "category", "score", "strategy"]
        ]

    # Articles déjà consultés/interagis par l'utilisateur
    seen_items = user_item[user_idx].indices

    # Articles candidats : exclure les articles déjà vus
    candidate_indices = np.setdiff1d(
        np.arange(len(item_to_idx)),
        seen_items
    )

    # ======================================
    # Score Content-Based
    # ======================================

    user_profile = user_profiles[user_idx]

    cb_scores = (
        user_profile @ tfidf_matrix[candidate_indices].T
    )

    cb_scores = cb_scores.toarray().ravel()

    cb_norm = min_max_normalize(cb_scores)

    # ======================================
    # Score ALS et Hybrid
    # ======================================

    has_interactions = (
        item_interaction_counts[candidate_indices] > 0
    )

    als_scores = np.full(
        len(candidate_indices),
        np.nan
    )

    final_scores = cb_norm.copy()

    warm_positions = np.where(has_interactions)[0]

    if len(warm_positions) > 0:

        warm_items = candidate_indices[warm_positions]

        user_vector = als_model.user_factors[user_idx]
        item_vectors = als_model.item_factors[warm_items]

        warm_als_scores = item_vectors @ user_vector

        als_norm = min_max_normalize(warm_als_scores)

        als_scores[warm_positions] = warm_als_scores

        final_scores[warm_positions] = (
            alpha * cb_norm[warm_positions]
            + (1 - alpha) * als_norm
        )

    # ======================================
    # Création du tableau des recommandations
    # ======================================

    recommendations = pd.DataFrame({
        "news_id": [
            idx_to_item[i] for i in candidate_indices
        ],
        "score": final_scores,
        "score_cb": cb_norm,
        "score_als": als_scores,
        "strategy": np.where(
            has_interactions,
            "Hybrid CB + ALS",
            "Content-Based (Cold Start Article)"
        )
    })

    recommendations = recommendations.merge(
        news_catalog[["news_id", "title", "category"]],
        on="news_id",
        how="left"
    )

    recommendations = recommendations.sort_values(
        "score",
        ascending=False
    ).head(top_n)

    return recommendations[
        [
            "news_id",
            "title",
            "category",
            "score",
            "score_cb",
            "score_als",
            "strategy"
        ]
    ].reset_index(drop=True)
