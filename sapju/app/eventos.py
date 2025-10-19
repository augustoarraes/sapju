import requests, json, os, dotenv

dotenv.load_dotenv(".env")

url_publisher = os.environ["URL_EVENTO"]

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer SEU_TOKEN_QD_HOUVER"
}


def envia_mensagem_simples(msg: str):
    try:
        msg = {"message": msg}
        response = requests.post(url_publisher, json=msg, headers=headers)
        if response.status_code == 200:
           print("Resposta:", response.json())
        else:
           print(f"Erro: Status Code {response.status_code}")
           print("Mensagem de erro:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")