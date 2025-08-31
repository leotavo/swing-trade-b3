.PHONY: dev run test lint typecheck

dev:
	poetry install --with dev
	pre-commit install

run:
	poetry run uvicorn app.main:app --reload

test:
	PYTHONPATH=. poetry run pytest --cov=app --cov=swing_trade

lint:
	pre-commit run --all-files


typecheck:
	poetry run mypy --strict .
