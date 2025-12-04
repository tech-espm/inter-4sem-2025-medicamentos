from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)

engine = create_engine(config.conexao_banco)

def pegar_valor_por_label(label):
    try:
        label_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//*[normalize-space(text())='{label}']"
            ))
        )
        valor_elem = label_elem.find_element(By.XPATH, "following-sibling::*[1]")
        return valor_elem.text.strip()
    except Exception:
        return None

def raspar_laboratorio():
    return pegar_valor_por_label("Fabricante")

def coletar_urls_pagina(pagina):
    driver.get(f"{config.urlbase}?p={pagina}")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)

    cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.product-item")
        )
    )

    print(f"Página {pagina} tem {len(cards)} produtos")

    urls = []

    for index, card in enumerate(cards, start=1):
        try:
            links = card.find_elements(By.TAG_NAME, "a")
            product_url = None
            
            for ln in links:
                href = ln.get_attribute("href")
                if not href:
                    continue

                if href.startswith(config.url_r) and href.endswith(".html"):
                    product_url = href
                    break

            if not product_url:
                print(f"Card {index}: nenhum link de produto encontrado")
                continue

            urls.append(product_url)
            print(f"Card {index}: URL coletada -> {product_url}")

        except Exception as e:
            print(f"Erro ao coletar link do card {index}: {e}")

    return urls

# ---------------------------------
# RASPAGEM PELO LINK
# ---------------------------------

todas_urls = []

for pagina in range(1, 9):
    urls_pagina = coletar_urls_pagina(pagina)
    todas_urls.extend(urls_pagina)

print(f"Total de URLs coletadas: {len(todas_urls)}")

with Session(engine) as sessao, sessao.begin():

    # 1) carregar laboratórios que JÁ existem no banco
    laboratorios_existentes = set()
    for (nome_lab,) in sessao.execute(text("SELECT nomeLaboratorio FROM laboratorio")):
        # se quiser ignorar maiúsculas/minúsculas:
        laboratorios_existentes.add(nome_lab.strip())

    print(f"Já existem {len(laboratorios_existentes)} laboratórios no banco.")

    # 2) loop de raspagem
    for i, url in enumerate(todas_urls, start=1):
        try:
            driver.get(url)
            print(f"\n[{i}/{len(todas_urls)}] Visitando: {url}")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "h1")
                )
            )

            laboratorio = raspar_laboratorio()
            if laboratorio:
                laboratorio = laboratorio.strip()
            print(f"Laboratório: {laboratorio}")

            if not laboratorio:
                print(" -> sem laboratório, pulando.")
                continue

            # verifica se já existe no set
            if laboratorio in laboratorios_existentes:
                print(" -> já existe no banco, não vou inserir.")
                continue

            # se não existe, insere e adiciona ao set
            sessao.execute(
                text("INSERT INTO laboratorio (nomeLaboratorio) VALUES (:v)"),
                {"v": laboratorio}
            )
            laboratorios_existentes.add(laboratorio)
            print(" -> laboratório inserido com sucesso.")

        except Exception as e:
            print(f"Erro ao processar {url}: {e}")
            continue

driver.quit()
