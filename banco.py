from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config import conexao_banco
import logging
import re

logger = logging.getLogger(__name__)

engine = create_engine(conexao_banco)
  