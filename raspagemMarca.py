from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import config

engine = create_engine(config.conexao_banco)

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)

for n in range(1, 9):

    with Session(engine) as sessao, sessao.begin():

        driver.get(f"{config.urlbase}?p={n}")

        marcas = [m.text.strip() for m in WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.product-brand"))
        )]

        for nome_marca in marcas:

            # é necessário verificar se já existe no banco
            id_existente = sessao.execute(
                text("SELECT idmarca FROM marca WHERE nomeMarca = :nome"),
                {"nome": nome_marca}
            ).scalar()

            # se a marca já existir, pula
            if id_existente:
                continue

            # se não existi, insere
            sessao.execute(
                text("INSERT INTO marca (nomeMarca) VALUES (:nome)"),
                {"nome": nome_marca}
            )

driver.quit()
