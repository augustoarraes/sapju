from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.db import session
from typing import List
# from prometheus_fastapi_instrumentator import Instrumentator
from app.extracao import ExtracaoDocumento
from app.model import DocumentoModel
from app.schema import DocumentoEvento
import dotenv, os, pika, threading, json


app = FastAPI(title='Extrator SAPJu', description='Consumer do RabbitMQ & Extrator de Documentos SAPJu')
dotenv.load_dotenv(".env")

rabbit_host=os.environ["RABBITMQ_HOST"]
rabbit_port=os.environ["RABBITMQ_PORT"]
rabbit_queue=os.environ["RABBITMQ_QUEUE"]


# /api/eventos/status


def callback(ch, method, properties, body):
    try:
        msg = json.loads(body)
        print(f"Payload recebido: {msg}")
        # .. chamar o extrator de texto aqui
        extracao = ExtracaoDocumento( DocumentoEvento(**msg) )
        extracao.extracao_documento()
    except Exception as e:
        print(f"Erro no processamento da mensagem: {e}")


def inicia_consumidor():
    conn = pika.BlockingConnection( pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, heartbeat=120, blocked_connection_timeout=360) )
    canal = conn.channel()
    canal.queue_declare( queue=rabbit_queue )
    print(f"Conectando ao RabbitMQ ...")
    canal.basic_consume( queue=rabbit_queue, on_message_callback=callback, auto_ack=True )
    canal.start_consuming()


@app.on_event("startup")
async def inicia_evento():
    thread = threading.Thread( target=inicia_consumidor, daemon=True )
    thread.start()
    print(f"Inicia evento consumidor ...")


@app.get("/ping")
def ping_pong():
    return {"ping": "pong"}


#Instrumentator().instrument(app).expose(app) # prometheus
