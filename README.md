# SAPJu

SAPJu defini com as iniciais de *`Sistema de Análise de Processos Jurídicos`* + `u` minusculo. 

Melhor [referência](desafio-python-developer.md) do Sistema. O Sistema distribuído foi desenvolvido com o frame do Python FastAPI, com Docker, Banco de Dados Postgres e eventos com RabbitMQ. São três microsserviços FastAPI:
- API: App Backend de Processo e Documentos
- Publisher: Responsável inserir na fila de eventos do RabbitMQ
- Extrator: Responsável por consumir a fila de eventos do RabbitMQ e Realizar a Extração dos Textos dos Documentos (cadastrados na API).


## Subindo o Sistema

```bash
docker compose up -d

# .. caso o backend não suba de imediato:
docker restart sapju_api
# .. caso queira verificar o log de execução do backend
docker logs -f sapju_api
```

Swagger da API: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)

Admin Web de Eventos (RabbitMQ): [http://127.0.0.1:15672](http://127.0.0.1:15672/docs) (guest/guest)

Swagger do Publisher de Documentos: [http://127.0.0.1:5673/docs](http://127.0.0.1:5673/docs)

Swagger do Extrator de Documentos: [http://127.0.0.1:5674/docs](http://127.0.0.1:5674/docs)

Quando o deploy da App concluir, a pasta `uploads` será criada. Uma diretorio importante para o fluxo da aplicação.

E, as configurações e credenciais do sistema estão em `/sapju/app/.env` e em `compose.yml`.


## Utilizando a API

### Cadastrando o Processo
Endpoint: 
~~~bash
http://localhost:5000/api/processo
~~~
Body:
``` json
{
  "classe": "ARE",
  "numero": 123456,
  "orgao_origem": "STF"
}
```

### Upload de Documento(s)
Enpoint:
~~~bash
http://localhost:5000/api/processos/{processo_id}/documentos
~~~
Em Body, escolher `form-data`, criar a `Key` *`arquivos`* e o tipo dessa `Key` é *`File`*. Em `Value`, selecione o Documento para upload.

### Consultando o Processo
Endpoint: 
~~~bash
http://localhost:5000/api/processos/{processo_id}
~~~

### Consultando um Documento
Endpoint: 
~~~bash
http://localhost:5000/api/processos/{processo_id}/documentos/{documento_id}/status
~~~


## Extrator
Endpoint de acompanhamento da atividade do Extrator:
~~~bash
http://localhost:3000/api/eventos/status
~~~

## Arquitetura da Aplicação



## Melhorias e Futuras Features



## Contato

Augusto Arraes
[(85) 99991 6898](https://wa.me/5585999916898)