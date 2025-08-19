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

## Observabilidade

Aplicação FastAPI instrumentada com métricas de CPU, memória e latência expostas no endpoint `/metrics` para coleta via Prometheus.
