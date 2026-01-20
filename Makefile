.PHONY: install run test test-live lint format docker-build up down rebuild logs logs-api db-shell db-tables mig-up mig-rev

install:
	pip install -e ".[dev]"

run:
	uvicorn atlas_template.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest tests/ -v

test-live:
	# Lance uniquement les tests d'intégration
	pytest tests/integration -v

lint:
	ruff check --fix .
	mypy src/

format:
	ruff format .

# --- Docker Operations ---

up:
	docker compose up -d

down:
	docker compose down

rebuild:
	# Force la reconstruction
	docker compose down
	docker compose up -d --build

logs:
	# Logs de tous les conteneurs
	docker compose logs -f

logs-api:
	# Logs spécifiques de l'API
	docker compose logs -f api

# --- Database Tools  ---

db-shell:
	# Connecte directement au PSQL dans le conteneur
	docker compose exec db psql -U atlas -d atlas_db

db-tables:
	# Affiche la liste des tables
	docker compose exec db psql -U atlas -d atlas_db -c "\dt"

# --- Migrations (Alembic Local) ---

mig-rev:
	# Usage: make mig-rev m="message de migration"
	POSTGRES_HOST=localhost alembic revision --autogenerate -m "$(m)"

mig-up:
	POSTGRES_HOST=localhost alembic upgrade head
