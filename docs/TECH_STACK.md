# TECH_STACK - Swing Trade B3

Legenda de status: [x] Entregue | [ ] Planejado

## Núcleo

- [x] Python 3.11 + Poetry
- [x] FastAPI (API) + Uvicorn
- [x] Pydantic v2 (validação)
- [x] GitHub Actions (CI/CD)
- [x] ruff (lint), black (format), mypy (tipagem), pytest (testes), coverage (cobertura)
- [ ] python-dotenv (.env)

## Dados

- [x] requests (HTTP)
- [x] brapi.dev (B3, OHLCV diário)
- [x] yfinance (fallback) ou Alpha Vantage (chave)
- [x] pandas + pyarrow (Parquet) — considerar Polars
- [ ] holidays (feriados BR), tzdata
- [ ] joblib / cron (GitHub Actions)

## EDA

- [ ] pandas/polars
- [ ] Jupyter/Quarto
- [ ] matplotlib + plotly

## Estratégia & Backtest

- [ ] pandas_ta (RSI, MACD, EMAs)
- [ ] vectorbt (ou backtrader)
- [ ] numpy

## Otimização

- [ ] Optuna (ou GridSearchCV do scikit-learn)

## IA (posterior)

- [ ] scikit-learn / xgboost
- [ ] MLflow (experimentos)
- [ ] DVC (dados)

## Paper Trading

- [ ] API de corretora com modo simulado (ex: MetaTrader5)

## Observabilidade

- [x] Logging estruturado (JSON via CLI)
- [ ] Streamlit (dashboard local)
- [ ] Prometheus + Grafana (ou Grafana Cloud)
- [ ] healthchecks.io / Telegram Bot API

## Segurança

- [x] bandit (SAST), pip-audit (vulns)
- [ ] trufflehog (secrets)
- [x] GitHub Secrets/Environments (CI)
- [ ] AWS Secrets Manager (opcional)

## Notas de Licença

- vectorbt (AGPLv3). Alternativa: backtrader (licença mais permissiva).
