from fastapi import FastAPI, HTTPException
import pika, json, dotenv, os
from app.schema import Message, DocumentoEvento

app = FastAPI(title="Publisher Evento do RabbitMQ")

dotenv.load_dotenv(".env")

rabbit_host=os.environ["RABBITMQ_HOST"]
rabbit_port=os.environ["RABBITMQ_PORT"]
rabbit_queue=os.environ["RABBITMQ_QUEUE"]


@app.on_event("startup")
async def startup_event():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host, port=rabbit_port, heartbeat=120, blocked_connection_timeout=600)
        )
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_queue)
        app.state.rabbitmq_connection = connection
        app.state.rabbitmq_channel = channel
        print("Conectou com RabbitMQ")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Erro de conexão com RabbitMQ: {e}")


@app.post("/evento/documento")
async def envia_doc_rabbitmq(documento: DocumentoEvento):
    if not hasattr(app.state, 'rabbitmq_channel') or not app.state.rabbitmq_channel.is_open:
        raise HTTPException(status_code=500, detail="RabbitMQ connection not established.")
    try:
        app.state.rabbitmq_channel.basic_publish(
            exchange='',
            routing_key=rabbit_queue,
            body=json.dumps(documento.dict())
        )
        return {"status": "Documento enviado", "Documento": documento.dict()}
    except pika.exceptions.AMQPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message to RabbitMQ: {e}")


@app.post("/evento/enviamensagem")
async def envia_msg_rabbitmq(message: Message):
    if not hasattr(app.state, 'rabbitmq_channel') or not app.state.rabbitmq_channel.is_open:
        raise HTTPException(status_code=500, detail="RabbitMQ connection not established.")
    try:
        app.state.rabbitmq_channel.basic_publish(
            exchange='',
            routing_key=rabbit_queue,
            body=json.dumps({"message": message.message})
        )
        return {"status": "Message sent", "message": message.message}
    except pika.exceptions.AMQPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message to RabbitMQ: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, 'rabbitmq_connection') and app.state.rabbitmq_connection.is_open:
        app.state.rabbitmq_connection.close()
        print("Fechando conexão com RabbitMQ")


@app.get("/ping")
def ping_pong():
    return {"ping": "pong"}
