# Swing Trade B3

[![CI](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml/badge.svg)](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](pyproject.toml)
[![Roadmap progress](https://progress-bar.dev/0/?title=milestones)](Agents.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> Automatizar operações de Swing Trade na B3 (Bolsa de Valores do Brasil) usando dados históricos e indicadores técnicos para gerar sinais de compra e venda, testar estratégias e acompanhar resultados.

## Índice

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
- [Testes](#testes)
- [Observabilidade](#observabilidade)
- [Roadmap](#roadmap)
- [Stack Tecnológica](#stack-tecnológica)
- [Contribuindo](#contribuindo)
- [Comunidade e Suporte](#comunidade-e-suporte)
- [Licença](#licença)
- [Aviso Legal](#aviso-legal)

## Visão Geral

O projeto visa construir um agente capaz de operar swing trade automatizado utilizando indicadores técnicos e dados históricos da B3.

## Status do Projeto

Status atual: **aguardando desenvolvimento**

![Progresso do roadmap](https://progress-bar.dev/0/?title=progresso&width=200)

## Recursos

- API REST com [FastAPI](https://fastapi.tiangolo.com/)
- Coleta e preparação de dados históricos da B3
- Estratégias configuráveis de entrada e saída
- Backtesting para validação de estratégias
- Integração futura com alertas e paper trading

## Arquitetura

O sistema é dividido em módulos independentes que tratam coleta de dados, geração de sinais, backtesting e exposição de API. Essa separação facilita a manutenção e a transparência de cada etapa do pipeline.

## Estrutura do Projeto

```
├── app/            # Interface REST com FastAPI
├── swing_trade/    # Lógica de trading e utilitários
├── tests/          # Testes automatizados
├── README.md       # Documentação principal
└── Agents.md       # Roadmap e instruções
```

## Como Começar

### Pré-requisitos

- [Python 3.11](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

### Instalação

Após clonar o repositório, instale as dependências com:

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

### Configuração

Crie um arquivo `.env` na raiz do projeto para variáveis sensíveis (tokens de API, chaves etc.). Nenhum valor é obrigatório no MVP, mas o uso de variáveis de ambiente garante transparência sobre a configuração.

## Uso

Inicie a aplicação FastAPI com:

```bash
poetry run uvicorn app.main:app --reload
```

Acesse `http://localhost:8000/docs` para explorar os endpoints disponíveis.

## Testes

Execute a suíte de testes com:

```bash
poetry run pytest
```

## Observabilidade

A aplicação FastAPI é instrumentada com métricas de CPU, memória e latência expostas no endpoint `/metrics` para coleta via Prometheus.

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

Para uma lista detalhada de tarefas e milestones, consulte o arquivo [Agents.md](Agents.md).

## Stack Tecnológica

Consulte o documento [TECH_STACK.md](TECH_STACK.md) para a lista completa de tecnologias utilizadas no projeto.

## Contribuindo

Leia o [CONTRIBUTING.md](CONTRIBUTING.md) para saber como colaborar com o projeto.

## Comunidade e Suporte

Problemas e sugestões podem ser registrados na aba [Issues](https://github.com/leotavo/swing-trade-b3/issues). Pull requests são bem-vindos.

## Licença

Este projeto é licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Aviso Legal

Este software é disponibilizado somente para fins educacionais. Ele não constitui recomendação de investimento e os autores não se responsabilizam por perdas financeiras decorrentes de seu uso.

