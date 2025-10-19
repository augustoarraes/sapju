import requests, json, os, dotenv
from app.schema import DocumentoEvento

dotenv.load_dotenv(".env")

url_publisher_msg = os.environ["URL_EVENTO_MSG"]
url_publisher_doc = os.environ["URL_EVENTO_DOC"]

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer SEU_TOKEN_QD_HOUVER"
}


# Envia para Publisher


def envia_mensagem_simples(msg: str):
    try:
        msg = {"message": msg}
        response = requests.post(url_publisher_msg, json=msg, headers=headers)
        if response.status_code == 200:
           print("Resposta:", response.json())
        else:
           print(f"Erro: Status Code {response.status_code}")
           print("Mensagem de erro:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")



def envia_documento(documento: DocumentoEvento):
    try:
        msg = documento.dict()
        response = requests.post(url_publisher_doc, json=msg, headers=headers)
        if response.status_code == 200:
           print("Resposta:", response.json())
        else:
           print(f"Erro: Status Code {response.status_code}")
           print("Mensagem de erro:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")
