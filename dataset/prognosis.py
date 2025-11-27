import pandas as pd

df = pd.read_csv("dataset/tabela_anvisa_limpa.csv")

def classificar_indicacao(txt: str) -> str:
    if not isinstance(txt, str):
        return "outros"
    t = txt.lower()

    # DOR / FEBRE / MÚSCULO / ARTICULAÇÃO 
    if "dor e inflamação do sistema musculoesquelético" in t:
        return "dor_musculoesqueletica"
    if "dores musculares" in t or "contraturas musculares" in t:
        return "dor_muscular"
    if "cefaleia e enxaqueca" in t or ("cefaleia" in t and "enxaqueca" in t):
        return "cefaleia_enxaqueca"
    if "cefaleia tensional" in t:
        return "cefaleia_tensional"
    if "cefaleia" in t:
        return "cefaleia"
    if "dor de dente" in t:
        return "dor_dente"
    if "febre" in t and "gripes e resfriados comuns" in t:
        return "febre_gripe_resfriado"
    if "febre" in t:
        return "febre_dor_leve"

    # GRIPE / RESFRIADO / RINITE / SINUSITE 
    if "gripe e resfriado comuns" in t:
        return "gripe_resfriado"
    if "sintomas de gripe, resfriado, rinite e sinusite" in t:
        return "gripe_resfriado_rinite_sinusite"
    if "congestão nasal" in t and "rinite" in t:
        return "rinite_congestao_nasal"
    if "congestão nasal" in t:
        return "congestao_nasal"
    if "rinite alérgica" in t:
        return "rinite_alergica"

    # TOSSE / SECREÇÃO BRONCOPULMONAR 
    if "tosse seca, sem catarro" in t:
        return "tosse_seca"
    if "tosse seca" in t:
        return "tosse_seca"
    if "tosse" in t:
        return "tosse"
    if "secreções mucosas densas e viscosas nas vias respiratórias" in t:
        return "secrecao_broncopulmonar"

    # AZIA / REFLUXO / MÁ DIGESTÃO / CÓLICAS / DIARREIA / CONSTIPAÇÃO
    if "azia" in t or "queimação" in t or "regurgitação ácida" in t:
        return "azia_refluxo"
    if "dor de estômago" in t or "má digestão" in t or "distensão abdominal" in t or "eructação" in t or "flatulência" in t:
        return "dispepsia_distensao"
    if "cólica" in t and "gastrintestinais" in t:
        return "colicas_gastrintestinais"
    if "diarreia aguda" in t or ("reidratação" in t and "diarreia" in t):
        return "diarreia_aguda_reidratacao"
    if "diarreia" in t:
        return "diarreia"
    if "prisão de ventre" in t or "laxativo" in t or "constipação intestinal" in t:
        return "constipacao_intestinal"
    if "regularização do hábito intestinal" in t:
        return "disturbios_habito_intestinal"

    #  PELE / DERMATITE / MICOSE / ACNE / HERPES / PEDICULOSE / ESCABIOSE
    if "acne vulgar" in t and "rosácea" in t:
        return "acne_rosacea"
    if "acne vulgar" in t:
        return "acne_vulgar"
    if "dermatites, eczemas, eritema solar, queimadura de primeiro grau e picadas de inseto" in t:
        return "dermatite_eczema_queimaduras_picadas"
    if "micoses superficiais de pele e unha" in t:
        return "micose_pele_unha"
    if "micoses superficiais de pele" in t:
        return "micose_pele"
    if "micoses de unha" in t or "infecções fúngicas das unhas" in t:
        return "onicomicose"
    if "dermatite seborreica" in t and "couro cabeludo" in t:
        return "dermatite_seborreica_couro_cabeludo"
    if "dermatite seborreica" in t:
        return "dermatite_seborreica"
    if "dermatite de fraldas" in t:
        return "dermatite_fraldas"
    if "brotoeja" in t:
        return "brotoeja"
    if "caspa" in t:
        return "caspa_dermatite_couro_cabeludo"
    if "herpes labial" in t:
        return "herpes_labial"
    if "pediculose" in t:
        return "pediculose"
    if "escabiose" in t:
        return "escabiose"
    if "prurido" in t and "picada de insetos" in t:
        return "prurido_picada_insetos"
    if "prurido" in t:
        return "prurido"
    if "ferimentos superficiais na pele" in t or "ferimentos leves" in t or "escaras" in t or "fissuras da pele" in t:
        return "ferimentos_superficiais"
    if "irritações da pele" in t and "exposição ao sol" in t:
        return "irritacao_pele_solar"
    if "irritações da pele" in t:
        return "irritacao_pele"

    # CANDIDÍASE / INFECÇÕES FÚNGICAS GENITAIS
    if "candidíase vaginal e perianal" in t:
        return "candidiase_vaginal_perianal"
    if "candidíase vaginal" in t:
        return "candidiase_vaginal"
    if "candidíase vulvar e peniana" in t or "candidíase vulvar" in t:
        return "candidiase_vulvar_peniana"

    # HEMORROIDAS / REGIÃO ANAL
    if "hemorroidas" in t:
        return "hemorroidas"

    # OLHOS 
    if "lubrificante oftálmico" in t or "lágrima artificial" in t:
        return "olho_seco_lubrificacao"
    if "irritação e prurido oculares" in t:
        return "irritacao_prurido_ocular"

    # BOCA / GARGANTA
    if "inflamações e dores na mucosa da boca" in t or "dor de garganta" in t:
        return "inflamacao_boca_garganta"
    if "aftas" in t:
        return "aftas_inflamacao_bucal"
    if "desconfortos bucais da primeira dentição" in t:
        return "desconforto_primeira_denticao"

    # FÍGADO
    if "auxiliar no tratamento dos distúrbios do fígado" in t:
        return "disturbios_figado"

    # DIABETE / APETITE / MINERALIZAÇÃO / TABACO
    if "estimulante do apetite" in t:
        return "estimulo_apetite"
    if "mineralização óssea" in t:
        return "mineralizacao_ossea"
    if "dependência do tabaco" in t:
        return "dependencia_tabaco"

    # URINÁRIO
    if "dor, ardor, desconforto para urinar" in t:
        return "disuria_desconforto_urinario"

    # PARASITAS / VERMES 
    if "ascaridíase" in t or "enterobíase" in t or "tricuríase" in t or "anci" in t or "teníase" in t:
        return "verminoses_intestinais"

    # CINETOSE / ENJOO
    if "cinetose" in t:
        return "cinetose_enjoo"

    # VASCULAR / HEMATOMAS
    if "flebites e tromboflebites superficiais" in t or "hematomas e contusões" in t or "varizes" in t:
        return "processos_inflamatorios_veias_hematomas"

    # HIDRATAÇÃO / DIARREIA
    if "reidratação" in t and "diarreia aguda" in t:
        return "diarreia_aguda_reidratacao"
    

    if "dores moderadas a fortes" in t:
        return "dor_moderada_forte"

    if "verrugas comuns" in t:
        return "verrugas_comuns"

    if "alopecia androgenética" in t:
        return "alopecia_androgenetica"

    if "mucosa nasal ressecada" in t or "mucosa nasal irritada" in t:
        return "mucosa_nasal_ressecada"

    if "dor de ouvido" in t or "remoção de cerume" in t:
        return "dor_ouvido_cerume"

    if "inflamação da garganta" in t:
        return "inflamacao_boca_garganta"

    if "rosácea" in t:
        return "rosacea"

    if "impetigo" in t or "furúnculo" in t or "úlcera cutânea" in t:
        return "infeccao_bacteriana_pele"

    if "primeira dentição" in t or "desconfortos bucais" in t:
        return "desconforto_primeira_denticao"

    if "pele seca e áspera" in t or "espessamento da pele" in t:
        return "pele_seca_espessada"

    # correçãaaaao
    if "candisíase" in t or "candisíase vaginal e peniana" in t:
        return "candidiase_vulvar_peniana"

    if "micoses superficiais da pele" in t:
        return "micose_pele"


    # fallback
    return "outros"


df["diagnostico_regra"] = df["Indicacao"].apply(classificar_indicacao)

# ver quantos caíram em cada diagnóstico
print(df["diagnostico_regra"].value_counts())


# ver o "outros" --> fallback
outros = df[df["diagnostico_regra"] == "outros"]["Indicacao"]
for linha in outros:
    print(linha)


df.to_csv("dataset/tabela_diagnostico.csv", index=False, encoding="utf-8-sig")
print("Arquivo salvo com sucesso!")



def main():
    print("Carregando CSV...")
    df = pd.read_csv("dataset/tabela_anvisa_limpa.csv", encoding="utf-8")

    df["diagnostico_regra"] = df["Indicacao"].apply(classificar_indicacao)
    ohe = pd.get_dummies(df["diagnostico_regra"], prefix="diag")

    
    ohe = ohe.astype(int)

    df_final = pd.concat([df, ohe], axis=1)

    df_final.to_csv("dataset/tabela_diagnostico_onehot.csv", index=False, encoding="utf-8-sig")

    print("csv salvo")


if __name__ == "__main__":
    main()