FROM python:3.11-slim

WORKDIR /app

# Optimisation Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# 1. Installation des dépendances (Cache optimisé)
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# 2. Copie du code source
COPY src/ ./src/

# Sécurité : User non-root
RUN useradd -m atlas
USER atlas

EXPOSE 8000
CMD ["uvicorn", "atlas_template.main:app", "--host", "0.0.0.0", "--port", "8000"]