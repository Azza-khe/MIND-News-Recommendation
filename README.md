# MIND News Recommendation System

A **Hybrid News Recommendation System** that combines Content-Based Filtering, Collaborative Filtering (ALS), and Popularity-Based Recommendation to deliver personalized news recommendations.

## Project Overview

This project explores different recommendation strategies using the **Microsoft News Dataset (MIND)**. It aims to recommend relevant news articles based on users' reading histories, article content, and collective user interactions.

The system implements and evaluates multiple recommendation approaches before combining them into a hybrid model.

## Objectives

- Explore and analyze the MIND dataset.
- Build a Content-Based Recommendation model using TF-IDF and cosine similarity.
- Implement a Popularity-Based recommendation baseline.
- Develop a Collaborative Filtering model using Alternating Least Squares (ALS).
- Combine recommendation models through weighted score fusion.
- Evaluate model performance using ranking metrics.
- Build an interactive web application with Streamlit.

## Recommendation Approaches

### 1. Content-Based Filtering

Recommends articles based on their textual similarity to a user's reading history.

- TF-IDF vectorization
- Article representation using titles, abstracts, categories, and subcategories
- User profile construction from previously read articles
- Cosine similarity for ranking recommendations

### 2. Popularity-Based Recommendation

Uses historical user interactions to identify popular news articles.

- Counts article interactions
- Ranks candidate articles according to popularity
- Provides a baseline recommendation strategy

### 3. Collaborative Filtering – ALS

Uses implicit user-item interactions to learn latent representations of users and articles.

- User-item interaction matrix
- Alternating Least Squares (ALS)
- Latent factor representations
- Personalized recommendation scores

### 4. Hybrid Recommendation

Combines Content-Based Filtering and ALS through weighted score fusion.

**Hybrid Score:**

`Hybrid Score = α × Content-Based Score + (1 − α) × ALS Score`

The scores are normalized before fusion. The parameter α controls the contribution of each model.

The selected configuration in the experiments is **α = 0.8**.

## Evaluation Metrics

The recommendation models are evaluated using:

- **Precision@K:** Proportion of relevant articles among the top K recommendations.
- **Recall@K:** Proportion of relevant articles retrieved among all relevant candidates.
- **NDCG@K:** Measures the quality of the ranking, giving more importance to relevant articles appearing near the top.
- **Coverage:** Measures the proportion of the article catalogue recommended by the system.

## Technology Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy, SciPy
- **Machine Learning:** Scikit-learn
- **Collaborative Filtering:** Implicit (ALS)
- **Text Processing:** TF-IDF, Cosine Similarity
- **Data Visualization:** Matplotlib
- **Web Application:** Streamlit
- **Development Tools:** Jupyter Notebook, VS Code, Git, GitHub

## Project Structure

```text
MIND-News-Recommendation/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_content_based_model.ipynb
│   ├── 03_popularity_baseline.ipynb
│   ├── 04_collaborative_filtering_ALS.ipynb
│   └── 05_hybrid_model.ipynb
│
├── streamlit_app/
│   ├── artifacts/
│   ├── pages/
│   │   ├── 1_Model_Evaluation.py
│   │   ├── 2_Recommendation_Demo.py
│   │   └── 3_Cold_Start.py
│   ├── app.py
│   ├── recommender.py
│   └── test_recommender.py
│
├── data/
│   └── (dataset and processed data – not included)
│
├── results/
│
├── arborescence.txt
└── README.md
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Azza-khe/MIND-News-Recommendation.git
cd MIND-News-Recommendation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install streamlit numpy pandas scipy joblib implicit
```

Install any additional dependencies required by the notebooks or application.

### 4. Run the Streamlit application

```bash
python -m streamlit run streamlit_app/app.py
```

The application will be available at:

`http://localhost:8501`

## Streamlit Application

The interactive application provides:

- **Dashboard:** Overview of the project and recommendation approaches.
- **Model Evaluation:** Comparison of recommendation model performance.
- **Recommendation Demo:** Generate personalized news recommendations for a selected user.
- **Cold Start Analysis:** Explore recommendation strategies for users or articles with limited interaction history.

## Dataset

This project uses the **Microsoft News Dataset (MIND)**.

Official dataset website: https://msnews.github.io/

The original dataset and intermediate processed files are not included in this repository because of their size. Download the dataset separately when reproducing the notebook experiments.

The Streamlit application uses the precomputed artifacts provided in `streamlit_app/artifacts/`.

## Future Improvements

- Improve cold-start recommendation strategies.
- Explore additional hybrid recommendation techniques.
- Optimize model performance and scalability.
- Enhance recommendation diversity and personalization.
- Deploy the application online.

---

**Developed by Azza KHECHINE**  
Engineering Student – National School of Computer Science (ENSI), Tunisia

GitHub: https://github.com/Azza-khe
