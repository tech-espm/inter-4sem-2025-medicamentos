from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import time
import config

# -------------------------------------------------
# CONFIGURAÇÕES
# -------------------------------------------------

driver = webdriver.Chrome()
driver.set_page_load_timeout(300)
wait = WebDriverWait(driver, 10)

engine = create_engine(config.conexao_banco)

# -------------------------------------------------
# NORMALIZAÇÃO
# -------------------------------------------------

def normalizar(txt):
    if not txt:
        return None
    txt = unicodedata.normalize("NFKD", str(txt))
    txt = txt.encode("ASCII", "ignore").decode("ASCII")
    return txt.strip().title()

# -------------------------------------------------
# RASPAGEM
# -------------------------------------------------

def raspar_nome_medicamento():
    try:
        return wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text.strip()
    except:
        return None


def raspar_preco():
    try:
        elems = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//span[contains(@class, 'price-pdp-content')]")
            )
        )
        for elem in elems:
            texto = elem.text.strip()
            if texto:
                texto = texto.replace("R$", "").replace(".", "").replace(",", ".")
                return float(texto)
        return None
    except:
        return None


def raspar_marca():
    try:
        return wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(normalize-space(), 'Marca')]//a")
            )
        ).text.strip()
    except:
        return None


def raspar_quantidade():
    try:
        elem = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(normalize-space(), 'Quantidade')]")
            )
        )
        return elem.text.replace("Quantidade", "").strip()
    except:
        return "1"


def raspar_dosagem():
    try:
        return wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[normalize-space()='Dosagem']/following-sibling::span[1]")
            )
        ).text.strip()
    except:
        return "N/A"


def raspar_substancia():
    try:
        return wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(normalize-space(), 'Princípio Ativo')]//a")
            )
        ).text.strip()
    except:
        try:
            elem = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//p[contains(normalize-space(), 'Princípio Ativo')]")
                )
            )
            return elem.text.replace("Princípio Ativo", "").replace(":", "").strip()
        except:
            return None

# -------------------------------------------------
# COLETA DE URLs
# -------------------------------------------------

def coletar_urls_pagina(pagina):
    driver.get(f"{config.urlbase}?p={pagina}")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    cards = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-item"))
    )

    urls = []
    for card in cards:
        links = card.find_elements(By.TAG_NAME, "a")
        for ln in links:
            href = ln.get_attribute("href")
            if href and href.startswith(config.url_r) and href.endswith(".html"):
                urls.append(href)
                break
    return urls

# -------------------------------------------------
# BANCO — BUSCAS
# -------------------------------------------------

def buscar_id_marca(sessao, nome):
    nome = normalizar(nome)
    row = sessao.execute(
        text("SELECT idmarca FROM marca WHERE nomeMarca = :n"),
        {"n": nome}
    ).fetchone()
    return row[0] if row else None


def buscar_id_substancia(sessao, nome):
    nome = normalizar(nome)
    row = sessao.execute(
        text("SELECT idsubstancia FROM substancia WHERE nomeSubstancia = :n"),
        {"n": nome}
    ).fetchone()
    return row[0] if row else None


def medicamento_ja_existe(sessao, link):
    row = sessao.execute(
        text("SELECT idmedicamento FROM medicamento WHERE link = :l"),
        {"l": link}
    ).fetchone()
    return row is not None


def relacionar_medicamento_substancia(sessao, id_medicamento, id_substancia):
    existe = sessao.execute(
        text("""
            SELECT 1
            FROM substancia_has_medicamento
            WHERE idmedicamento = :m AND idsubstancia = :s
        """),
        {"m": id_medicamento, "s": id_substancia}
    ).fetchone()

    if not existe:
        sessao.execute(
            text("""
                INSERT INTO substancia_has_medicamento
                    (idmedicamento, idsubstancia)
                VALUES
                    (:m, :s)
            """),
            {"m": id_medicamento, "s": id_substancia}
        )

# -------------------------------------------------
# FLUXO PRINCIPAL
# -------------------------------------------------

try:
    todas_urls = []
    for pagina in range(1, 9):
        todas_urls.extend(coletar_urls_pagina(pagina))

    print(f"Total de URLs coletadas: {len(todas_urls)}")

    with Session(engine) as sessao, sessao.begin():
        for i, url in enumerate(todas_urls, start=1):
            print(f"\n[{i}/{len(todas_urls)}] {url}")
            driver.get(url)
            time.sleep(2)

            nome = raspar_nome_medicamento()
            preco = raspar_preco() or 0.0
            marca = raspar_marca()
            quantidade = raspar_quantidade()
            dosagem = raspar_dosagem()
            substancia = raspar_substancia()

            if medicamento_ja_existe(sessao, url):
                print(" -> já existe, pulando")
                continue

            id_marca = buscar_id_marca(sessao, marca)
            if not id_marca:
                print(" -> marca não encontrada, pulando")
                continue

            id_substancia = buscar_id_substancia(sessao, substancia)
            if not id_substancia:
                print(" -> substância não encontrada no banco, pulando")
                continue

            res = sessao.execute(
                text("""
                    INSERT INTO medicamento
                        (nomeMedicamento, dosagem, link, preco, idmarca, quantidade)
                    VALUES
                        (:n, :d, :l, :p, :m, :q)
                """),
                {
                    "n": nome,
                    "d": dosagem,
                    "l": url,
                    "p": preco,
                    "m": id_marca,
                    "q": quantidade
                }
            )

            id_medicamento = res.lastrowid

            relacionar_medicamento_substancia(
                sessao, id_medicamento, id_substancia
            )

            print(" -> medicamento inserido com sucesso")

finally:
    driver.quit()
    print("\nDriver encerrado.")