# Contribuição

Este projeto segue um fluxo trunk‑based. A branch padrão é `main` e os trabalhos acontecem em branches curtas, focadas e de curta duração.

## Convenção de branches

- Padrão: `{type}/{slug}`
- `type ∈ {feat, fix, docs, chore, refactor, test}`
- `slug`: palavras em kebab‑case que descrevem o objetivo

Exemplos válidos

- `feat/data-connector-b3`
- `fix/ci-windows-paths`
- `docs/m1-subissues-atomic`

## Regras de Pull Request

- Merge: use rebase ou squash (evite merge commits).
- Tamanho: mantenha PRs pequenos (idealmente < 300 linhas alteradas).
- Qualidade: rode pre-commit, lint, typecheck e testes antes de abrir o PR.
- Descrição: inclua contexto, escopo e referência a issues (ex.: `Closes #123`).

## Mensagens de commit (Conventional Commits)

Siga o padrão https://www.conventionalcommits.org/.

- Tipos comuns: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.
- Escopo opcional: `type(scope): descrição` (ex.: `feat(api): adicionar endpoint de sinais`).
- Descrição: em português claro, no imperativo, concisa.
- Breaking change: use `!` após o tipo/escopo (ex.: `feat(core)!: altera contrato de sinais`)
  e detalhe no corpo: `BREAKING CHANGE: ...`.

Exemplos

- `feat(strategy): implementar RSI + MACD`
- `fix(ci): corrigir path no Windows`
- `docs(contributing): adicionar guia de Conventional Commits`
- `refactor(backtest): extrair cálculo de métricas`
- `test(data): cobrir limpeza de nulos`
- `chore(pre-commit): atualizar hooks`

## Dicas

- Atualize a branch com `rebase` para manter o histórico limpo.
- Prefira vários PRs pequenos a um PR grande.

## Releases e tags

- Use apenas tags semânticas no formato `vMAJOR.MINOR.PATCH` (ex.: `v0.2.0`).
- Publique um Release no GitHub reutilizando notas em `docs/releases/`.
- Referencie Issues e PRs no corpo do Release (ex.: "Closes #2").
- Evite tags por issue (ex.: `issue-2`); esse padrão não será mais usado.
