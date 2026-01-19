# Utiliser une image python officielle légère
FROM python:3.11-slim

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/app/src

WORKDIR /app

COPY pyproject.toml .

# Installation des dépendances lourdes en amont.
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn[standard] sqlalchemy asyncpg alembic pydantic pydantic-settings openai pgvector

COPY src/ src/

# Installation du package lui-même (pour résoudre les imports 'atlas_template')
RUN pip install .

# Création utilisateur non-root
RUN useradd -m atlas
USER atlas

EXPOSE 8000

# Lancement
CMD ["uvicorn", "atlas_template.main:app", "--host", "0.0.0.0", "--port", "8000"]
