from pydantic import BaseModel

class Message(BaseModel):
    message: str


class DocumentoCreate(BaseModel):
    status: str
    checksum: str
    documento_id: str

class DocumentoEvento(DocumentoCreate):
    processo_id: str
