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
		produtos = [p.text for p in WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.ProductCardNamestyles__ProductNameStyles-sc-1l5s4fj-0.cuGHOR.product-card-name"))
		)]

		precos = [pr.text for pr in WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Pricestyles__ProductPriceStyles-sc-118x8ec-0.bMEbfn.price"))
		)]

		marcas = [m.text for m in WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-brand"))
		)]

		adicional = [a.text for a in WebDriverWait(driver, 20).until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.additional-info"))
		)]
                                                                                
		for nome, preco, marca, dose in zip(produtos, precos, marcas, adicional):
			# primeiro buscamos o ID da marca (se não existir, criar)
			resultado = sessao.execute(
				text("SELECT idmarca FROM marca WHERE nomeMarca = :nome"),
				{"nome": marca}
			).fetchone()

			if resultado:
				id_marca = resultado[0]
			else:
				sessao.execute(
					text("INSERT INTO marca (nomeMarca) VALUES (:nome)"),
					{"nome": marca}
				)
				id_marca = sessao.execute(
					text("SELECT idmarca FROM marca WHERE nomeMarca = :nome"),
					{"nome": marca}
				).fetchone()[0]

			# depois, vamos inserir medicamento com FK correta
			sessao.execute(
				text("""
				INSERT INTO medicamentos (nomeMedicamento, preco, dosagem, marca)
				VALUES (:nomeMedicamento, :preco, :dosagem, :marca)
				"""),
				{
					"nomeMedicamento": nome,
					"preco": float(preco.replace("R$", "").replace(",", ".").strip()),
					"dosagem": dose,
					"marca": id_marca,
				}
			)


# df = pd.DataFrame(dados)
# df.to_csv("saida.csv", index=False, encoding="utf-8-sig")

driver.quit()
