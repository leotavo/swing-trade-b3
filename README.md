# Swing Trade B3

[![CI](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml/badge.svg)](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml)
[![CodeQL](https://github.com/leotavo/swing-trade-b3/actions/workflows/codeql.yml/badge.svg)](https://github.com/leotavo/swing-trade-b3/actions/workflows/codeql.yml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/dependabot)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](pyproject.toml)
[![M1 - Community & CI](https://img.shields.io/github/milestones/progress/leotavo/swing-trade-b3/1?logo=github)](https://github.com/leotavo/swing-trade-b3/milestone/1)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Open Issues](https://img.shields.io/github/issues/leotavo/swing-trade-b3)](https://github.com/leotavo/swing-trade-b3/issues)
[![GitHub Stars](https://img.shields.io/github/stars/leotavo/swing-trade-b3)](https://github.com/leotavo/swing-trade-b3/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/leotavo/swing-trade-b3)](https://github.com/leotavo/swing-trade-b3/network/members)
[![Last Commit](https://img.shields.io/github/last-commit/leotavo/swing-trade-b3)](https://github.com/leotavo/swing-trade-b3/commits)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/leotavo/swing-trade-b3/branch/main/graph/badge.svg)](https://codecov.io/gh/leotavo/swing-trade-b3)
[![Docs](https://img.shields.io/badge/docs-latest-blue.svg)](https://github.com/leotavo/swing-trade-b3/wiki)
[![GitHub Release](https://img.shields.io/github/v/release/leotavo/swing-trade-b3?include_prereleases)](https://github.com/leotavo/swing-trade-b3/releases)
[![Roadmap](https://img.shields.io/badge/roadmap-Milestones-blue)](https://github.com/leotavo/swing-trade-b3/milestones)

> **Resumo**
> Agente para automatizar Swing Trade na B3 com dados históricos, indicadores técnicos, backtesting e API REST para integração.
> O idioma padrão do projeto é o português.

## TL;DR (Resumo rápido)

```bash
git clone https://github.com/leotavo/swing-trade-b3 && cd swing-trade-b3
poetry install
cp -n .env.example .env || true
make dev
# smoke-test
curl -fsS http://localhost:8000/healthz | jq .
curl -I http://localhost:8000/metrics | head -n 1
```

## Índice

- [Swing Trade B3](#swing-trade-b3)
  - [TL;DR (Resumo rápido)](#tldr-resumo-rápido)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
  - [Status do Projeto](#status-do-projeto)
  - [Recursos](#recursos)
  - [Arquitetura](#arquitetura)
  - [Estrutura do Projeto](#estrutura-do-projeto)
  - [Como Começar](#como-começar)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação](#instalação)
    - [Configuração](#configuração)
  - [Uso](#uso)
  - [Observabilidade](#observabilidade)
    - [Teste rápido](#teste-rápido)
  - [Comandos de Desenvolvimento](#comandos-de-desenvolvimento)
  - [Testes e Qualidade](#testes-e-qualidade)
  - [Roadmap](#roadmap)
  - [Stack Tecnológica](#stack-tecnológica)
  - [Contribuindo](#contribuindo)
  - [Comunidade e Suporte](#comunidade-e-suporte)
  - [Licença](#licença)
  - [Aviso Legal](#aviso-legal)
  - [Troubleshooting Rápido](#troubleshooting-rápido)

## Visão Geral

O projeto visa construir um agente capaz de operar swing trade automatizado utilizando indicadores técnicos e dados históricos da B3.

## Status do Projeto

Status atual: **M1 – Community & CI em progresso**

[![M1 - Community & CI](https://img.shields.io/github/milestones/progress/leotavo/swing-trade-b3/1?logo=github)](https://github.com/leotavo/swing-trade-b3/milestone/1)

## Recursos

- API REST com [FastAPI](https://fastapi.tiangolo.com/)
- Coleta e preparação de dados históricos da B3 (fallback: *yfinance → brapi → B3*)
- Estratégias configuráveis (ex.: RSI, MACD, EMAs)
- Backtesting com custos e *slippage* padrão
- Observabilidade (healthcheck e métricas Prometheus)
- Integração futura com alertas e *paper trading*

## Arquitetura

Divisão em módulos independentes: ingestão, estratégias/sinais, backtesting e API.

```mermaid
flowchart LR
    A["Fontes de dados: yfinance, brapi, B3"] --> B["Ingestão e Preparação"]
    B --> C["Estratégias e Sinais"]
    C --> D["Backtesting"]
    C --> E["API \(FastAPI\)"]
    D --> F["Relatórios e Resultados"]
    E --> G["Notificações: e-mail e Telegram"]
```

## Estrutura do Projeto

```bash
├── app/             # Interface REST (FastAPI)
├── swing_trade/     # Núcleo: dados, indicadores, sinais, backtesting
├── tests/           # Testes automatizados
├── README.md        # Documentação principal
└── AGENTS.md        # Roadmap e instruções operacionais
```

## Como Começar

### Pré-requisitos

- [Python 3.11](https://www.python.org/)
- [Poetry](https://python-poetry.org/) instalado e no PATH

### Instalação

```bash
poetry install
# opcional: requirements.txt para pip
poetry export -f requirements.txt -o requirements.txt --without-hashes
```

### Configuração

Crie um `.env` (ou copie do `.env.example`). Exemplo:

```ini
# Timezone de exibição (interno em UTC)
TZ_DISPLAY=America/Sao_Paulo

# Provedores e custos (bps = 0,01%)
DATA_PROVIDER=yfinance
FEES_ROUNDTRIP_BPS=10
SLIPPAGE_BPS=10

# Tokens/chaves (opcionais)
BRAPI_TOKEN=
ALPHAVANTAGE_KEY=

# Futuro: persistência
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname
```

## Uso

Se você usou o **TL;DR**, a API estará em `http://localhost:8000`.

Iniciar manualmente:

```bash
make run
# ou:
poetry run uvicorn app.main:app --reload --port 8000
```

## Observabilidade

- **Healthcheck:** `GET /healthz` → `{"status":"ok"}`
- **Métricas Prometheus:** `GET /metrics` (OpenMetrics `text/plain; version=0.0.4`)
- Testes cobrem disponibilidade e formato para evitar regressões.

### Teste rápido

```bash
curl -fsS http://localhost:8000/healthz | jq .
curl -I    http://localhost:8000/metrics | head -n 1
curl -fsS  http://localhost:8000/metrics | head -n 20
```

## Comandos de Desenvolvimento

| Comando            | Ação                                             |
|--------------------|--------------------------------------------------|
| `make dev`         | Sobe FastAPI com reload                          |
| `make run`         | Executa a API (sem reload)                       |
| `make lint`        | ruff/black                                       |
| `make format`      | Formata código                                   |
| `make typecheck`   | mypy (strict)                                    |
| `make test`        | pytest                                           |
| `make cov`         | cobertura local                                  |
| `make ci`          | lint + typecheck + test + cov                    |

## Testes e Qualidade

```bash
make test
make typecheck
make lint
```

Para um lint rápido apenas nos arquivos modificados, utilize `pre-commit run --files <arquivos_modificados>`.

- Meta de cobertura: **≥ 80% (alerta se abaixo)**
- Estilo: **ruff + black**
- Tipagem: **mypy (strict)**
- CI: GitHub Actions (lint, typecheck, testes, cobertura)

## Roadmap

- [ ] M1 - Configuração Inicial
- [ ] M2 - Coleta e Preparação de Dados
- [ ] M3 - Estratégia Base Swing Trade
- [ ] M4 - Backtesting Inicial
- [ ] M5 - Notificações e Monitoramento
- [ ] M6 - Ajuste de Parâmetros e Otimização
- [ ] M7 - Modelo de ML Básico
- [ ] M8 - Paper Trading
- [ ] M9 - Observabilidade Básica
- [ ] M10 - Segurança e Compliance
- [ ] M11 - Documentação e Guias
- [ ] M12 - Validação Final do MVP

> Para detalhes, veja [AGENTS.md](AGENTS.md).

## Stack Tecnológica

Confira [TECH_STACK.md](TECH_STACK.md).

## Contribuindo

Leia o [CONTRIBUTING.md](CONTRIBUTING.md) e siga *Conventional Commits*.
PRs com testes e atualização de docs quando aplicável.
Branches devem seguir `feat/`, `fix/` ou `docs/` e são verificadas automaticamente no CI. Antes de abrir o PR, renomeie a branch para seguir esse padrão. Um workflow renomeia automaticamente branches criadas pelo Codex para esse padrão antes da validação.
Se o workflow falhar devido ao nome, renomeie a branch para começar com um dos prefixos permitidos (ex.: `fix/codex-add-branch-name-validation-workflow`).

## Comunidade e Suporte

- Código de Conduta: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Dúvidas gerais: [Discussions](https://github.com/leotavo/swing-trade-b3/discussions)
- Bugs/features: [Issues](https://github.com/leotavo/swing-trade-b3/issues)
- Segurança: [SECURITY.md](SECURITY.md)

## Licença

MIT — veja [LICENSE](LICENSE).

## Aviso Legal

Projeto **educacional**. Não constitui recomendação de investimento. Os autores não se responsabilizam por perdas financeiras.

## Troubleshooting Rápido

- **Poetry não encontrado**: `pipx install poetry` ou docs oficiais.
- **Porta 8000 ocupada**: `make dev PORT=8001` e acesse `http://localhost:8001`.
- **Windows/PowerShell**: use `curl` do Git ou `iwr/irm`.
- **.env**: mantenha na raiz e reinicie o servidor após alterações.

<!-- Teste de verificação de verificação de branch -->
