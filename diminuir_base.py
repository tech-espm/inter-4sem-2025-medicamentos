import pandas as pd
import unicodedata

df = pd.read_csv("dataset_final_medicamentos.csv")

def limpar_texto(t):
    if pd.isna(t):
        return ""
    t = str(t).lower().strip()
    # acentos
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    # facilitar o match
    t = t.replace("mg", " mg")
    t = t.replace("ml", " ml")
    t = t.replace("-", " ")
    t = " ".join(t.split())
    t = t.encode("ascii", errors="ignore").decode("utf-8")
    return t

df["subgrupo"] = df["Subgrupo terapêutico ou farmacológico"].apply(limpar_texto)


# df["subgrupo"] = (
#     df["Subgrupo terapêutico ou farmacológico"]
#       .astype(str)
#       .str.lower()
#       .str.normalize("NFKD")
#       .str.encode("ascii", errors="ignore")
#       .str.decode("utf-8")
# )

# Definir subgrupos d
subgrupos_desejados = ["antiinflamatorios e antirreumaticos nao esteroidais", "expectorantes, excluindo associacoes com antitussigenos", "analgesicos e antipiretico"]

# Criar coluna identificando se pertence ao subgrupo desejado
df["subgrupo_desejado"] = df["subgrupo"].apply(
    lambda x: any(s in x for s in subgrupos_desejados)
)

#  Filtrar
df_filtrada = df[df["subgrupo_desejado"] == True].copy()

# print("Tamanho da base original:", df.shape)
# print("Tamanho da base filtrada:", df_filtrada.shape)


df_filtrada.to_csv("base_filtrada_subgrupos.csv", index=False, encoding="utf-8-sig")
