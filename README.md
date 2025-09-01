# swing-trade-b3

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

Ferramentas e automações para swing trade na B3.

## Ambiente de desenvolvimento

- Pré-requisitos: Python 3.11+ e Poetry 2.x
- Venv local: configurada via `poetry.toml` (`[virtualenvs] in-project = true`)

### Instalação

1) Instalar dependências

```
poetry install
```

2) Ativar o ambiente virtual (Poetry 2.x)

PowerShell (Windows):

```
Invoke-Expression (poetry env activate)
```

ou use sem ativar, prefixando com `poetry run` (ex.: `poetry run python -m app`).

3) Desativar (quando terminar)

```
deactivate

### Scripts de conveniência

Sem ativar a venv:

```
poetry run lint       # ruff check .
poetry run format     # black .
poetry run typecheck  # mypy .
poetry run test       # pytest com cobertura
```

Com a venv ativa, basta executar `lint`, `format`, `typecheck`, `test`.
```
