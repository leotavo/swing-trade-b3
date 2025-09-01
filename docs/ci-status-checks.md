# Status Checks obrigatórios (CI)

Este repositório usa um workflow do GitHub Actions chamado "CI" com um job chamado `ci (3.11)`.

Para habilitar status checks obrigatórios na branch `main`:

1) Vá em Settings → Branches → Add rule (ou edite a regra existente para `main`).
2) Marque "Require status checks to pass before merging".
3) Em "Status checks that are required", selecione:
   - `ci (3.11)`
4) Marque também "Require branches to be up to date before merging".
5) Salve.

Observação: O nome do check corresponde ao nome do job definido no workflow (neste caso, `ci (3.11)`).
