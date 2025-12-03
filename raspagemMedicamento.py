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
wait = WebDriverWait(driver, 10)

engine = create_engine(config.conexao_banco)

def raspar_nome_medicamento():
    """Pega o texto do <h1> (nome do produto)."""
    try:
        elem = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        return elem.text.strip()
    except Exception as e:
        print("Erro ao raspar nome do medicamento:", e)
        return None

def raspar_preco():
    """
    Lê o preço em qualquer <span> com classe 'price-pdp-content'
    e retorna float. Se não encontrar texto, retorna None.
    """
    try:
        elems = wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//span[contains(@class, 'price-pdp-content')]"
            ))
        )

        for elem in elems:
            texto = elem.text.strip()
            if not texto:
                continue  # pula spans vazios

            print("DEBUG PREÇO BRUTO:", repr(texto))

            texto = (
                texto.replace("R$", "")
                     .replace("\xa0", " ")
                     .strip()
            )
            texto = (
                texto.replace(".", "")
                     .replace(",", ".")
                     .strip()
            )

            return float(texto)

        # se chegou aqui, nenhum span tinha texto
        print("DEBUG PREÇO: nenhum span com texto de preço encontrado.")
        return None

    except Exception as e:
        print("Erro ao raspar preço:", e)
        return None




def raspar_marca_nome():
    """Pega o nome da marca na linha 'Marca <a>Allegra</a>'."""
    try:
        elem = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(normalize-space(), 'Marca')]//a"
            ))
        )
        return elem.text.strip()
    except Exception as e:
        print("Erro ao raspar marca:", e)
        return None


def raspar_quantidade():
    """Pega a quantidade na linha 'Quantidade 60ml'."""
    try:
        elem = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(normalize-space(), 'Quantidade')]"
            ))
        )
        texto = elem.text.strip()
        # remove o label
        return texto.replace("Quantidade", "").strip()
    except Exception as e:
        print("Erro ao raspar quantidade:", e)
        return "1"   # fallback para não quebrar


def raspar_dosagem():
    """
    Pega a dosagem no bloco:
    <span>Dosagem</span>
    <span>100MG</span>
    Retorna '100MG'.
    """
    try:
        elem = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[normalize-space()='Dosagem']/following-sibling::span[1]"
            ))
        )
        texto = elem.text.strip()
        print("DEBUG DOSAGEM:", repr(texto))
        return texto
    except Exception as e:
        print("Erro ao raspar dosagem:", e)
        return None



def raspar_substancia():
    """
    Pega o princípio ativo.
    Primeiro tenta na linha 'Princípio Ativo <a>Fexofenadina</a>'.
    Se não achar, tenta pegar o texto bruto.
    """
    try:
        elem = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(normalize-space(), 'Princípio Ativo')]//a"
            ))
        )
        return elem.text.strip()
    except Exception:
        try:
            elem = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//p[contains(normalize-space(), 'Princípio Ativo')]"
                ))
            )
            texto = elem.text.strip()
            return (texto
                    .replace("Princípio Ativo", "")
                    .replace(":", "")
                    .strip())
        except Exception as e:
            print("Erro ao raspar substância:", e)
            return "N/A"


# -------------------------------------------
# COLETA DAS URLs A PARTIR DA LISTAGEM
# -------------------------------------------

def coletar_urls_pagina(pagina: int):
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
# FUNÇÕES DE BANCO PARA MARCA E MEDICAMENTO
# -------------------------------------------

def buscar_id_marca(sessao: Session, nome_marca: str):
    """Busca o idmarca na tabela marca pelo nome."""
    if not nome_marca:
        return None

    row = sessao.execute(
        text("SELECT idmarca FROM marca WHERE nomeMarca = :n"),
        {"n": nome_marca}
    ).fetchone()

    if row:
        return row[0]

    print(f"⚠ Marca '{nome_marca}' não encontrada na tabela marca.")
    return None


def medicamento_ja_existe(sessao: Session, link: str):
    """Evita inserir o mesmo produto duas vezes (usando o link)."""
    row = sessao.execute(
        text("SELECT idMedicamentos FROM medicamentos WHERE link = :l"),
        {"l": link}
    ).fetchone()
    return row is not None


# -------------------------------------------
# FLUXO PRINCIPAL
# -------------------------------------------

try:
    # 1) Coletar todas as URLs de produto
    todas_urls = []
    for pagina in range(1, 9):   # ajuste o range se tiver mais/menos páginas
        urls_pagina = coletar_urls_pagina(pagina)
        todas_urls.extend(urls_pagina)

    print(f"\nTotal de URLs coletadas: {len(todas_urls)}\n")

    # 2) Entrar em cada URL e montar o registro de medicamentos
    with Session(engine) as sessao, sessao.begin():
        for i, url in enumerate(todas_urls, start=1):
            try:
                print(f"\n[{i}/{len(todas_urls)}] Visitando: {url}")
                driver.get(url)

                # garante que a página carregou (título)
                wait.until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "h1")
                    )
                )

                nome = raspar_nome_medicamento()
                preco = raspar_preco()
                nome_marca = raspar_marca_nome()
                quantidade = raspar_quantidade()
                dosagem = raspar_dosagem()
                substancia = raspar_substancia()

                print(f" -> Nome: {nome}")
                print(f" -> Marca: {nome_marca}")
                print(f" -> Preço: {preco}")
                print(f" -> Quantidade: {quantidade}")
                print(f" -> Dosagem: {dosagem}")
                print(f" -> Substância: {substancia}")

                if medicamento_ja_existe(sessao, url):
                    print(" -> já existe no banco (mesmo link), pulando.")
                    continue

                id_marca = buscar_id_marca(sessao, nome_marca)
                if not id_marca:
                    print(" -> sem id de marca, pulando.")
                    continue

                # fallbacks para não quebrar NOT NULL
                if preco is None:
                    preco = 0.0
                if not dosagem:
                    dosagem = "N/A"
                if not quantidade:
                    quantidade = "1"
                if not substancia:
                    substancia = "N/A"

                sessao.execute(
                    text("""
                        INSERT INTO medicamentos
                            (nomeMedicamento, dosagem, link, preco, substancia, marca, quantidade)
                        VALUES
                            (:nome, :dosagem, :link, :preco, :substancia, :marca, :quantidade)
                    """),
                    {
                        "nome": nome,
                        "dosagem": dosagem,
                        "link": url,
                        "preco": preco,
                        "substancia": substancia,
                        "marca": id_marca,
                        "quantidade": quantidade
                    }
                )

                print(" -> medicamento inserido com sucesso!")

            except Exception as e:
                print(f"Erro ao processar {url}: {e}")
                continue

finally:
    driver.quit()
    print("\nDriver encerrado.")
