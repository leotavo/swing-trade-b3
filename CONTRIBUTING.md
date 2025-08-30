# Guia de Contribuição

Obrigado por considerar contribuir com o projeto **Swing Trade B3**. Este documento descreve o fluxo de trabalho e as expectativas para colaborar de forma organizada.

## Ambiente de Desenvolvimento

Instale as dependências utilizando [Poetry](https://python-poetry.org/):

```bash
poetry install
```

## Fluxo de Branches
- O ramo principal é `main` e deve sempre representar um estado estável do projeto.
- Crie branches a partir de `main` com prefixos descritivos, por exemplo:
  - `feat/` para novas funcionalidades
  - `fix/` para correções de bugs
  - `docs/` para ajustes de documentação
- Abra Pull Requests para unir alterações em `main`. Solicite revisão antes de fazer o merge.
- Os nomes de branch são validados automaticamente via CI e devem seguir o padrão acima.
  Caso a verificação falhe, renomeie a branch para começar com um dos prefixos permitidos (ex.: `fix/codex-add-branch-name-validation-workflow`).

## Padrões de Commit
- Utilize o padrão [Conventional Commits](https://www.conventionalcommits.org/).
- Exemplos: `feat: adiciona conector B3`, `fix: corrige cálculo de RSI`, `docs: atualiza README`.
- Escreva mensagens curtas e no imperativo.

## Testes e Qualidade
- Execute os linters e testes antes de enviar um PR:
  ```bash
  pre-commit run --files <arquivos_modificados>
  pytest
  ```
- Garanta que todos os testes estejam passando e que o código siga as regras de estilo.

## Dúvidas
Abra uma issue caso tenha qualquer dúvida ou sugestão.
