from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd 

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)
dados = []  # Moved initialization of 'dados' here

for n in range(1, 146):
    driver.get(f"https://www.drogasil.com.br/medicamentos/medicina-natural.html?p={n}")
    precos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Pricestyles__ProductPriceStyles-sc-118x8ec-0.bMEbfn.price"))
    )
    marcas = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-brand"))
    )
    produtos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.ProductCardNamestyles__ProductNameStyles-sc-1l5s4fj-0.cuGHOR.product-card-name"))
    )

    for nome, preco, marca in zip(produtos, precos, marcas):
        dados.append({
            "Produto": nome.text,
            "Preço": preco.text,
            "Marca": marca.text
        })

df = pd.DataFrame(dados)
df.to_csv("medicamentos_naturais_drogasil.csv", index=False, encoding="utf-8-sig")

driver.quit()