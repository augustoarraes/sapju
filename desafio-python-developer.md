# Desafio Python Developer

Orientações Gerais

- Crie um repositório no Github
- Compartilhe com o recrutador o link do seu repositório.

## Desafio

### Objetivo

Desenvolver um sistema de análise de processos jurídicos.

### Descrição

Crie um serviço com:

- API REST e Swagger com qualquer framework Python **async** que possibilite:
  - cadastro de um processo;
  - upload de arquivos PDF apenas para processos previamente cadastrados;
  - consulta de:
    - dados cadastrais do processo;
    - texto do PDF;
    - status da tarefa de extração do texto;
- Serviço em background ou worker para consumo de eventos de uma fila do RabbitMQ;
- O consumo de eventos da fila do serviço de mensageria deverá extrair e armazenar o texto dos arquivos PDF.
  - Todos os arquivos compartilhados no desafio possuem camada textual, desta forma pode-se utilizar a lib Python `pdftotext`, diponível em: https://pypi.org/project/pdftotext/
- status da tarefa de extração do texto:
  - CONCLUIDA: a tarefa de extração do texto foi concluída com sucesso;
  - EM_EXECUCAO: a tarefa de extração do texto está em execução;
  - NAO_INICIADA: a tarefa de extração do texto não foi iniciada;
  - FALHA_NO_PROCESSAMENTO: a tarefa de extração do texto falhou no processamento.
- A escolha da infraestrutura de armazenamento de dados e dos documentos é livre.

> IMPORTANTE: não é necessário construir nenhum tipo de frontend, serviço de autenticação ou segurança.

## API

### Dados para cadastro do processo:

Requisição:

- Endpoint: `/api/processos`
- Dados do processo:
  - Classe: `ARE`, `RE` ou `AI`;
  - Número: número inteiro >= 1;
  - Origem: sigla de qualquer Tribunal Superior do Brasil, por exemplo: STF, STJ entre outros.

``` json
{
  "classe": "ARE",
  "numero": 123456,
  "orgao_origem": "STF"
}
```

Resposta:

``` json
{
  "status": "processo cadastrado"
}
```

### Upload de documento

Requisição:

- Endpoint: `/api/processos/{processo_id}/documentos`

Resposta:

``` json
{
  "status": "documento cadastrado",
  "checksum": "sha256 do documento",
  "documento_id": "identificador único do documento"
}
```

### Consulta de dados do processo

Requisição:

- Endpoint: `/api/processos/{processo_id}`
- `processo_id`: classe + número do processo, por exemplo: `ARE123456`

Resposta:

``` json
{
  "processo": {
    "classe": "ARE",
    "numero": 123456,
    "orgao_origem": "STF"
    "documentos": [
      {
        "id": "identificador único do documento",
        "checksum": "sha256 do documento",
      }
    ]
  }
}
```

### Consulta de documento

Requisição:

- Endpoint: `/api/processos/{processo_id}/documentos/{documento_id}`
- `processo_id`: classe + número do processo, por exemplo: `ARE123456`
- `documento_id`: identificador único do documento

Resposta:

``` json
{
  "id": "identificador único do documento",
  "checksum": "sha256 do documento",
  "texto": "texto do documento"
}
```

### Status da tarefa de extração do texto

Requisição:

- Endpoint: `/api/processos/{processo_id}/documentos/{documento_id}/status`
- `processo_id`: classe + número do processo, por exemplo: `ARE123456`
- `documento_id`: identificador único do documento

Resposta:

``` json
{
  "status": "tarefa de extração do texto",
  "data_criacao": "data de criação da primeira tarefa",
  "data_atualizacao": "data de atualização da tarefa"
}
```

## O que iremos avaliar

- Decisões arquitetura da solução e seus trade-offs;
- Funcionamento da aplicação;
- Documentação;
- Testes, como você lida com edge cases e cobertura de testes;
- Uso do git;
- Organização e estrutura do código de acordo com boas práticas;

## Diferenciais

- Uso de Docker;
- Integração contínua (CI).

## Prazo

O prazo de conclusão do desafio é de 7 dias.

> NOTA: entendemos que o desafio é ligeiramente extenso e não esperamos uma solução production ready completa. Documente seus trade-offs e o que você priorizaria em uma próxima iteração. Valorizamos um código bem pensado.