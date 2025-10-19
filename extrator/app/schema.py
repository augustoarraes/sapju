from pydantic import BaseModel, ValidationError, Field
from typing import Optional
from datetime import datetime
from typing import List


class DocumentoCreate(BaseModel):
    status: str
    checksum: str
    documento_id: str

class DocumentoEvento(DocumentoCreate):
    processo_id: str
