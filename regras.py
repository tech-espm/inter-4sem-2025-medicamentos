# regras.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd


@dataclass
class RegraResultado:
    df: pd.DataFrame
    alertas: List[str]


# Sintomas que disparam ALERTA (não é diagnóstico; é triagem de segurança)
SINTOMAS_ALERTA = {
    "dor_no_peito": "Dor no peito pode indicar algo sério. Procure atendimento imediato.",
    "falta_de_ar": "Falta de ar pode indicar algo sério. Procure atendimento imediato.",
    "desconforto_para_urinar": "Se houver dor forte, febre ou sangue, procure avaliação médica.",
}

# Regras simples de "boost" (aumenta score de itens que combinem com o contexto)
BOOSTS = [
    # (condição: sintomas presentes, termos que se o medicamento tiver -> ganha boost, valor)
    ({"febre"}, ["antiterm", "antipiret"], 0.15),
    ({"dor", "cefaleia", "enxaqueca"}, ["analges", "antiinflam"], 0.12),
    ({"congestao_nasal", "coriza"}, ["descongestion", "rinite", "antialerg"], 0.10),
    ({"tosse_seca"}, ["antituss", "tosse"], 0.10),
    ({"diarreias_de_diferentes_causas"}, ["antidiarre", "reidrat", "hidrata"], 0.12),
]

# Regras simples de "evitar" (se sintomas indicam X, derruba itens que sejam Y)
PENALIDADES = [
    # (condição: sintomas presentes, termos a penalizar, valor)
    ({"diarreias_de_diferentes_causas"}, ["lax", "laxante", "laxativo"], 0.25),
    ({"prisao_de_ventre", "constipacao_intestinal"}, ["antidiarre"], 0.25),
    ({"tosse_seca"}, ["expector", "mucolit"], 0.15),
]


def aplicar_regras(sintomas_list: List[str], df_recs: pd.DataFrame,
                   texto_col: str = "doc", score_col: str = "score") -> RegraResultado:
    """
    Espera df_recs com colunas:
      - score_col: float (score do TF-IDF/KNN)
      - texto_col: str  (texto do medicamento: indicacoes/classe/principio_ativo etc)
    """
    df = df_recs.copy()

    # Alertas
    alertas = []
    sset = set(sintomas_list)
    for s, msg in SINTOMAS_ALERTA.items():
        if s in sset:
            alertas.append(msg)

    # Normaliza texto para match simples
    if texto_col in df.columns:
        texto = df[texto_col].fillna("").astype(str).str.lower()
    else:
        # se não tiver, cria vazio (regras não quebram)
        texto = pd.Series([""] * len(df), index=df.index)

    # Boosts
    if score_col not in df.columns:
        df[score_col] = 0.0

    for cond_sintomas, termos, boost in BOOSTS:
        if cond_sintomas & sset:
            mask = False
            for t in termos:
                mask = mask | texto.str.contains(t)
            df.loc[mask, score_col] = df.loc[mask, score_col] + boost

    # Penalidades
    for cond_sintomas, termos, pen in PENALIDADES:
        if cond_sintomas & sset:
            mask = False
            for t in termos:
                mask = mask | texto.str.contains(t)
            df.loc[mask, score_col] = df.loc[mask, score_col] - pen

    df = df.sort_values(score_col, ascending=False).reset_index(drop=True)

    return RegraResultado(df=df, alertas=alertas)
