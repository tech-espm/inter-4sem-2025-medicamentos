from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
import config

engine = create_engine(config.conexao_banco)

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)
dados = [] 

for n in range(1, 181):
	with Session(engine) as sessao, sessao.begin():
		driver.get(f"{config.urlbase}?page={n}")
		precos = WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sc-17561f71-0.hHHZnG.price"))
		)
		marcas = WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-brand"))
		)
		produtos = WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.sc-21abf319-0.eJHuBu.product-card-name"))
		)                                                                                         

		for nome, preco, marca in zip(produtos, precos, marcas):
			medicamento = {
				'nome': nome.text,
				'preco': float(preco.text.replace("R$", "").replace(",", ".").strip()),
				'marca': marca.text
			}
			sessao.execute(text("INSERT INTO medicamento (nome, preco, marca) VALUES (:nome, :preco, :marca)"), medicamento)

# df = pd.DataFrame(dados)
# df.to_csv("saida.csv", index=False, encoding="utf-8-sig")

driver.quit()
