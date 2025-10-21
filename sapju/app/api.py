from fastapi import FastAPI, status, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
#from sqlalchemy import and_
from app.db import session
from typing import List
# from prometheus_fastapi_instrumentator import Instrumentator

from app.model import ProcessoModel, DocumentoModel
from app.schema import DocumentoEvento,  DocumentoData, ProcessoCreate, ProcessoData, DocumentoProcesso, DocumentoExtracao
from app.eventos import envia_mensagem_simples, envia_documento
from simple_file_checksum import get_checksum
import dotenv, os, uuid, threading


app = FastAPI(title='API SAPJu', description='Sistema de Análise de Processos Jurídicos')
dotenv.load_dotenv(".env")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/processos", status_code=status.HTTP_201_CREATED, tags=['Processo'])
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



@app.post("/api/processos/{processo_id}/documentos", tags=['Documento'])
async def upload_documento(processo_id: str, arquivos: List[UploadFile] = File(...)):
    dir_uploads = os.environ["DIR_UPLOAD"]
    algo = os.environ["ALGO_CHECKSUM"]
    documentos = []

    for arquivo in arquivos:
        uuid_documento = str(uuid.uuid1() )
        nome_documento = f"{uuid_documento}__{arquivo.filename}"
        with open(f"{dir_uploads}/{nome_documento}", "wb") as escrever:
            escrever.write( await arquivo.read() )
            checksum = str( get_checksum(f"{dir_uploads}/{nome_documento}", algorithm=algo) )
        documento = DocumentoModel(processo_id=processo_id, status="NAO_INICIADA", 
                                   documento_id=uuid_documento, checksum=checksum,
                                   nome_documento=nome_documento)
        session.add(documento)
        session.commit()
        aux = {
            "status": documento.status,
            "checksum": documento.checksum,
            "documento_id": documento.documento_id
        }
        documentos.append(aux)
        aux["processo_id"] = processo_id
        documento_evento = DocumentoEvento(**aux)
        thread = threading.Thread( target=envia_documento( documento_evento ), daemon=True )
        thread.start()

    return documentos


@app.get("/api/processos/{processo_id}/documentos/{documento_id}", response_model=DocumentoData, tags=['Documento'])
async def consulta_documento(processo_id: str, documento_id: str):
    try:
        documento = session.query(DocumentoModel).filter(DocumentoModel.processo_id==processo_id, DocumentoModel.documento_id==documento_id).first()
        if not documento:
            raise HTTPException(status_code=404, detail=f"Documento não encontrado!")
        return documento
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=f"Erro: {e}")
    finally:
        session.close()


@app.get("/api/processos/{processo_id}/documentos/{documento_id}/status", response_model=DocumentoExtracao, tags=['Extração'])
async def consulta_documento(processo_id: str, documento_id: str):
    try:
        documento = session.query(DocumentoModel).filter(DocumentoModel.processo_id==processo_id, DocumentoModel.documento_id==documento_id).first()
        if not documento:
            raise HTTPException(status_code=404, detail=f"Documento não encontrado!")
        return documento
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=f"Erro: {e}")
    finally:
        session.close()
    


@app.get("/ping")
def ping_pong():
    envia_mensagem_simples("enviando msg test")
    return {"ping": "pong"}


#Instrumentator().instrument(app).expose(app) # prometheus
