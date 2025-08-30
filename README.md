# Swing Trade B3

[![CI](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml/badge.svg)](https://github.com/leotavo/swing-trade-b3/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](pyproject.toml)
[![Roadmap progress](https://progress-bar.dev/0/?title=milestones)](Agents.md)

> Automatizar operações de Swing Trade na B3 (Bolsa de Valores do Brasil) usando dados históricos e indicadores técnicos para gerar sinais de compra e venda, testar estratégias e acompanhar resultados.

## Índice

- [Visão Geral](#vis%C3%A3o-geral)
- [Status do Projeto](#status-do-projeto)
- [Roadmap](#roadmap)
- [Instalação](#instala%C3%A7%C3%A3o)
- [Execução](#execu%C3%A7%C3%A3o)
- [Observabilidade](#observabilidade)
- [Stack Tecnológica](#stack-tecnol%C3%B3gica)
- [Contribuindo](#contribuindo)
- [Licença](#licen%C3%A7a)

## Visão Geral

O projeto visa construir um agente capaz de operar swing trade automatizado utilizando indicadores técnicos e dados históricos da B3.

## Status do Projeto

Status atual: **aguardando desenvolvimento**

![Progresso do roadmap](https://progress-bar.dev/0/?title=progresso&width=200)

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

## Instalação

Este projeto utiliza [Poetry](https://python-poetry.org/) para gerenciar as dependências. Após clonar o repositório, instale-as executando:

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

A aplicação FastAPI é instrumentada com métricas de CPU, memória e latência expostas no endpoint `/metrics` para coleta via Prometheus.

## Stack Tecnológica

Consulte o documento [TECH_STACK.md](TECH_STACK.md) para a lista completa de tecnologias utilizadas no projeto.

## Contribuindo

Leia o [CONTRIBUTING.md](CONTRIBUTING.md) para saber como colaborar com o projeto.

## Licença

Este projeto é licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

