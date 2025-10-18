from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import session
from typing import List
# from prometheus_fastapi_instrumentator import Instrumentator

from app.model import ProcessoModel, DocumentoModel
from app.schema import DocumentoCreate,  DocumentoData, ProcessoCreate, ProcessoData


app = FastAPI(title='API SAPJu', description='Sistema de Análise de Processos Jurídicos')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/ping")
def ping_pong():
    return {"ping": "pong"}


#Instrumentator().instrument(app).expose(app) # prometheus