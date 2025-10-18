from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import and_
from app.db import session
from typing import List
# from prometheus_fastapi_instrumentator import Instrumentator

from app.model import ProcessoModel, DocumentoModel
from app.schema import DocumentoCreate,  DocumentoData, ProcessoCreate, ProcessoData, DocumentoProcesso
from app.util import separa_classe_numero


app = FastAPI(title='API SAPJu', description='Sistema de Análise de Processos Jurídicos')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/processo", status_code=status.HTTP_201_CREATED, tags=['Processo'])
async def create_processo(processo: ProcessoCreate):
    print(str(processo))
    processo = ProcessoModel(classe=processo.classe, numero=processo.numero, 
                             orgao_origem=processo.orgao_origem, 
                             processo_id=f"{processo.classe}{processo.numero}")
    session.add(processo)
    session.commit()
    return { "status": "processo cadastrado" }



@app.get("/api/processos/{processo_id}", tags=['Processo'])
def consulta_processo(processo_id: str):

    processo = session.query(ProcessoModel).filter(ProcessoModel.processo_id==processo_id).first()
    if not processo:
        raise HTTPException(status_code=404, detail=f"Processo não encontrado!")
    
    documentos = session.query(DocumentoModel).filter(DocumentoModel.processo_id==processo_id).all()

    schema_documentos = [ 
        DocumentoProcesso( documento_id=documento.documento_id, checksum=documento.checksum )
        for documento in documentos
    ]
    schema_processo = ProcessoData(
        classe = processo.classe,
        numero = processo.numero,
        orgao_origem = processo.orgao_origem,
        documentos = schema_documentos
    )
    
    return {"processo": schema_processo}




@app.get("/ping")
def ping_pong():
    return {"ping": "pong"}


#Instrumentator().instrument(app).expose(app) # prometheus