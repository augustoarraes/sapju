from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import deferred
from sqlalchemy.dialects import postgresql
from app.db import Base
from datetime import datetime


class ProcessoModel(Base):
    __tablename__ = "processo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    classe = Column(String)
    numero = Column(Integer, default=0)
    processo_id = Column(String)
    orgao_origem = Column(String)
    data_abertura = Column(DateTime, default=datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f"))


class DocumentoModel(Base):
    __tablename__ = "documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, default=0)
    processo_id = Column(Integer, default=0)
    status = Column(String)
    checksum = Column(String)
    nome_documento = Column(String)
    texto = Column(String)
    data_criacao = Column(DateTime, default=datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f"))
    data_atualizacao = Column(DateTime, default=datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f"))
