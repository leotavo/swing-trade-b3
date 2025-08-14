# TECH_STACK — Swing Trade B3

## Núcleo
- Python 3.11 + Poetry
- FastAPI (API) + Uvicorn
- Pydantic v2 (validação)
- GitHub Actions (CI/CD)
- ruff (lint), pytest (testes), coverage (cobertura)
- python-dotenv (.env)

## Dados
- requests (HTTP)
- BRAPI (ou REST simples)
- yfinance (fallback) ou Alpha Vantage (chave)
- pandas + pyarrow (Parquet) — considerar Polars
- holidays (feriados BR), tzdata
- joblib / cron (GitHub Actions)

## EDA
- pandas/polars
- Jupyter/Quarto
- matplotlib + plotly

## Estratégia & Backtest
- pandas_ta (RSI, MACD, EMAs)
- vectorbt (ou backtrader)
- numpy

## IA (posterior)
- scikit-learn / xgboost
- MLflow (experimentos)
- DVC (dados)

## Observabilidade
- logging estruturado
- Prometheus + Grafana (ou Grafana Cloud)
- healthchecks.io / Telegram Bot API

## Segurança
- bandit (SAST), pip-audit (vulns), trufflehog (secrets)
- GitHub Environments/Secrets ou AWS Secrets Manager

## Notas de Licença
- vectorbt (AGPLv3). Alternativa: backtrader (licença mais permissiva).