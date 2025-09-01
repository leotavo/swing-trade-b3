# Milestone 1 — Configuração Inicial
_Subissues atômicas com critérios de aceite_

> Contexto: M1 cobre 3 issues — **#1 Criar repositório com Python + Poetry**, **#2 .gitignore + convenção de branches**, **#3 Pipeline inicial (GitHub Actions)**.  
> Formato padrão por subissue: **Objetivo**, **Escopo**, **Critérios de Aceite**, **Entregáveis**, **Notas**.

---

## Issue #1 — Criar repositório GitHub com Python + Poetry

### M1-SI-1.1 — Inicializar repositório e estrutura base
**Objetivo.** Criar repositório com commit inicial e diretórios básicos.  
**Escopo.** README, LICENSE (MIT), estrutura `src/`, pasta `tests/`.  
**Critérios de Aceite.**
- [x] Repositório com commit inicial e `README.md` com título do projeto.
- [x] `LICENSE` com MIT.
- [x] Estrutura criada: `src/app/` e `tests/` (com `__init__.py` onde couber).
**Entregáveis.** Árvores de diretório + screenshot/print do primeiro commit.  
**Notas.** Sem CI e sem .gitignore (tratados em outras issues).

---

### M1-SI-1.2 — Configurar Poetry (layout src)
**Objetivo.** Configurar `pyproject.toml` com layout `src` e pacote `app`.  
**Escopo.** `poetry init` + ajustes para layout `src`.  
**Critérios de Aceite.**
- [x] `pyproject.toml` com `name`, `version`, `description` e `authors` definidos.
- [x] Mapeamento de pacote: `packages = [{ include = "app", from = "src" }]`.
- [x] `poetry lock` executa sem erros e gera `poetry.lock`.
**Entregáveis.** Diff do `pyproject.toml` + saída do `poetry lock`.  
**Notas.** Sem dependências além das padrão do projeto.

---

