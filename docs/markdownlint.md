# Markdownlint — Guia de Uso

Este projeto usa o markdownlint para padronizar Markdown em documentos e README.

## Regras ativas

- Base: `markdownlint:recommended` (via `.markdownlint.json`).
- Desativadas por contexto do projeto:
  - MD013: comprimento de linha (desativada para facilitar diffs e URLs longas).
  - MD033: HTML em Markdown (permitimos casos pontuais).
  - MD041: heading de nível 1 no início do arquivo (não exigido em todos os docs).

## Regras comuns no repositório

- MD040: sempre especifique a linguagem em blocos de código (ex.: `bash`, `json`, `text`).
- MD022: deixe 1 linha em branco antes/depois de títulos (#, ##, ...).
- MD032: deixe 1 linha em branco antes/depois de listas (-, *, 1.).

## Como executar localmente

Pré-requisito: Node.js 18+.

```bash
npx markdownlint-cli "**/*.md" --config .markdownlint.json
```

## Pre-commit

Há um hook configurado em `.pre-commit-config.yaml`.

Instalar hooks:

```bash
pre-commit install
```

Checar todo o repositório:

```bash
pre-commit run markdownlint --all-files
```

## CI

O GitHub Actions roda um job `markdownlint` em `.github/workflows/ci.yml` usando `markdownlint-cli`.
