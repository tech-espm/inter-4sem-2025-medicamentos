from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config

# -------------------------------------------
# CONFIGURAÇÕES
# -------------------------------------------

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)

engine = create_engine(config.conexao_banco)
wait = WebDriverWait(driver, 10)


# -------------------------------------------
# RASPAGEM: MARCA E LABORATÓRIO
# -------------------------------------------

def raspar_marca():
    try:
        elem = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(normalize-space(), 'Marca')]/b/a"
            ))
        )
        return elem.text.strip()
    except Exception as e:
        print("Erro ao raspar marca:", e)
        return None

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

    cards = wait.until(
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


# -------------------------------------------
# FUNÇÕES DE BANCO
# -------------------------------------------

def buscar_id_laboratorio(sessao: Session, nome_lab: str):
    """
    Busca o idlaboratorio na tabela laboratorio pelo nome.
    NÃO insere laboratório novo, só faz SELECT.
    """
    if not nome_lab:
        return None

    row = sessao.execute(
        text("SELECT idlaboratorio FROM laboratorio WHERE nomeLaboratorio = :n"),
        {"n": nome_lab}
    ).fetchone()

    if row:
        return row[0]

    print(f"⚠ Laboratório '{nome_lab}' não encontrado no banco.")
    return None


def marca_ja_existe(sessao: Session, nome_marca: str, id_lab: int):
    """
    Verifica se já existe essa combinação de marca + laboratório.
    """
    row = sessao.execute(
        text("""
            SELECT 1
            FROM marca
            WHERE nomeMarca = :m AND idlaboratorio = :lab
        """),
        {"m": nome_marca, "lab": id_lab}
    ).fetchone()

    return row is not None


# -------------------------------------------
# FLUXO PRINCIPAL
# -------------------------------------------

todas_urls = []

for pagina in range(1, 9):
    urls_pagina = coletar_urls_pagina(pagina)
    todas_urls.extend(urls_pagina)

print(f"\nTotal de URLs coletadas: {len(todas_urls)}\n")

try:
    with Session(engine) as sessao, sessao.begin():
        for i, url in enumerate(todas_urls, start=1):
            try:
                print(f"\n[{i}/{len(todas_urls)}] Visitando: {url}")
                driver.get(url)

                # espera página carregar
                wait.until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "h1")
                    )
                )

                nome_marca = raspar_marca()
                nome_lab = raspar_laboratorio()

                print(f" -> Marca: {nome_marca} | Laboratório: {nome_lab}")

                if not nome_marca or not nome_lab:
                    print(" -> pulando: faltou marca ou laboratório")
                    continue

                id_lab = buscar_id_laboratorio(sessao, nome_lab)
                if not id_lab:
                    print(" -> pulando: laboratório não cadastrado no banco")
                    continue

                if marca_ja_existe(sessao, nome_marca, id_lab):
                    print(" -> marca já cadastrada para esse laboratório, pulando")
                    continue

                sessao.execute(
                    text("""
                        INSERT INTO marca (nomeMarca, idlaboratorio)
                        VALUES (:nome, :lab)
                    """),
                    {"nome": nome_marca, "lab": id_lab}
                )

                print(" -> marca inserida com sucesso!")

            except Exception as e:
                print(f"Erro ao processar {url}: {e}")
                continue

finally:
    driver.quit()
    print("\nDriver encerrado.")
