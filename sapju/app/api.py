from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import session
from typing import List
# from prometheus_fastapi_instrumentator import Instrumentator

# from app.model import ProdutoModel
# from app.schema import ProdutoData, ProdutoCreate, ProdutoUpdate, Produtos


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