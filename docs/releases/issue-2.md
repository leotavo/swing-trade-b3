# Release: Issue #2 — .gitignore e convenção de branches

- Status: concluído
- Data: 2025-09-01
- Commits principais: dc6db46, 4bd3d3c, b5295cf, 47f8bee

Resumo

- .gitignore curado para Python/Poetry/IDE/OS: `__pycache__/`, `.pytest_cache/`, `.venv/`, `.mypy_cache/`, `.ruff_cache/`, `.vscode/`, `*.log`, `*.tmp`, `data/raw/`.
- Convenção de branches definida no `CONTRIBUTING.md`: `{type}/{slug}` com `type ∈ {feat, fix, docs, chore, refactor, test}` e exemplos.
- Conventional Commits documentados com exemplos, escopo opcional e breaking changes.

Evidências

- `git check-ignore` confirma arquivos temporários e de dados brutos ignorados.
- Commits de documentação e ajustes:
  - `dc6db46` — curadoria do `.gitignore` e marcação da M1-SI-2.1.
  - `4bd3d3c` — convenção de branches (M1-SI-2.2).
  - `b5295cf` — guia de Conventional Commits (M1-SI-2.3).
  - `47f8bee` — roadmap atualizado marcando Issue #2 concluída.

Arquivos de referência

- `.gitignore`
- `CONTRIBUTING.md`
- `docs/M1_subissues_atomic.md`
- `docs/MILESTONES_ISSUES.md`
