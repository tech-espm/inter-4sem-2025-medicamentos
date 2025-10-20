from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd 

driver = webdriver.Chrome() 
driver.set_page_load_timeout(300) 
driver.get("https://www.drogasil.com.br/medicamentos/medicamentos.html") 

precos = WebDriverWait(driver, 20).until( EC.presence_of_all_elements_located((By.CLASS_NAME, "Pricestyles__ProductPriceStyles-sc-118x8ec-0.bMEbfn.price")) ) 
marcas = WebDriverWait(driver, 20).until( EC.presence_of_all_elements_located((By.CLASS_NAME, "product-brand")) ) 
produtos = WebDriverWait(driver, 20).until( EC.presence_of_all_elements_located((By.CLASS_NAME, "price.price-from")) ) 
dosagem = WebDriverWait(driver, 20).until( EC.presence_of_all_elements_located((By.CLASS_NAME, "additional-info")) )

dados = []
for nome, preco, marca, dose in zip(produtos, precos, marcas, dosagem):
    dados.append({
        "Produto": nome.text,
        "Preço": preco.text,
        "Marca": marca.text,
        "Dosagem": dose.text
    })

df = pd.DataFrame(dados)
df.to_csv("medicamentos_drogasil.csv", index=False, encoding="utf-8-sig")

driver.quit()