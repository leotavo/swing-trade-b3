# AGENTS.md - Operating Manual para o Codex

Nota específica deste repositório: cobertura de testes exigida é definida no `pyproject.toml`/CI (atual: 100%). Não reduzir sem issue aprovada.

> **Missão**: manter este repositório **sanitizado** (padrões consistentes, CI verde, segurança básica, documentação mínima) e acelerar entregas **sem quebrar contrato público do projeto**.
> Importante (Anti-OOM no VS Code): adotar o "Modo Leve" por padrão para evitar uso excessivo de memória durante as tarefas do Codex. Evite rodar verificações completas a cada mudança e foque em escopos pequenos. Detalhes em `docs/codex-execution-modes.md`.

## Idioma e Estilo

- Idioma padrão: português (pt-br) para prompts, respostas e preâmbulos do Codex.
- Termos de código, nomes de comandos e identificadores: manter em inglês (sem tradução).
- Tom: conciso, direto e colaborativo; foque em próximos passos e ações objetivas.
- Evitar pedir validação ao usuário a cada passo; consolidar checagens no fechamento da issue/PR.
- Encoding/EOL: UTF-8 (sem BOM) e `lf` em todos os arquivos de texto. Já configurado via `.editorconfig` e `.gitattributes`; pre-commit aplica `mixed-line-ending` e `fix-byte-order-marker`.

## 0) Contexto do Projeto (o que você precisa saber)

- Linguagem: **Python 3.11** (Poetry).
- Estrutura: `src/swing_trade_b3` (código) · `tests/` (testes) · `docs/` (documentação) · `.github/` (ci/config).
- API opcional com **FastAPI** (`src/swing_trade_b3/api/app.py`) — app factory `create_app()`; endpoint `/health`.
- CLI principal: `python -m swing_trade_b3 ...` (vide README).
- Qualidade atual (pyproject): **ruff**, **black**, **mypy**, **pytest** já configurados; pre-commit habilitado.
- CI: workflows em `.github/workflows/ci.yml` e `update-roadmap.yml`.

> **Regra de ouro**: **não** introduza mudanças de API pública, formatos de dados ou contratos de CLI sem issue aprovada.

---

## 1) Padrões de Qualidade e Gates (alvos que o PR deve atingir)

- **Lint/format**: `ruff` + `black` (line-length 100).
- **Tipos**: `mypy` (sem `Any` e sem `# type: ignore` desnecessários).
- **Testes**: `pytest` com cobertura conforme `pyproject.toml` (fonte de verdade). Não reduza thresholds sem issue aprovada.
- **Markdown**: `markdownlint` (usa `.markdownlint.json` quando houver; não bloquear PR só por estilo).
- **Pre-commit**: correções automáticas para whitespace, EOF, ruff/black.

Execução local (Modo Leve – evitar OOM):

- Instalação: `poetry install --with dev`.
- Durante a implementação: rode ferramentas de forma alvo/escopo (ex.: `poetry run ruff check src/swing_trade_b3/arquivo.py`, `poetry run mypy src/swing_trade_b3/módulo/`, `poetry run pytest -q -k <escopo>`).
- Validação final (uma vez, antes do PR): `poetry run ci` (ruff + black --check + mypy + pytest). Demais verificações completas ficam a cargo do CI no PR.

---

## 2) Branching, Commits e PR

- **Branch naming**: `feat/...`, `fix/...`, `chore/...`, `docs/...`, `test/...` (ex: `chore/codex-ready-sanitization`).
- **Commits**: estilo *Conventional Commits* (ex: `fix(connector-b3): handle empty series`).
- **PR**: use `.github/PULL_REQUEST_TEMPLATE.md` e preencha: **Resumo / Mudanças / Por quê / Como testar / Riscos / Próximos passos**.
- **Proteções**: PR **só** pode ser aprovado com CI verde (lint/type/test) + 1 review humano.
- **Evitar redundâncias**: não executar localmente, em cada iteração, o mesmo conjunto completo de checks que já roda no CI. Foque no escopo tocado e deixe a validação integral para o PR.

---

## 3) Tarefas de “Sanitização” (alto nível – focar escopos pequenos)

Siga estes itens como backlog de higiene, sempre quebrando em tarefas pequenas (evitar travar em tarefas grandes). Detalhes operacionais ficam nos docs citados.