### M1-SI-1.3 — Fixar Python 3.11 e venv no projeto
**Objetivo.** Garantir versão e isolamento reprodutíveis.  
**Escopo.** Definição da versão Python e venv local.  
**Critérios de Aceite.**
- [x] `tool.poetry.dependencies.python = "^3.11"` no `pyproject.toml`.
- [x] Venv no diretório do projeto configurada (`poetry config virtualenvs.in-project true`).
- [x] README atualizado com instruções de ativação (`poetry install`, `poetry shell`).
**Entregáveis.** Trechos do `pyproject.toml` + README.  
**Notas.** Não criar `.venv` no git (será ignorado via .gitignore na Issue #2).

---

### M1-SI-1.4 — Instalar dev-deps e scripts (ruff, black, mypy, pytest)
**Objetivo.** Preparar ferramentas locais de qualidade.  
**Escopo.** Adicionar dev-deps e scripts de conveniência em `pyproject.toml`.  
**Critérios de Aceite.**
- [x] Dev-deps instaladas: `ruff`, `black`, `mypy`, `pytest`, `pytest-cov`.
- [x] Seções `[tool.ruff]`, `[tool.black]`, `[tool.mypy]` definidas.
- [x] Scripts `lint`, `format`, `typecheck`, `test` definidos em `[tool.poetry.scripts]` ou `tool.task`.
**Entregáveis.** Diff do `pyproject.toml` + execução dos comandos (prints).  
**Notas.** CI virá na Issue #3.

---

### M1-SI-1.5 — Esqueleto de CLI mínima
**Objetivo.** Executar `python -m app` e retornar exit code 0.  
**Escopo.** `src/app/__main__.py` com `main()` simples e `__version__` em `app/__init__.py`.  
**Critérios de Aceite.**
- [x] `python -m app` imprime uma linha de teste e encerra com exit code 0.
- [x] `app.__version__` disponível e importável.
**Entregáveis.** Saída do terminal + trecho do código.  
**Notas.** Sem argumentos/flags por enquanto.

---

### M1-SI-1.6 — Teste smoke inicial
**Objetivo.** Validar import básico e execução da CLI.  
**Escopo.** `tests/test_smoke.py` com 3 asserts (import, versão, main()).  
**Critérios de Aceite.**
 - [x] `pytest -q` passa localmente.
 - [x] Cobertura mínima exibida (`--cov`), sem exigência de threshold.
**Entregáveis.** Saída do `pytest` + arquivo de teste.  
**Notas.** Threshold será tratado futuramente.

---

### M1-SI-1.7 — Pre-commit com hooks básicos
**Objetivo.** Garantir padronização antes dos commits.  
**Escopo.** `.pre-commit-config.yaml` com hooks ruff/black/EOF/trailing-whitespace.  
**Critérios de Aceite.**
- [ ] Arquivo `.pre-commit-config.yaml` criado com os hooks citados.
- [ ] `pre-commit install` executado e evidenciado.
- [ ] Um commit demonstrando execução dos hooks.
**Entregáveis.** Log do pre-commit + diff dos arquivos.  
**Notas.** Bandit/pip-audit podem ser adicionados depois.

---

### M1-SI-1.8 — README (dev setup) e Badges básicos
**Objetivo.** Documentar setup local e exibir badges essenciais.  
**Escopo.** Atualizar README com instruções de dev e badges de MIT/Python.  
**Critérios de Aceite.**
- [x] README com seções: requisitos, instalação (`poetry install`), ativação, scripts.
- [x] Badges: Licença MIT e Python 3.11. (Badge de CI será adicionado na Issue #3.)
**Entregáveis.** Diff do README + renderização com badges.  
**Notas.** Manter PT-BR no README.

---

## Issue #2 — Configurar .gitignore e convenção de branches

### M1-SI-2.1 — .gitignore curado (Python/Poetry/IDE/OS)
**Objetivo.** Evitar arquivos indesejados no repositório.  
**Escopo.** Criar `.gitignore` cobrindo Python, Poetry (`.venv/`), VS Code, sistemas operacionais e diretórios temporários.  
**Critérios de Aceite.**
- [ ] `.gitignore` inclui: `__pycache__/`, `.pytest_cache/`, `.venv/`, `.mypy_cache/`, `.ruff_cache/`, `.vscode/`, `*.log`, `*.tmp`, `data/raw/` (se aplicável).
- [ ] Teste prático: criar um arquivo temporário e confirmar que é ignorado.
**Entregáveis.** Conteúdo do `.gitignore` + print de `git status` sem ruído.  
**Notas.** Não ignorar `data/processed/` se for fonte de artefatos versionados.

---

### M1-SI-2.2 — Definir convenção de branches (trunk-based)
**Objetivo.** Padronizar nomes e fluxo de branches.  
**Escopo.** Documento curto no `CONTRIBUTING.md`.  
**Critérios de Aceite.**
- [ ] Padrão `{type}/{slug}` com `type ∈ {feat, fix, docs, chore, refactor, test}`.
- [ ] Exemplo prático com 3 nomes válidos.
- [ ] Regra de PR curta: rebase ou squash; PR menor que 300 linhas.
**Entregáveis.** `CONTRIBUTING.md` atualizado.  
**Notas.** Alinha com Conventional Commits.

---

### M1-SI-2.3 — Conventional Commits (mensagens de commit)
**Objetivo.** Padronizar mensagens de commit.  
**Escopo.** Seção no `CONTRIBUTING.md`.  
**Critérios de Aceite.**
- [ ] Exemplos para `feat:`, `fix:`, `docs:`, `refactor:`, `test:`.
- [ ] Regra de escopo opcional (ex.: `feat(api): ...`).
- [ ] Referência à documentação oficial.
**Entregáveis.** Trecho do CONTRIBUTING + 1 commit de exemplo.  
**Notas.** Validadores de mensagem podem ser adicionados depois.

---

### M1-SI-2.4 — Proteções da branch `main` (documentadas)
**Objetivo.** Descrever política de proteção da `main`.  
**Escopo.** Checklist manual/documental para aplicar nas Settings.  
**Critérios de Aceite.**
- [ ] Checklist inclui: PR obrigatório, 1 reviewer, status checks do CI obrigatórios, proibição de force-push, exigir branches atualizadas antes do merge.
- [ ] Link/print das Settings (quando aplicadas).
**Entregáveis.** `docs/git-flow.md` com checklist.  
**Notas.** Aplicação efetiva pode ser feita depois; aqui é documentação.

---

### M1-SI-2.5 — Templates de PR e Issues
**Objetivo.** Padronizar abertura de PRs e Issues.  
**Escopo.** `.github/PULL_REQUEST_TEMPLATE.md` e `.github/ISSUE_TEMPLATE/bug.md` + `feature.md`.  
**Critérios de Aceite.**
- [ ] Templates criados com seções mínimas (descrição, evidências, checklist, riscos).
- [ ] PRs novos herdam o template automaticamente.
**Entregáveis.** Arquivos under `.github/` + print de PR com template.  
**Notas.** Simples e direto; sem exagero de campos.

---

### M1-SI-2.6 — Atualizar README com “Fluxo de Git”
**Objetivo.** Expor regras essenciais ao time/colaboradores.  
**Escopo.** Adicionar seção “Fluxo de Git” e links para `CONTRIBUTING.md` e `docs/git-flow.md`.  
**Critérios de Aceite.**
- [ ] Seção adicionada ao README.
- [ ] Links verificados funcionam.
**Entregáveis.** Diff do README.  
**Notas.** Manter linguagem clara e objetiva.

---

## Issue #3 — Criar pipeline inicial no GitHub Actions para lint/testes

### M1-SI-3.1 — Workflow base: setup Python + Poetry + cache
**Objetivo.** Garantir ambiente rápido e reprodutível na CI.  
**Escopo.** `.github/workflows/ci.yml` com `actions/setup-python`, cache do Poetry e dependências.  
**Critérios de Aceite.**
- [ ] Job `ci` roda em `ubuntu-latest` com Python 3.11.
- [ ] Cache de `~/.cache/pypoetry` e de `__pycache__`/pip funciona (hit em execuções subsequentes).
**Entregáveis.** Workflow YAML + print do log destacando cache hit.  
**Notas.** Usar `poetry install --no-interaction --no-root` quando apropriado.

---

### M1-SI-3.2 — Etapa Lint (ruff) e Format check (black)
**Objetivo.** Padronizar estilo na CI.  
**Escopo.** Steps para `ruff check .` e `black --check .`.  
**Critérios de Aceite.**
- [ ] Falhas de lint/format fazem o job falhar.
- [ ] Logs da CI mostram contagem de arquivos verificados.
**Entregáveis.** Log da execução.  
**Notas.** Estilos já definidos no `pyproject.toml` (Issue #1).

---

### M1-SI-3.3 — Type-check (mypy strict)
**Objetivo.** Rodar análise estática na CI.  
**Escopo.** Step `mypy .` com configuração strict.  
**Critérios de Aceite.**
- [ ] Job falha se houver erros de type.
- [ ] Log contém estatística de módulos verificados.
**Entregáveis.** Log da execução.  
**Notas.** Suppressions devem ser justificadas em código.

---

### M1-SI-3.4 — Testes (pytest) + cobertura
**Objetivo.** Executar testes e coletar cobertura.  
**Escopo.** Step `pytest -q --cov=src --cov-report=xml --cov-report=term`.  
**Critérios de Aceite.**
- [ ] CI conclui sem erros com pelo menos 1 teste executado.
- [ ] Artefato `coverage.xml` salvo (upload como artifact).
**Entregáveis.** Log do pytest + artifact anexo na execução.  
**Notas.** Threshold de 80% será apenas alerta (não bloqueia) por enquanto.

---

### M1-SI-3.5 — Triggers e Concurrency
**Objetivo.** Evitar filas e rodar nos momentos certos.  
**Escopo.** `on: [push, pull_request]` (main e branches), `concurrency: group: ci-${{ github.ref }}, cancel-in-progress: true`.  
**Critérios de Aceite.**
- [ ] PRs acionam a CI automaticamente.
- [ ] Novos pushes cancelam execução anterior do mesmo ref.
**Entregáveis.** YAML com as chaves referidas + print de execução cancelada por concurrency.  
**Notas.** Pode incluir `paths-ignore` para ignorar mudanças em docs.

---

### M1-SI-3.6 — Badge de CI no README
**Objetivo.** Exibir status da pipeline.  
**Escopo.** Adicionar badge do workflow ao topo do README.  
**Critérios de Aceite.**
- [ ] Badge renderiza corretamente e reflete status do último run.
- [ ] Link do badge aponta para a página do workflow.
**Entregáveis.** Diff do README + print do badge.  
**Notas.** Manter perto das demais badges (MIT/Python).

---

### M1-SI-3.7 — Artefatos e logs úteis
**Objetivo.** Facilitar investigação em caso de falha.  
**Escopo.** Upload de `coverage.xml`, relatório HTML de cobertura (se gerado) e logs relevantes.  
**Critérios de Aceite.**
- [ ] Artifacts disponíveis para download nos runs da CI.
- [ ] Tamanho dos artifacts mantido razoável (<10 MB).
**Entregáveis.** Lista de artifacts anexados.  
**Notas.** Evitar anexar `.venv`/caches.

---

### M1-SI-3.8 — Status checks obrigatórios (documentados)
**Objetivo.** Preparar para bloqueio de merge via status checks.  
**Escopo.** Documentar quais checks serão obrigatórios (lint, type, tests).  
**Critérios de Aceite.**
- [ ] Documento `docs/ci-status-checks.md` com os nomes exatos dos checks.
- [ ] Passo-a-passo de como ativar nas Settings do repositório.
**Entregáveis.** Documento citado.  
**Notas.** A ativação efetiva nas Settings pode ser feita depois.

---

## Padrões gerais (usar em todas as subissues)
- **DoR (Definition of Ready):** escopo claro, dependências listadas, estimativa e plano de teste local.
- **DoD (Definition of Done):** `ruff` e `black` sem erro, `mypy` sem erro, `pytest` ok, README/Docs atualizados quando tocados, evidências anexadas na issue/PR.
