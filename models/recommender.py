import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

TFIDF = joblib.load("models/recommender_tfidf.joblib")
KNN = joblib.load("models/recommender_knn.joblib")

vectorizer = TFIDF["vectorizer"]
X_tfidf = TFIDF["X"]
df_base = TFIDF["df"]

knn = KNN["knn"]
X_knn = KNN["X"]
sintoma_cols = KNN["sintoma_cols"]

def recomendar(sintomas_list, top_k=10):
    # --- TF-IDF ---
    query_doc = " ".join(sintomas_list)
    q_vec = vectorizer.transform([query_doc])
    tfidf_scores = cosine_similarity(q_vec, X_tfidf).ravel()

    # --- KNN ---
    # --- KNN (com distância) ---
    user_vec = pd.DataFrame([{c: int(c in sintomas_list) for c in sintoma_cols}])
    pool = max(top_k * 10, 50)   # pega uma “piscina” maior
    distances, indices = knn.kneighbors(user_vec, n_neighbors=pool)


    df = df_base.copy()
    df["score_tfidf"] = tfidf_scores
    df["score_knn"] = 0.0

    for dist, idx in zip(distances[0], indices[0]):
        df.loc[idx, "score_knn"] = 1 - dist  # quanto menor a distância, maior o score


    # ensemble simples
    df["score"] = 0.6 * df["score_tfidf"] + 0.4 * df["score_knn"]
    
    if "substancia_limpa" in df.columns:
        df = df.sort_values("score", ascending=False)
        df = df.drop_duplicates(subset=["substancia_limpa"], keep="first")

    if "doc" not in df.columns:
        df["doc"] = df[sintoma_cols].apply(
            lambda row: " ".join([c for c, v in row.items() if v == 1]),
            axis=1
    )


    return df.head(top_k).reset_index(drop=True)



