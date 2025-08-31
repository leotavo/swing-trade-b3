.PHONY: dev run test lint

dev:
	poetry install --with dev
	poetry run pre-commit install

run:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest --cov=app --cov=swing_trade

lint:
	poetry run pre-commit run --all-files
