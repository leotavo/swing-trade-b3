# swing-trade-b3

[![CI](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml/badge.svg)](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml) [![Quality Gate](https://img.shields.io/sonar/quality_gate/leotavo_swing-trade-b3?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/summary/new_code?id=leotavo_swing-trade-b3) [![Coverage](https://img.shields.io/sonar/coverage/leotavo_swing-trade-b3?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/summary/new_code?id=leotavo_swing-trade-b3) ![Python](https://img.shields.io/badge/python-3.11-blue.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

 Ferramentas e automações para swing trade na B3.

 Consulte o Tech Stack em [docs/TECH_STACK.md](docs/TECH_STACK.md).

## Documentação

- Checks de CI: `docs/ci-status-checks.md`
- Troubleshooting de CI: `docs/ci-troubleshooting.md`
- Especificação do conector de dados: `docs/data-connector-spec.md`
- Esquema de dados: `docs/data-schema.md`
- Fluxo de Git: `docs/git-flow.md`
- Tech Stack: `docs/TECH_STACK.md`
- Guia do Markdownlint: `docs/markdownlint.md`
- Guia de testes e cobertura: `docs/testing.md`

 - Modos de execução do Codex (Anti-OOM): `docs/codex-execution-modes.md`
## Ambiente de desenvolvimento

- Pré-requisitos: Python 3.11+ e Poetry 2.x
- Venv local: configurada via `poetry.toml` (`[virtualenvs] in-project = true`)

### Instalação

1. Instalar dependências

```bash
poetry install
```

1. Ativar o ambiente virtual (Poetry 2.x)

PowerShell (Windows):

```powershell
Invoke-Expression (poetry env activate)
```

ou use sem ativar, prefixando com `poetry run` (ex.: `poetry run python -m swing_trade_b3`).

1. Desativar (quando terminar)

```powershell
deactivate
```

### Scripts de conveniência

Sem ativar a venv:

```bash
poetry run lint       # ruff check .
poetry run format     # black .
poetry run typecheck  # mypy .
poetry run test       # pytest com cobertura (exige 100%)
```

Com a venv ativa, basta executar `lint`, `format`, `typecheck`, `test`.

### Cobertura de testes (100%)

- Cobertura rápida no terminal: `poetry run pytest --cov=src --cov-report=term-missing`
- Enforçar 100%: `poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=100`
- Relatório HTML: `poetry run pytest --cov=src --cov-report=html` e abra `htmlcov/index.html`

Dicas e boas práticas: veja `docs/testing.md`.

## Fluxo de Git

- Convenção de branches: `{type}/{slug}` (feat, fix, docs, chore, refactor, test). Veja `CONTRIBUTING.md`.
- Proteções da `main` e política de PR: consulte `docs/git-flow.md`.
- Mensagens seguindo Conventional Commits.

## Coleta de dados (CLI)

Com a venv ativa, exemplos:

```bash
# Um símbolo em CSV
python -m swing_trade_b3 fetch --symbol PETR4 --start 2023-01-01 --end 2024-01-01

# Parquet comprimido (snappy) com throttle de 5 req/s
python -m swing_trade_b3 fetch --symbol PETR4 --start 2023-01-01 --end 2024-01-01 \
  --format parquet --compression snappy --throttle 0.2

# Vários símbolos via linha e arquivo
python -m swing_trade_b3 fetch -s PETR4 VALE3 --symbols-file symbols.txt \
  --start 2023-01-01 --end 2024-01-01 --format parquet

# Forçar histórico completo do provedor e filtrar localmente
python -m swing_trade_b3 fetch --symbol PETR4 --start 2008-01-01 --end 2025-01-01 --force-max

# Resumo em JSON (para automações)
python -m swing_trade_b3 fetch -s PETR4 VALE3 --start 2023-01-01 --end 2024-01-01 \
  --format parquet --compression snappy --throttle 0.2 \
  --json-summary out/summary.json

# Logging estruturado (JSON)
python -m swing_trade_b3 fetch --symbol PETR4 --start 2023-01-01 --end 2024-01-01 \
  --log-json  # emite logs no stdout em JSON (útil p/ observabilidade/CI)
```

Arquivo `symbols.txt` (exemplo):

```text
# carteira base
PETR4
VALE3
ITUB4
```

Saída e comportamento:

- Salva em `data/raw/{SYMBOL}/YYYY.csv|.parquet` com mesclagem idempotente e sem duplicatas.
- Resumo final com sucessos/falhas por símbolo.
- `--throttle` limita a taxa de requisições; retries usam o mesmo limitador.
- `--json-summary` grava um relatório estruturado (run/symbols/summary) para uso em CI/scripts.

Exemplo de JSON (resumo)

```json
{
  "run": {
    "started_at": "2025-09-01T17:13:49Z",
    "ended_at": "2025-09-01T17:13:51Z",
    "duration_s": 1.35,
    "provider": "brapi.dev",
    "args": {
      "start": "2023-01-01",
      "end": "2024-01-01",
      "format": "parquet",
      "compression": "snappy",
      "throttle": 0.2,
      "force_max": false,
      "symbols": ["PETR4", "VALE3"]
    }
  },
  "symbols": [
    {
      "symbol": "PETR4",
      "status": "ok",
      "rows": 248,
      "date_first": "2023-01-02",
      "date_last": "2023-12-28",
      "files": ["data/raw/PETR4/2023.parquet"],
      "range_used": "5y",
      "duration_s": 0.78,
      "http": {"attempts": 1, "retries": 0, "sleep_total_s": 0.0, "last_status": 200, "throttle_calls": 1}
    },
    {
      "symbol": "VALE3",
      "status": "ok",
      "rows": 248,
      "date_first": "2023-01-02",
      "date_last": "2023-12-28",
      "files": ["data/raw/VALE3/2023.parquet"],
      "range_used": "5y",
      "duration_s": 0.56,
      "http": {"attempts": 1, "retries": 0, "sleep_total_s": 0.0, "last_status": 200, "throttle_calls": 1}
    }
  ],
  "summary": {"ok": 2, "no_data": 0, "failed": 0, "total": 2}
}
```

## Processamento de dados (CLI)

Converte dados brutos de `data/raw/{SYMBOL}/YYYY.(csv|parquet)` para dataset processado idempotente em `data/processed/{SYMBOL}.(parquet|csv)`.

Pré‑requisito: ter dados brutos salvos via `fetch`.

```bash
# Processar um símbolo (Parquet com snappy)
python -m swing_trade_b3 process --symbol PETR4 --start 2023-01-01 --end 2024-01-01 \
  --format parquet --compression snappy

# Processar vários símbolos
python -m swing_trade_b3 process -s PETR4 VALE3 --format parquet --compression snappy

# Logging JSON durante o processamento
python -m swing_trade_b3 process -s PETR4 --log-json
```

Saída e comportamento:

- Lê partições em `data/raw/{SYMBOL}/` (CSV e/ou Parquet).
- Limpa e valida (sem nulos/negativos; dtypes corretos; UTC; dedupe e ordenação por `symbol,date`).
- Salva idempotente em `data/processed/{SYMBOL}.parquet` (ou `.csv`).

## Pipeline ponta a ponta (fetch → process)

Exemplo prático coletando dados brutos e gerando o dataset processado:

```bash
# 1) Coletar dados brutos (Parquet + snappy) com throttle e summary
python -m swing_trade_b3 fetch -s PETR4 VALE3 \
  --start 2023-01-01 --end 2024-01-01 \
  --format parquet --compression snappy --throttle 0.2 \
  --json-summary out/fetch-summary.json

# 2) Processar para dataset final (idempotente)
python -m swing_trade_b3 process -s PETR4 VALE3 \
  --start 2023-01-01 --end 2024-01-01 \
  --format parquet --compression snappy

# Arquivos gerados (exemplos):
# - data/raw/PETR4/2023.parquet, data/raw/VALE3/2023.parquet
# - data/processed/PETR4.parquet, data/processed/VALE3.parquet
```

## Observabilidade

- Logs estruturados: use `--log-json` para emitir logs em JSON (um por linha), ideal para pipelines/ELK.
  - Exemplo: `python -m swing_trade_b3 fetch -s PETR4 --start 2023-01-01 --end 2024-01-01 --log-json > logs/fetch.jsonl`
- Resumo de execução: use `--json-summary PATH` para gerar um relatório consolidado da execução.
  - Exemplo: `python -m swing_trade_b3 fetch -s PETR4 --start 2023-01-01 --end 2024-01-01 --json-summary out/summary.json`
- Recomendações: use ambos — logs para timeline e troubleshooting; summary para integrações/CI.
  - Exemplo completo de summary: `docs/summary-example.json`.

### Consultas rápidas com `jq`

Filtrar apenas WARN/ERROR (Unix shells):

```bash
jq -r 'select(.level=="WARNING" or .level=="ERROR") | .time+" "+.level+" "+.message' logs/fetch.jsonl
```

Salvar particionamentos escritos (persistence):

```bash
jq -r 'select(.logger=="app.persistence" and .message=="saved raw partition") | {symbol,year,rows,bytes,path}' logs/fetch.jsonl
```

Contar ocorrências por nível:

```bash
jq -s 'group_by(.level) | map({level: .[0].level, count: length})' logs/fetch.jsonl
```

Filtrar eventos HTTP 429 (rate limit):

```bash
jq -r 'select(.logger=="app.connector.b3" and (.message|test("429")))' logs/fetch.jsonl
```

Observação (PowerShell): use aspas duplas e escape `"` conforme necessário.

## Padrões de Estilo

- Idioma: explique e documente em português (pt‑BR); mantenha nomes de funções, variáveis e identificadores em inglês.
- Commits: Conventional Commits (ex.: `feat:`, `fix:`, `docs:`, `chore:`). Mensagens podem ser em português; escopo/código permanecem em inglês.
- Código: siga tipagem e lint configurados (ruff, black, mypy) e priorize nomes claros em inglês.

Veja também um exemplo completo em:

- docs/summary-example.json

## Contribuir com o Codex

- Idioma padrão: pt-br para prompts/respostas do Codex (termos de código em inglês).

Checks rápidos antes do PR:

```bash
poetry install --with dev
poetry run ruff check . && poetry run ruff format --check
poetry run black --check .
poetry run mypy src
poetry run pytest
```

Consultas úteis:
- docs/ci-status-checks.md
- docs/ci-troubleshooting.md

### Modo Leve (anti-OOM) — recomendado

Durante o desenvolvimento, execute checagens por escopo tocado:

```bash
poetry run ruff check <paths_tocados>
poetry run mypy <pastas_tocadas>
poetry run pytest -q -k <padrao>
```

Validação final única (antes do PR):

```bash
poetry run ci
```

Mais detalhes: `docs/codex-execution-modes.md`

## API (FastAPI)

- Iniciar localmente:

```bash
poetry run uvicorn swing_trade_b3.api.app:create_app --factory --reload --host 0.0.0.0 --port 8000
```

- Healthcheck:
  - GET `/health` -> `{ "status": "ok", "version": "<semver>" }`

Observação: a API é opcional nesta fase; o pipeline via CLI segue como principal.
