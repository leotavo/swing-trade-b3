# Milestone 2 — Coleta e Preparação de Dados

Subissues atômicas com critérios de aceite

> Contexto: M2 cobre 4 issues — **#4 Implementar conector API B3 (histórico)**, **#5 Rotina de limpeza e normalização dos dados**, **#6 Script de atualização diária automática**, **#7 Resiliência da coleta de dados da B3 (Mitigação de Risco)**.  
> Formato padrão por subissue: **Objetivo**, **Escopo**, **Critérios de Aceite**, **Entregáveis**, **Notas**.

> Roadmap: ver `docs/MILESTONES_ISSUES.md` (bloco M2).

---

## Issue #4 — Implementar conector API B3 (histórico)

### M2-SI-4.1 — Especificar fonte e contrato do conector

**Objetivo.** Definir a fonte de dados e o contrato do conector para OHLCV diários.  
**Escopo.** Documento curto com endpoints, limites, parâmetros e interface Python (funções públicas).  
**Critérios de Aceite.**

- [x] Interface definida (ex.: `fetch_daily(symbol: str, start: date, end: date) -> DataFrame`).
- [x] Campos padronizados: `date, symbol, open, high, low, close, volume` (dtypes e timezone UTC).
- [x] Padrão de erros: exceções específicas para HTTP, parsing e limites (429/5xx/timeouts).

**Entregáveis.** `docs/data-connector-spec.md` com contrato e limites.  
**Notas.** Fonte pode ser API oficial/serviço compatível; manter design desacoplado.

---

### M2-SI-4.2 — Cliente HTTP com timeout, backoff e user-agent

**Objetivo.** Garantir robustez básica de rede.  
**Escopo.** Implementar cliente com timeouts, retries exponenciais com jitter e user-agent identificável.  
**Critérios de Aceite.**

- [x] Timeout configurável (padrão ≤ 10s) e `max_retries` (padrão 3).
- [x] Backoff exponencial com jitter e tratamento de 429/5xx.
- [x] Logs estruturados por tentativa e motivo do retry.

**Entregáveis.** Código + exemplo de uso (snippet).  
**Notas.** Sem expor chaves em logs; respeitar termos de uso.

---

### M2-SI-4.3 — Parser e normalização para OHLCV diário

**Objetivo.** Transformar resposta da API em DataFrame padronizado.  
**Escopo.** Mapear campos, normalizar datas/timezone, ordenar e validar colunas/dtypes.  
**Critérios de Aceite.**

- [x] Colunas: `date` (datetime64[ns, UTC]), `symbol` (str), `open/high/low/close` (float64), `volume` (int64).
- [x] Ordenação crescente por `date`, sem duplicatas.
- [x] Linhas com valores inválidos (NaN/negativos) removidas com log de contagem.

**Entregáveis.** Função `to_ohlcv(df_raw) -> DataFrame` + testes de forma.  
**Notas.** Considerar feriados/ausência de pregão sem criar valores sintéticos.

---

### M2-SI-4.4 — Persistência em `data/raw/` (CSV/Parquet)

**Objetivo.** Armazenar dados brutos por símbolo e faixa de datas.  
**Escopo.** Escrever arquivo por `symbol` e `YYYY` ou intervalo solicitado.  
**Critérios de Aceite.**

- [x] Arquivos em `data/raw/{symbol}/YYYY.parquet` (ou `.csv`) com schema consistente.
- [x] Reexecução não duplica linhas (merge + dedupe por `(symbol,date)`).
- [x] Registro de caminho e tamanho final no log.

**Entregáveis.** Função de persistência + amostra de arquivo.  
**Notas.** Evitar commits de `data/raw/` (já ignorado no .gitignore).

---

### M2-SI-4.5 — CLI de coleta (símbolo e período)

