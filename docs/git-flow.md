# Fluxo de Git e Proteção da Branch main

Este documento descreve a política recomendada de fluxo de Git e as proteções da branch `main` para este repositório.

## Fluxo (trunk‑based)

- Branch padrão: `main`.
- Trabalhos em branches curtas: `{type}/{slug}` (ver `CONTRIBUTING.md`).
- Abra PR para integrar em `main`; evite commits diretos.
- Use rebase/squash no merge.

## Proteções recomendadas para `main` (Branch protection rule)

Marque as opções abaixo ao criar/editar a regra em Settings › Branches:

- Requer pull request antes do merge (Require a pull request before merging)
  - Required approvals: 1
  - Dismiss stale pull request approvals when new commits are pushed (opcional)
- Require status checks to pass before merging
  - Status checks obrigatórios: "CI" (workflow do GitHub Actions; definir após a Issue #3)
  - Require branches to be up to date before merging
- Restrict who can push to matching branches
  - Bloqueia force‑push na `main` (somente via PR)

Link direto para configuração da regra de proteção:

- https://github.com/leotavo/swing-trade-b3/settings/branches

## Passo a passo (GitHub UI)

1) Acesse Settings › Branches
2) Clique em "Add rule"
3) Branch name pattern: `main`
4) Habilite as opções conforme a seção acima
5) Salve

Observação: Os nomes exatos dos status checks serão definidos na Issue #3 (CI) e documentados em `docs/ci-status-checks.md`.

## Releases e versionamento

- Adoção de versionamento semântico: crie tags no formato `vMAJOR.MINOR.PATCH`.
- Crie o Release no GitHub para cada tag semântica e inclua notas relevantes (Issues/PRs).
- Não usar tags por issue (ex.: `issue-123`). Historicamente pode haver tags assim no passado, mas o padrão atual é apenas semântico.
