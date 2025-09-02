# CI – Falhas comuns e como corrigir

Este guia lista as falhas mais frequentes no CI e como resolvê‑las localmente.

## Testes e cobertura (< 100%)

- Sintoma: o job “Pytest (with coverage, 100% required)” falha com mensagem indicando cobertura abaixo de 100%.
- Como reproduzir localmente:
  - Com Poetry: `poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=100`
  - HTML detalhado: `poetry run pytest --cov=src --cov-report=html` e abra `htmlcov/index.html`.
- Como corrigir:
  - Escreva testes para as linhas listadas como “missing” (term-missing) ou destacadas em vermelho no relatório HTML.
  - Cubra também ramos de erro/validação. Use mocks para dependências externas.
  - Use `# pragma: no cover` apenas para trechos realmente inalcançáveis ou específicos de ambiente (com parcimônia).

## Falhas de testes (asserts/erros)

- Sintoma: `pytest` falha por exceções/asserts.
- Como reproduzir localmente: `poetry run pytest -x` (para parar no primeiro erro) ou `poetry run pytest -k <padrão>`.
- Como corrigir:
  - Ajuste a implementação ou o teste conforme a especificação desejada.
  - Verifique mensagens/tracebacks e rode somente o teste afetado para iterar rapidamente.

## Lint (Ruff)

- Sintoma: etapa “Ruff (lint)” falha.
- Reproduzir: `poetry run ruff check .`
- Corrigir: `poetry run ruff check . --fix` (auto‑fix); depois ajuste manualmente o que sobrar.

## Formatação (Black)

- Sintoma: etapa “Black (format check)” falha.
- Reproduzir: `poetry run black --check .`
- Corrigir: `poetry run black .`

## Tipagem (Mypy)

- Sintoma: etapa “Mypy (type check)” falha.
- Reproduzir: `poetry run mypy .`
- Corrigir: ajuste anotações e contratos; evite `Any`. Se necessário, suplemente stubs ou ignore pontuais com justificativa.

## Markdownlint

- Sintoma: job `markdownlint` falha.
- Reproduzir (requer Node 18+): `npx markdownlint-cli "**/*.md" --config .markdownlint.json`
- Corrigir: adeque títulos, listas e code fences; confira dicas em `CONTRIBUTING.md`.

## Dicas gerais

- Sempre rode localmente antes do push: `poetry run lint`, `poetry run format`, `poetry run typecheck`, `poetry run test`.
- Use `pre-commit` para automatizar checks: `pre-commit install` e depois `pre-commit run --all-files`.
- Em PRs, inclua evidências (saídas de comandos) para facilitar a revisão.
