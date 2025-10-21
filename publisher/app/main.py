from fastapi import FastAPI, HTTPException
import asyncio, aio_pika, json, dotenv, os
from app.schema import Message, DocumentoEvento


app = FastAPI(title="Publisher Evento do RabbitMQ")

dotenv.load_dotenv(".env")

rabbit_host=os.environ["RABBITMQ_HOST"]
rabbit_port=int(os.environ["RABBITMQ_PORT"])
rabbit_queue=os.environ["RABBITMQ_QUEUE"]


async def conecta_rabbit():
    app.state.connection = await aio_pika.connect_robust(host=rabbit_host, port=rabbit_port, heartbeat=30, timeout=10)
    app.state.channel = await app.state.connection.channel()

@app.on_event("startup")
async def startup_event():
    try:
        await conecta_rabbit()
        await app.state.channel.declare_queue(rabbit_queue) # , durable=True 
        print("Conectou com RabbitMQ")
    except Exception as e:
        print(f"Erro de conexão com RabbitMQ: {e}")

@app.post("/evento/documento")
async def envia_doc_rabbitmq(documento: DocumentoEvento):
    try:
        if not app.state.connection or app.state.connection.is_closed:
            await conecta_rabbit()
        await app.state.channel.default_exchange.publish(
            aio_pika.Message( body = json.dumps( documento.dict() ).encode("utf-8") ),
            routing_key = rabbit_queue
        )
        print(f"{documento.dict()} passou por aqui ... publicado no RabbitMQ")
        return {"status": "Documento enviado", "Documento": documento.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message to RabbitMQ: {e}")

# @app.post("/evento/enviamensagem")
# async def envia_msg_rabbitmq(message: Message):
#     if not hasattr(app.state, 'rabbitmq_channel') or not app.state.rabbitmq_channel.is_open:
#         raise HTTPException(status_code=500, detail="RabbitMQ connection not established.")
#     try:
#         app.state.rabbitmq_channel.basic_publish(
#             exchange='',
#             routing_key=rabbit_queue,
#             body=json.dumps({"message": message.message})
#         )
#         return {"status": "Message sent", "message": message.message}
#     except pika.exceptions.AMQPError as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send message to RabbitMQ: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    try:
        if app.state.channel and not app.state.channel.is_closed:
            await app.state.channel.close()
        if app.state.connection and not app.state.connection.is_closed:
            await app.state.connection.close()
        print("Fechando conexão com RabbitMQ")
    except Exception as e:
        print(f"Erro ao fechar conexão: {e}")

@app.get("/ping")
def ping_pong():
    return {"ping": "pong", 
            "queue": rabbit_queue}
