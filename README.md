# Atlas Backend Template (v0.1.0)

Production-ready FastAPI template with Async SQLAlchemy, Pgvector, and Background Tasks.

## 🚀 Quickstart (5 min)

1. **Pré-requis** : Docker, Python 3.11+, Make.

2. **Installation** :
   ```bash
   cp .env.example .env
   # Remplir .env (OPENAI_API_KEY optionnel pour dev local si mock activé)
   make install
   pre-commit install
