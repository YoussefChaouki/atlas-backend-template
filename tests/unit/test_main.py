from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from atlas_template.main import app


def test_health_check():
    """
    Test le endpoint /health en simulant (mocking) les connexions DB et Redis.
    Cela permet au test de passer même si Docker n'est pas lancé.
    """
    # 1. On "patch" les fonctions de vérification pour qu'elles renvoient toujours True
    with (
        patch("atlas_template.main.wait_for_db", new_callable=AsyncMock) as mock_db,
        patch("atlas_template.main.check_redis", new_callable=AsyncMock) as mock_redis,
    ):
        # On force le succès des mocks
        mock_db.return_value = True
        mock_redis.return_value = True

        # 2. On lance le client de test
        # Note: TestClient déclenche le lifespan (démarrage de l'app)
        with TestClient(app) as client:
            response = client.get("/health")

            # 3. Vérifications
            assert response.status_code == 200
            data = response.json()

            # On vérifie les champs statiques
            assert data["status"] == "ok"
            assert data["service"] == "atlas-template"

            # On vérifie juste que les clés d'infra sont présentes (pas leur valeur exacte)
            assert "db" in data
            assert "redis" in data
            assert "environment" in data
