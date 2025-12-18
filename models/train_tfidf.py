import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from pathlib import Path

DATA_PATH = Path("dataset_final_medicamentos.csv")
OUT_PATH = Path("models/recommender_tfidf.joblib")

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

    # cria "documento" textual a partir dos sintomas ativos
    df["doc"] = df[sintoma_cols].apply(
        lambda row: " ".join([col for col, v in row.items() if v == 1]),
        axis=1
    )

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["doc"])

    OUT_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(
        {"vectorizer": vectorizer, "X": X, "df": df},
        OUT_PATH
    )

    print("TF-IDF treinado e salvo com sucesso.")

if __name__ == "__main__":
    main()
