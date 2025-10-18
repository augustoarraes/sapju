# SAPJu

SAPJu é um Sistema de Análise de Processos Jurídicos. Melhor [referência](desafio-python-developer.md) do Sistema.


## Subindo o Sistema

```bash
docker compose up -d

# .. caso o backend não suba de imediato:
docker restart sapju_api
# .. caso queira verificar o log de execução do backend
docker logs -f sapju_api
```

As configurações e credenciais do sistema estão no `/sapju/app/.env` e no `compose.yml`.

Swagger da API: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)


## Utilizando a API



## Arquitetura da Aplicação



## Melhorias



## Contato

Augusto Arraes
[(85) 99991 6898](https://wa.me/5585999916898)