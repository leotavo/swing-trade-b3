# Release: Issue #1 — Criar repositório GitHub com Python + Poetry

- Status: concluído
- Data: 2025-09-01
- Commit de validação: ee0ac42

Resumo

- Estrutura base criada: `src/app/`, `tests/`, `README.md`, `LICENSE` (MIT).
- Poetry configurado com layout `src` e pacote `app`.
- Python fixado em `^3.11` e venv local via `poetry.toml`.
- Ferramentas dev: ruff, black, mypy, pytest (com seções de config e scripts).
- CLI mínima: `python -m app` imprime e retorna exit code 0.
- Testes smoke passando (3 passed).
- Pre-commit configurado e executando hooks básicos.

Evidências

- `poetry run python -m app` → OK
- `poetry run pytest -q` → 3 passed
- `poetry run pre-commit run --all-files` → Passed

Arquivos de referência

- `pyproject.toml`
- `poetry.lock`
- `poetry.toml`
- `README.md`
- `LICENSE`
- `src/app/__main__.py`, `src/app/__init__.py`, `src/app/cli.py`
- `tests/test_smoke.py`
