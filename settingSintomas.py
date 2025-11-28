
import pandas as pd
import re

df = pd.read_csv("dataset/tabela_diagnostico.csv")
df2= df.drop(columns=['Concentracao_maxima'])
    

sintomas = {
    "dor_muscular": (
        "dor muscular", "mialgia", "dor nos músculos"
    ),
    "dor_musculoesqueletica": (
        "dor e inflamação do sistema musculoesquelético",
        "musculoesquelético"
    ),
    "dor_moderada": ("dores moderadas",),
    "dor_forte": ("dores fortes",),
    "dor_leve": ("dores leves",),
    "dor_corpo": ("dor no corpo", "dores no corpo"),
    "dor_dente": ("dor de dente",),
    "cefaleia": ("cefaleia", "dor de cabeça"),
    "enxaqueca": ("enxaqueca",),
    "cefaleia_tensional": ("cefaleia tensional",),
    "contraturas_musculares": ("contraturas musculares",),
    "inflamacao_muscular": ("inflamação do sistema musculoesquelético",),
    "febre": ("febre",),

    "tosse": ("tosse",),
    "tosse_seca": ("tosse seca", "tosse irritativa"),
    "tosse_catarro": ("catarro", "tosse com catarro"),
    "secrecao_broncopulmonar": (
        "secreções mucosas densas",
        "secreções viscosas",
        "vias respiratórias"
    ),
    
    "gripe": ("gripe", "gripal"),
    "resfriado": ("resfriado",),
    "coriza": ("coriza",),
    "espirros": ("espirro",),
    "dor_garganta": ("dor de garganta",),
    "irritacao_garganta": (
        "irritação da garganta",
        "irritações da garganta"
    ),
    "congestao_nasal": ("congestão nasal", "nariz entupido"),
    "rinite_alergica": ("rinite alérgica",),
    "sinusite": ("sinusite",),

    "dermatite": ("dermatite", "eczema"),
    "dermatite_fraldas": ("dermatite de fraldas",),
    "dermatite_seborreica": ("dermatite seborreica",),
    "dermatite_atopica": ("dermatite atópica",),
    "eczema": ("eczema",),
    "brotoeja": ("brotoeja",),
    "eritema_solar": ("eritema solar",),
    "queimadura_leve": ("queimadura de primeiro grau",),
    "irritacao_pele": ("irritações da pele", "irritação na pele"),
    "irritacao_solar": ("irritações da pele de pequena intensidade",),
    "pele_ressecada": (
        "pele seca", "ressecamento da pele", "pele áspera", "descamação"
    ),
    "coceira": ("prurido", "coceira"),
    "picada_inseto": ("picada de inseto",),
    "urticaria": ("urticária",),
    "escoriacoes": ("escoriações",),
    "ferimentos_superficiais": (
        "ferimentos superficiais", "ferimentos leves", "escaras", "fissuras"
    ),
    "hematomas": ("hematomas", "contusões"),
    "caspa": ("caspa",),
    "psoriase": ("psoríase",),
    "rosacea": ("rosácea",),
    "verrugas": ("verrugas comuns",),

    "micose_pele": (
        "micoses superficiais da pele", 
        "micose de pele", 
        "frieira"
    ),
    "micose_unha": (
        "micose de unha", 
        "infecções fúngicas das unhas"
    ),
    "infeccao_fungica_mista": (
        "infecções mistas por fungos e bactérias",
    ),
    "candidiase_vaginal": ("candidíase vaginal",),
    "candidiase_peniana": ("candidíase peniana", "candidíase vulvar e peniana"),
    "candidiase_perianal": ("candidíase perianal",),
    "impetigo": ("impetigo",),
    "furunculo": ("furúnculo",),
    "ulcera_cutanea": ("úlcera cutânea",),
    "pediculose": ("pediculose", "piolho"),
    "escabiose": ("escabiose", "sarna"),

    "azia": ("azia", "queimação", "regurgitação ácida"),
    "refluxo": ("refluxo",),
    "ma_digestao": ("má digestão", "dispepsia"),
    "dor_estomago": ("dor de estômago",),
    "nausea": ("enjoo", "náusea"),
    "vomito": ("vômito", "vomito"),
    "distensao_abdominal": ("distensão abdominal",),
    "gases": ("flatulência", "eructação"),
    "colica_intestinal": ("cólicas gastrintestinais",),
    "colica_menstrual": ("cólicas menstruais",),
    "diarreia": ("diarreia",),
    "diarreia_aguda": ("diarreia aguda",),
    "desidratacao_diarreia": ("reidratação na diarreia",),
    "prisao_ventre": ("prisão de ventre", "constipação intestinal"),

    "aftas": ("aftas",),
    "inflamacao_boca": (
        "inflamações e dores na mucosa da boca",
        "estomatite"
    ),
    "ardencia_ocular": ("ardência nos olhos",),
    "irritacao_ocular": ("irritação e prurido oculares",),
    "olho_seco": ("lubrificante oftálmico", "lágrima artificial"),
    "mucosa_nasal_ressecada": ("mucosa nasal ressecada",),
    
    "dor_urinar": (
        "dor para urinar",
        "ardor para urinar",
        "desconforto para urinar"
    ),
    
    "ascaridiase": ("ascaridíase",),
    "enterobiase": ("enterobíase",),
    "tricuríase": ("tricuríase",),
    "ancilostomiase": ("ancilostomíase",),
    "teniase": ("teníase",),
    
    "cinetose": ("cinetose", "enjoo de movimento", "enjoo de viagem"),
    "perda_apetite": ("estimulante do apetite", "perda de apetite"),
    "abstinencia_nicotina": ("dependência do tabaco", "abstinência de nicotina"),
}


sintomas_regex = {
    nome: re.compile(r"|".join(re.escape(s) for s in sinonimos), flags=re.IGNORECASE)
    for nome, sinonimos in sintomas.items()
}

#criando as colunas
def detectar_sintoma(texto, regex):
    if not isinstance(texto, str):
        return 0
    return 1 if regex.search(texto) else 0

for nome, regex in sintomas_regex.items():
    df2[nome] = df2["Indicacao"].apply(lambda x: detectar_sintoma(x, regex))

print("Processamento concluído. Colunas adicionadas:")
print([col for col in df2.columns if col not in ("Farmaco", "Indicacao", "diagnostico_regra")])


df2.to_csv("dataset/tabela_multi_hot.csv", index=False, encoding="utf-8-sig")
print("Arquivo salvo em dataset/tabela_multi_hot.csv")