**Objetivo.** Expor coleta via CLI para facilitar operação.  
**Escopo.** Comando `python -m swing_trade_b3 fetch --symbol PETR4 --start 2022-01-01 --end 2023-01-01`.  
**Critérios de Aceite.**

- [x] Exit code 0; imprime contagem de linhas, período e caminho salvo.
- [x] Valida parâmetros (datas válidas, símbolo não vazio).
- [x] Erros tratáveis retornam código ≠ 0 com mensagem clara.

**Entregáveis.** Help (`--help`) + exemplo de execução.  
**Notas.** Padronizar timezone e locale independentes do SO.

---

## Issue #5 — Rotina de limpeza e normalização dos dados

### M2-SI-5.1 — Especificar schema final (dataset processado)

**Objetivo.** Definir contrato do dataset processado.  
**Escopo.** Documentar colunas, dtypes, índices e ordenação.  
**Critérios de Aceite.**

- [x] Colunas mínimas: `date, symbol, open, high, low, close, volume`.
- [x] Dtypes e timezone formalizados; índice opcional (`date,symbol`).
- [x] Regras de missing/duplicatas explicitadas.

**Entregáveis.** `docs/data-schema.md` (seção dataset processado).  
**Notas.** Facilitar consumo posterior por backtest/estratégia.

---

### M2-SI-5.2 — Pipeline de limpeza e validação

**Objetivo.** Normalizar dados brutos para o schema final.  
**Escopo.** Remover duplicatas, tratar NaN, coerção de tipos, ordenação por data.  
**Critérios de Aceite.**

- [x] Saída sem valores nulos; datas estritamente crescentes por `symbol`.
- [x] Dtypes corretos e consistentes entre arquivos.
- [x] Relatório de qualidade (contagens removidas, range de datas) no log.

**Entregáveis.** Função `clean_and_validate(df_raw) -> DataFrame`.  
**Notas.** Evitar preenchimento artificial que masque problemas.

---

### M2-SI-5.3 — Persistência em `data/processed/`

**Objetivo.** Salvar dataset processado de forma idempotente.  
**Escopo.** Escrever em `data/processed/{symbol}.parquet` (ou particionado por ano).  
**Critérios de Aceite.**

- [x] Reexecuções não criam duplicatas (chave `(symbol,date)`).
- [x] Ordenação estável e compressão adequada (ex.: snappy/zstd).
- [x] Log da operação com tempo e linhas escritas.

**Entregáveis.** Função de persistência + exemplo de arquivo.  
**Notas.** Considerar tamanho/particionamento para múltiplos anos.

---

### M2-SI-5.4 — Testes de qualidade (unitários e de forma)

**Objetivo.** Garantir integridade pós-limpeza.  
**Escopo.** Testes para NaN=0, ordenação, dtypes e consistência de chaves.  
**Critérios de Aceite.**

- [x] `pytest -q` passa com asserts de qualidade principais.
- [x] Casos com dados problemáticos cobertos (linhas duplicadas, NaN, tipos errados).

**Entregáveis.** Arquivos `tests/test_data_cleaning.py` (ou similar).  
**Notas.** Usar fixtures mínimos e determinísticos.

---

## Issue #6 — Script de atualização diária automática

### M2-SI-6.1 — Atualização incremental por `symbol`

**Objetivo.** Baixar apenas o período novo desde a última data processada.  
**Escopo.** Ler última data em `data/processed/`, coletar delta e mesclar.  
**Critérios de Aceite.**

- [ ] Atualiza em < 5 minutos para até N símbolos (N definido no doc).
- [ ] Sem duplicatas e preserva ordenação.
- [ ] Saída e logs informam janela atualizada e contagens.

**Entregáveis.** CLI `update --symbol <SYM>` (ou lista) + logs.  
**Notas.** Considerar limites de rate da fonte.

---

### M2-SI-6.2 — Modo agendado (documentação)

