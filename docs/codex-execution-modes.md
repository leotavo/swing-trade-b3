# Modo de Execução do Codex (Anti-OOM)

Objetivo: evitar consumo excessivo de memória (OOM) ao trabalhar com o VS Code/CLI, mantendo o fluxo produtivo e o CI como fonte de verdade. Idioma padrão dos prompts/respostas: pt-br.

## Princípios
- Foco em escopos pequenos: altere e valide apenas o que foi tocado.
- Evite redundâncias: não replique localmente, a cada iteração, tudo que o CI já executa.
- Validação integral apenas no fechamento da issue/PR (uma passada): `poetry run ci`.
- Preferir comandos e leituras “pontuais” ao invés de varreduras globais.

## Modo Leve (padrão)
- Lint: `poetry run ruff check <paths_tocados>`
- Format (quando necessário): `poetry run fmt` (ou `black .` se for a intenção)
- Tipos: `poetry run mypy <pastas_tocadas>`
- Testes rápidos: `poetry run pytest -q -k <padrão>` (evitar relatórios HTML locais)
- Evitar leitura/varredura de diretórios pesados (ex.: `data/`, `out/`, `htmlcov/`).
- Preferir busca por padrão com `rg`/grep ou abrir arquivos específicos, ao invés de abrir toda a árvore.

## Validação Completa (PR/conclusão de issue)
- Rodar uma única vez localmente (opcional): `poetry run ci`.
- Confiar no pipeline do GitHub Actions para a execução integral (ruff, black --check, mypy, pytest com cobertura conforme `pyproject.toml`).
- Anexar no PR evidência (ex.: link dos jobs verdes; logs do `poetry run ci` se pertinente).

## Dividir Tarefas Grandes
- Se a tarefa parecer pesada (muitas alterações, impacto amplo), quebre em subtarefas e PRs menores.
- Use o template `.github/ISSUE_TEMPLATE/codex-task.yml` para registrar objetivo, critérios de aceite e como validar.
- Foque no “mínimo necessário para ficar verde” por entrega.

## Evitar Pedidos de Checagem Repetitivos
- Consolide perguntas/validações no final de uma entrega.
- Só interrompa o fluxo para confirmar ações destrutivas ou decisões de escopo.

## Referências
- `docs/testing.md` — comandos e dicas de cobertura
- `docs/ci-status-checks.md` — o que o CI valida
- `docs/ci-troubleshooting.md` — resolução de problemas comuns no CI
