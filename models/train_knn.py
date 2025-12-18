import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib
from pathlib import Path

DATA_PATH = Path("dataset_final_medicamentos.csv")
OUT_PATH = Path("models/recommender_knn.joblib")

META_COLS = {
    "idMedicamentos", "nomeMedicamento",
    "Subgrupo terapêutico ou farmacológico",
    "preco", "marca", "quantidade", "dosagem",
    "substancia", "substancia_limpa", "avaliacao",
    "dataPreco", "idMedicamento_base", "farmacos_encontrados"
}

def main():
    df = pd.read_csv(DATA_PATH)
    sintoma_cols = [c for c in df.columns if c not in META_COLS]

    X = df[sintoma_cols].astype(int)

    knn = NearestNeighbors(
        n_neighbors=10,
        metric="cosine"
    )
    knn.fit(X)

    OUT_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(
        {"knn": knn, "X": X, "df": df, "sintoma_cols": sintoma_cols},
        OUT_PATH
    )

    print("KNN treinado e salvo com sucesso.")

if __name__ == "__main__":
    main()
