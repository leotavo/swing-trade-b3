# Data Connector Spec — B3 (Histórico)

Objetivo: definir a fonte, contrato e limites do conector de dados históricos diários (OHLCV) para ativos da B3.

Fonte de dados adotada (inicial): brapi.dev (serviço público compatível com B3). Mantemos o design desacoplado para permitir troca de provedor sem quebrar a interface pública.

Provedor: brapi.dev

- Endpoint: `GET https://brapi.dev/api/quote/{symbol}`
- Parâmetros relevantes:
  - `interval=1d` (obrigatório para diário)
  - `range` OU janela específica (ver notas). Exemplos de `range`: `1mo`, `3mo`, `6mo`, `1y`, `5y`, `max`.
  - Alguns ambientes do brapi suportam `start`/`end` no formato `YYYY-MM-DD`. Caso indisponível, o conector faz paginação por janelas de `range` até cobrir `[start, end]`.
- Resposta: campo `historicalDataPrice` (lista) com itens `{date, open, high, low, close, volume, adjustedClose}`.
  - `date` é epoch (segundos) UTC.

Contrato público (Python)

- Função: `fetch_daily(symbol: str, start: date, end: date) -> pandas.DataFrame`
- Colunas padronizadas (e tipos):
  - `date`: `datetime64[ns, UTC]`
  - `symbol`: `str`
  - `open`, `high`, `low`, `close`: `float64`
  - `volume`: `int64`
  - Observações: sem duplicatas, ordenado ascendente por `date`.
- Erros padronizados:
  - `NetworkError`: problemas de rede/timeout.
  - `RateLimitError`: HTTP 429 ou política do provedor.
  - `ServerError`: HTTP 5xx.
  - `ParseError`: resposta malformada ou inesperada.

Cliente HTTP

- Timeout padrão: 10s (configurável por parâmetro/env `HTTP_TIMEOUT`)
- Retries com backoff exponencial + jitter para 429 e 5xx (padrão: `max_retries=3`)
- `User-Agent`: `swing-trade-b3/<version> (+github.com/leotavo/swing-trade-b3)`
- Logs: 1 linha por tentativa (método, url resumido, status/motivo, tentativa/limite, `sleep` aplicado)

Normalização

- Converte `date` (epoch) para `datetime` timezone UTC.
- Preenche `symbol` com o ticker solicitado.
- Validações: remove linhas com NaN/valores negativos em `open/high/low/close/volume`.
- Ordena por `date` ascendente e remove duplicatas por `(symbol, date)`.

Persistência de dados brutos

- Caminho: `data/raw/{symbol}/YYYY.csv` ou `YYYY.parquet`.
- Formato selecionável via CLI: `--format csv|parquet` (padrão: csv).
- Compressão Parquet opcional: `--compression snappy|zstd` (padrão: none).
- Sem duplicatas por `(symbol, date)` em reexecuções; ordenação estável.
- Schema consistente com as colunas padronizadas.

Limites e notas

- Rate limit do brapi.dev pode variar; sem chave, use baixa taxa (ex.: ≤ 5 req/s) e reduza sob 429.
- Provedor pode alterar campos/contratos; isolamos parsing em módulo próprio.
- Este conector não cria dados sintéticos em feriados/dias sem pregão.

Exemplo de uso (CLI)

```bash

python -m swing_trade_b3 fetch --symbol PETR4 --start 2023-01-01 --end 2024-01-01 --format parquet --compression snappy --throttle 0.2
python -m swing_trade_b3 fetch --symbol PETR4 VALE3 --start 2023-01-01 --end 2024-01-01 --symbols-file symbols.txt
python -m swing_trade_b3 fetch --symbol PETR4 --start 2023-01-01 --end 2024-01-01 --json-summary out/summary.json
python -m swing_trade_b3 fetch --symbol PETR4 --start 2023-01-01 --end 2024-01-01 --log-json  # logs estruturados (JSON)

```bash
```bash

Resumo JSON (opcional)

- Habilite com `--json-summary PATH` (ou `-` para stdout).
- Contém metadados da execução (janela, formato/compressão, throttle, force_max), status por símbolo (linhas, datas, arquivos, range_used) e totais agregados.
- Útil para integrações/CI sem depender de parse de textos.

Logging estruturado (opcional)

- Habilite com `--log-json` para emitir logs em JSON no stdout.
- Inclui campos de contexto (logger, nível, tempo, mensagem) e extras (ex.: attempt/status/url em HTTP; bytes/rows/path na persistência).
