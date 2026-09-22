.PHONY: help install install-dev lint format fix typecheck test audit check run run-dev

APP_HOST ?= 0.0.0.0
APP_PORT ?= 8000

help:
	@echo "Available commands:"
	@echo "  install"
	@echo "  install-dev"
	@echo "  lint"
	@echo "  format"
	@echo "  fix"
	@echo "  typecheck"
	@echo "  test"
	@echo "  audit"
	@echo "  check"
	@echo "  run"
	@echo "  run-dev"

install:
	poetry install --without dev

install-dev:
	poetry install

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

fix:
	poetry run ruff check . --fix
	poetry run ruff format .

typecheck:
	poetry run mypy src/

audit:
	poetry run bandit -r src/

test:
	poetry run pytest --cov=src --cov-report=term-missing

check: lint typecheck audit test

run:
	poetry run uvicorn src.main:app --host $(APP_HOST) --port $(APP_PORT)

run-dev:
	poetry run uvicorn src.main:app --host $(APP_HOST) --port $(APP_PORT) --reload