**Objetivo.** Descrever agendamento diário confiável.  
**Escopo.** Guia para cron (Linux), Agendador de Tarefas (Windows) e GitHub Actions `schedule`.  
**Critérios de Aceite.**

- [ ] Documento com exemplos de configuração por plataforma.
- [ ] Variáveis de ambiente e segredos documentados com segurança.

**Entregáveis.** `docs/data-update-schedule.md`.  
**Notas.** Não commitar chaves; usar `.env`/Secrets.

---

### M2-SI-6.3 — Logging e medição de desempenho

**Objetivo.** Tornar a rotina observável.  
**Escopo.** Logs estruturados (nível/tempo/ação) e métricas simples (tempo total, linhas).  
**Critérios de Aceite.**

- [ ] Logs gravados em arquivo local com rotação simples.
- [ ] Métricas básicas emitidas (tempo/linhas/símbolos) ao final.

**Entregáveis.** Config de logging + exemplo de execução.  
**Notas.** Base para M9 (observabilidade).

---

## Issue #7 — Testar resiliência da coleta de dados da B3 (Mitigação de Risco)

### M2-SI-7.1 — Retries e tolerância a falhas controladas

**Objetivo.** Garantir robustez a falhas transitórias.  
**Escopo.** Retries com backoff/jitter e tratamento de timeouts/429/5xx.  
**Critérios de Aceite.**

- [ ] Parâmetros de retry configuráveis; erro final com mensagem clara após esgotar.
- [ ] Casos cobertos em testes com mocks (simular 429/5xx/timeout).

**Entregáveis.** Testes e logs de exemplo.  
**Notas.** Respeitar limites de uso.

---

### M2-SI-7.2 — Continuidade parcial e relatório de falhas

**Objetivo.** Evitar término do processo em falhas parciais.  
**Escopo.** Prosseguir com demais símbolos/intervalos e consolidar um relatório final.  
**Critérios de Aceite.**

- [ ] Execução não encerra em primeira falha; erros coletados e reportados ao final.
- [ ] Exit code 0 quando houver dados úteis salvos; ≠0 apenas se 0 sucesso.

**Entregáveis.** Resumo final (sucesso/falha por símbolo) + resumo JSON opcional via `--json-summary` (ex.: `docs/summary-example.json`).  
**Notas.** JSON inclui metadados da execução (`run/symbols/summary`) para integrações/CI; acordar política com o time.

---

### M2-SI-7.3 — Limitação de taxa (throttling)

**Objetivo.** Prevenir rate-limit e banimentos.  
**Escopo.** Throttle simples (por segundo/minuto) com randomização leve.  
**Critérios de Aceite.**

- [ ] Parâmetros de taxa documentados; efeitos visíveis nos logs.
- [ ] Teste que valida a aplicação do intervalo entre requisições.

**Entregáveis.** Implementação + teste unitário mínimo.  
**Notas.** Ajustar valores conforme fornecedor de dados.

---

### M2-SI-7.4 — Testes de caos (simulados) para rede

**Objetivo.** Validar comportamento sob condições adversas.  
**Escopo.** Testes que injetam exceções, latência e respostas malformadas.  
**Critérios de Aceite.**

- [ ] Testes cobrem timeouts, respostas inválidas e quedas aleatórias.
- [ ] Logs e resultado final coerentes com política de continuidade.

**Entregáveis.** Conjunto de testes com fixtures/mocks.  
**Notas.** Sem testar chamadas reais fora do horário de pregão.

---

## Padrões gerais (usar em todas as subissues)

- **DoR (Definition of Ready):** escopo claro, dependências listadas, estimativa e plano de teste local.  
- **DoD (Definition of Done):** `ruff` e `black` sem erro, `mypy` sem erro, `pytest` ok, README/Docs atualizados quando tocados, evidências anexadas na issue/PR.
- **Observabilidade:** preferir logs estruturados com `--log-json` quando aplicável e emitir resumo em `--json-summary` para integrações/CI.