1. **Criar branch** `chore/codex-ready`.
2. **.editorconfig**: garantir na raiz (`charset=utf-8`, `end_of_line=lf`, `insert_final_newline=true`; `indent_size 4` para `.py` e `2` para `.md`).
3. **Cobertura/pytest**: manter `addopts` conforme `pyproject.toml` (fonte de verdade). Não reduzir thresholds sem issue aprovada. Ver `docs/testing.md`.
4. **Mypy**: remover ignores supérfluos; tipar funções públicas; corrigir falhas triviais (sem relaxar regras). Ver `poetry run typecheck`.
5. **Ruff/Black**: normalizar imports, remover código morto/unused, aplicar format. Ver `poetry run lint` e `poetry run fmt`.
6. **Templates GitHub**: manter `bug.md` e `feature.md`; usar `ISSUE_TEMPLATE/codex-task.yml` (Objetivo, Critérios de Aceite, Como validar, Restrições).
7. **CODEOWNERS**: garantir `/.github/CODEOWNERS` (ex.: `@leotavo`).
8. **SECURITY.md**: manter canal de reporte e nota “não versionar segredos; usar GitHub Secrets/Actions vars”.
9. **.gitignore**: excluir `.venv/`, caches (`.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`), cobertura (`coverage.xml`, `htmlcov/`), IDE, `data/raw/`, `out/`.
10. **CI**: checar `.github/workflows/ci.yml` (3.11; ruff/black --check/mypy/pytest; markdownlint opcional; sem novos segredos). Detalhes: `docs/ci-status-checks.md`.
11. **Docs**: manter README com “Contribuir com o Codex” apontando para `docs/ci-status-checks.md`, `docs/ci-troubleshooting.md` e `docs/codex-execution-modes.md`.
12. **Segurança & Segredos**: garantir ausência de segredos em `src/`, `tests/`, `docs/`. Se houver, remover e instruir uso de GitHub Secrets.
13. **Smoke tests**: preservar testes rápidos do CLI básico e `/health` da API.
14. **Ajustes finais**: `pre-commit run --all-files`; validação final única: `poetry run ci`.

Entrega da sanitização (no PR):

- Lista de arquivos criados/alterados.
- Evidência de validação final (ex.: saída de `poetry run ci` ou link do job CI).
- Observações de follow-up (abrir issues `Codex-ready: follow-ups` quando necessário).

---

## 4) Do / Don’t (limites do patch)

**Faça:**

- Mudanças **pequenas e focadas** no hygiene (lint, tipos, testes, templates, CI).
- Cobrir com testes alterações em funções **públicas**.
- Padronizar mensagens de erro e logs sem mudar semântica.
- Adotar o Modo Leve (anti-OOM): evitar rodar checks completos repetidamente; preferir escopos pequenos; deixar execução integral para o PR.

**Não faça:**

- **Não** atualizar dependências de runtime sem justificativa e sem issue aprovada.
- **Não** alterar a API pública (FastAPI/CLI), nomes de arquivos de dados ou contratos de saída.
- **Não** adicionar serviços externos, telemetry ou workflows que exijam novos segredos.
- **Não** solicitar checagens do usuário a todo momento; consolide validações e peça revisão apenas no fechamento da issue/PR.

---

## 5) Como validar (checklist rápido – ao concluir a issue)

- [ ] `pre-commit run --all-files` sem alterações pendentes.
- [ ] Validação local única: `poetry run ci` (sequência idêntica ao CI).
- [ ] CI (`ci.yml`) verde no PR (cobertura conforme `pyproject.toml`).
- [ ] Se tocou docs/CLI/API: atualizar docs relevantes e incluir instruções de teste em PR.

---

## 6) Mapa de diretórios (referência)

- **src/swing_trade_b3/**: código-fonte (CLI, conectores, processamento, API).
- **tests/**: testes unit/smoke/integração leve.
- **docs/**: guias de CI, troubleshooting, tech stack, data schema, releases.
- **.github/**: workflows, templates de issue/PR (adicionar `codex-task.yml`), CODEOWNERS.

> Em caso de dúvida, **abra uma issue `codex-task`** com objetivo, critérios de aceite e como validar. O patch deve ser o mínimo necessário para “ficar verde”. Para diretrizes de execução leves e anti-OOM, consulte `docs/codex-execution-modes.md`.
