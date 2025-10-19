from fastapi import FastAPI, status, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
#from sqlalchemy import and_
from app.db import session
from typing import List
# from prometheus_fastapi_instrumentator import Instrumentator

from app.model import DocumentoModel
from app.schema import DocumentoData, DocumentoProcesso
import dotenv, os, uuid


app = FastAPI(title='API SAPJu', description='Sistema de Análise de Processos Jurídicos')
dotenv.load_dotenv(".env")
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