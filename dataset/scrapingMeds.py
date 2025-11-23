import requests
import pandas as pd
from io import StringIO

url = "https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&tipo=INM&numeroAto=00000285&seqAto=000&valorAno=2024&orgao=DC/ANVISA/MS&codTipo=&desItem=&desItemFim=&cod_menu=1696&cod_modulo=134&pesquisa=true"
headers = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(url, headers=headers)
resp.encoding = "latin-1"
html = resp.text



tabelas = pd.read_html(StringIO(html))
df = tabelas[0]

#limpa a coluna indice que estava vindo
df = df.iloc[1:].reset_index(drop=True)

df.columns = [
    "Farmaco",
    "Subgrupo",
    "Forma_farmaceutica",
    "Concentracao_maxima",
    "Indicacao"
]

df.to_csv("dataset/tabela_anvisa_limpa.csv", index=False, encoding="utf-8-sig")

