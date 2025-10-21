from pydantic import BaseModel, ValidationError, Field
from typing import Optional
from datetime import datetime
from typing import List


class DocumentoCreate(BaseModel):
    status: str
    checksum: str
    documento_id: str

class DocumentoExtracao(BaseModel):
    status: str
    data_criacao: datetime
    data_atualizacao: datetime

class DocumentoProcesso(BaseModel):
    documento_id: str
    checksum: str

class DocumentoData(DocumentoProcesso):
    texto: str

class DocumentoEvento(DocumentoCreate):
    processo_id: str


class ProcessoCreate(BaseModel):
    classe: str
    numero: int
    orgao_origem: str

class ProcessoData(ProcessoCreate):
    documentos: List[DocumentoProcesso]

class ProcessoResponse(BaseModel):
    processo: ProcessoData
