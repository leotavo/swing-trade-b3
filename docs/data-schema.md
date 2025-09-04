# Data Schema — Dataset Processado

Objetivo: definir o contrato do dataset processado para consumo por análises, backtests e estratégias.

Escopo: dados diários (OHLCV) por símbolo da B3, limpos e normalizados a partir de `data/raw/`.

Colunas e tipos
- `date` (datetime64[ns, UTC]): data do pregão em UTC, sem hora relevante, ordenada ascendente por símbolo.
- `symbol` (string): ticker do ativo (ex.: `PETR4`).
- `open` (float64)
- `high` (float64)
- `low` (float64)
- `close` (float64)
- `volume` (int64): quantidade negociada no dia.

Regras
- Sem valores nulos.
- Sem valores negativos em `open/high/low/close/volume`.
- Sem duplicatas por chave `(symbol, date)`.
- Ordenação estritamente crescente por `date` dentro de cada `symbol`.
- Timezone em UTC.

Persistência
- Caminho: `data/processed/{symbol}.parquet` (recomendado) ou `.csv` (opcional).
- Idempotente: reexecuções mesclam e removem duplicatas, preservando ordenação e tipos.
- Compressão Parquet recomendada: `snappy`.

CLI
- Use `python -m swing_trade_b3 process` para converter `data/raw/` em `data/processed/`.
- Exemplos no README (seção "Processamento de dados (CLI)").

Funções públicas (Python)
- `clean_and_validate(df_raw: pandas.DataFrame) -> pandas.DataFrame`
  - Aplica normalização, validações e garante o schema final.
- `save_processed(symbol: str, df: pandas.DataFrame, base_dir: str|Path = "data/processed", fmt: str = "parquet", compression: Optional[str] = "snappy") -> Path`
  - Salva o dataset processado de forma idempotente.

Notas
- O dataset processado não cria dias sintéticos para feriados ou ausências de pregão.
- Quando necessário, campos adicionais podem ser adicionados em versões posteriores; mudanças breaking serão versionadas e documentadas.
