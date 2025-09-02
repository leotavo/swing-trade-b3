# Testes e Cobertura (100%)

Este projeto usa `pytest` com `pytest-cov` para medir a cobertura dos testes. As dependências de desenvolvimento já incluem o plugin (`pytest-cov`).

## Pré‑requisitos

- Python 3.11+
- Poetry 2.x
- Dependências instaladas: `poetry install`

## Como rodar os testes

Execução básica (silenciosa):

```bash
poetry run pytest -q
```

Atalho com cobertura 100% obrigatória (default via pyproject):

```bash
poetry run test
```

Este script executa `pytest` com cobertura e falha se < 100% (conforme `[tool.pytest.ini_options]` no `pyproject.toml`).

## Cobertura de testes

- Cobertura no terminal (com linhas faltantes) — já é padrão:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

- Enforçar 100% de cobertura (falha se < 100%) — já é padrão:

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=100
```

- Relatório HTML (navegável em `htmlcov/index.html`):

```bash
poetry run pytest --cov=src --cov-report=html
```

- XML para integrações de CI: o script `poetry run test` já gera `coverage.xml` por padrão e exige 100% de cobertura.

## Dicas avançadas

- Desativar temporariamente as opções padrão (ex.: rodar rápido sem cobertura):

```bash
poetry run pytest -q -o addopts=
```

- Injetar opções adicionais sem editar `pyproject.toml`:

```bash
PYTEST_ADDOPTS="-k mytestpattern" poetry run pytest
```

## Dicas para alcançar 100%

- Cubra caminhos de erro e validações (ex.: argumentos inválidos, arquivos ausentes, ranges de datas inconsistentes).
- Teste o CLI (`app.__main__.py`): cenários com e sem subcomandos, parâmetros obrigatórios/ausentes.
- Use `pytest.mark.parametrize` para variações de entradas sem código duplicado.
- Isole integrações externas com dublês (mocks/stubs) para forçar ramos difíceis.
- Marque apenas trechos verdadeiramente inalcançáveis com `# pragma: no cover` (ex.: salvaguardas de logging/formatters, branches dependentes de SO). Evite usar como atalho.

## Observações

- Se estiver rodando `pytest` fora do ambiente Poetry e receber erro "unrecognized arguments: --cov...", instale o plugin manualmente: `pip install pytest-cov`.
- Por padrão, não forçamos 100% via configuração global para não surpreender contribuidores; use a flag `--cov-fail-under=100` quando desejar enforcing local ou em jobs específicos de CI.
