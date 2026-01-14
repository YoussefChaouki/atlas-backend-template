.PHONY: install run test lint format docker-build

install:
	pip install -e ".[dev]"

run:
	uvicorn atlas_template.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest tests/ -v

lint:
	ruff check .
	mypy src/

format:
	ruff format .

docker-build:
	docker build -t atlas-template .