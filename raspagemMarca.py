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

for n in range(1, 9):
	with Session(engine) as sessao, sessao.begin():
		driver.get(f"{config.urlbase}?p={n}")
		marcas = [m.text for m in WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-brand"))
		)]                                                                   
		for marca in marcas:

			laboratorio ={
				'nomeMarca': marca
			}
			sessao.execute(text("INSERT INTO marca (nomeMarca) VALUES (:nomeMarca)"), laboratorio)

# df = pd.DataFrame(dados)
# df.to_csv("saida.csv", index=False, encoding="utf-8-sig")

driver.quit()
