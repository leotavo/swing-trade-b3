.PHONY: dev run test

dev:
	poetry install --with dev
	pre-commit install

run:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest
