# Desafio Python Moniari

## Descrição

Este projeto foi desenvolvido para avaliar suas habilidades com tecnologias de back-end, focando em Python, APIs REST, e arquitetura de serviços desacoplados.

## Tarefa

O desafio consiste em criar uma API simples utilizando Python (**FastAPI**), que permita aos usuários consultar cotações de ações.
O projeto é dividido em dois serviços distintos:

- Uma API voltada para o usuário final, que processa solicitações de usuários registrados em busca de informações sobre cotações de ações.
- Um serviço interno agregador de cotações, responsável por consultar APIs externas para buscar as cotações solicitadas pelos usuários.

## Requisitos Mínimos

### Serviço de API

- Os endpoints deste serviço devem exigir **autenticação**, não permitindo solicitações anônimas. Cada solicitação deve ser autenticada utilizando Basic Authentication (exemplo: `Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==` onde o token é a conversão em Base64 de username:senha).

- Ao receber uma solicitação de cotação de ação (através do endpoint dedicado no serviço de API), se a ação for encontrada, o serviço deve registrar no console o usuário requisitante e a ação solicitada.

- A resposta do serviço de API deve seguir o formato: `GET /stock?q=aapl.us`

```python
{
  "simbolo": "AAPL.US",
  "nome_da_empresa": "APPLE",
  "cotacao": 123
}
```

O valor da cotação deve ser extraído do campo `close` retornado pelo serviço de cotações.

- Todas as respostas dos endpoints devem ser em formato JSON.

### Serviço de Cotações

- Considerando que este serviço é interno, solicitações para seus endpoints não requerem autenticação.
- Ao receber uma solicitação de cotação, este serviço deve consultar uma API externa para obter as informações necessárias. Para este desafio, utilize a seguinte API: `https://stooq.com/q/l/?s={codigo_da_acao}&f=sd2t2ohlcvn&h&e=csv`.
- O `{codigo_da_acao}` deve ser substituído pelo código da ação desejada pelo usuário.
- Uma lista de códigos de ações disponíveis pode ser encontrada em: https://stooq.com/t/?i=518

### Mecanismo de Log

- Ambos os serviços, **Serviço de API** e **Serviço de Cotações**, devem implementar um **mecanismo de log** que registre as operações realizadas.
- Os logs gerados por ambos os serviços devem ser armazenados em uma pasta denominada `logs` dentro do diretório do projeto.
- Os arquivos de log devem ter a extensão `.log`.
- É importante que os logs incluam informações detalhadas sobre as solicitações processadas, incluindo timestamp, tipo de solicitação, dados da solicitação (se aplicável) e quaisquer mensagens de erro ou alertas gerados durante o processamento.

## Arquitetura

![Diagrama de Arquitetura](arquitetura.png)

1. Um usuário solicita a cotação atual de uma ação da Apple: `GET /stock?q=aapl.us`
2. O serviço de API encaminha a solicitação para o serviço de cotações para obter as informações necessárias.
3. O serviço de cotações consulta a API externa, processa a resposta e retorna as informações para o serviço de API.
4. As informações são formatadas e enviadas de volta ao usuário.
