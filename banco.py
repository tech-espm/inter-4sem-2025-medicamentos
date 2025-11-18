from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config import conexao_banco
import logging
import re

logger = logging.getLogger(__name__)

engine = create_engine(conexao_banco)
  
def executar_query(query, parametros=None):
    try:
        with Session(engine) as session:
            resultado = session.execute(text(query), parametros)
            session.commit()
            return resultado
    except SQLAlchemyError as e:
        logger.error(f"Erro ao executar a query: {e}")
        raise

def inserir_usuario(nome, email, senha):
    query = """
    INSERT INTO usuarios (nome, email, senha) 
    VALUES (:nome, :email, :senha)
    """
    parametros = {'nome': nome, 'email': email, 'senha': senha}
    try:
        executar_query(query, parametros)
        logger.info(f"Usuário {email} inserido com sucesso.")
    except IntegrityError:
        logger.warning(f"Falha ao inserir usuário: email {email} já existe.")
        raise ValueError("Email já cadastrado.")
    except SQLAlchemyError as e:
        logger.error(f"Erro ao inserir usuário: {e}")
        raise

def buscar_usuario_por_email(email):
    query = "SELECT * FROM usuarios WHERE email = :email"
    parametros = {'email': email}
    try:
        resultado = executar_query(query, parametros)
        usuario = resultado.fetchone()
        return usuario
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário por email: {e}")
        raise