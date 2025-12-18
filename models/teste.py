from recommender import recomendar

df = recomendar(
    ["febre", "tosse_seca", "dor_de_garganta"],
    top_k=5
)

print(df[[
    "nomeMedicamento",
    "score",
    "score_tfidf",
    "score_knn"
]])
