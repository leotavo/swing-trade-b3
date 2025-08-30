# Swing Trade B3

Objetivo principal

Automatizar operações de Swing Trade na B3 (Bolsa de Valores do Brasil) usando dados históricos e indicadores técnicos para gerar sinais de compra e venda, testar estratégias e acompanhar resultados.

Status: aguardando desenvolvimento

## Instalação

Este projeto utiliza [Poetry](https://python-poetry.org/) para gerenciar as dependências.
Após clonar o repositório, instale-as executando:

```bash
poetry install
```

Como alternativa, o projeto pode ser instalado em modo editável com `pip`:

```bash
pip install -e .
```

Para gerar um arquivo `requirements.txt` compatível com `pip`, utilize:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Execução

Inicie a aplicação FastAPI com:

```bash
poetry run uvicorn app.main:app --reload
```

Para rodar os testes:

```bash
pip install -e .
pytest
```

Ou utilizando Poetry:

```bash
poetry install
poetry run pytest
```

## Observabilidade

Aplicação FastAPI instrumentada com métricas de CPU, memória e latência expostas no endpoint `/metrics` para coleta via Prometheus.

## Licença

Este projeto é licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
