import httpx
import pytest


@pytest.mark.asyncio
async def test_search_endpoint_live(wait_for_api):
    """
    Test live contre Docker.
    Suppositions:
    - L'API tourne.
    - La DB contient des données (via backfill ou créé ici).
    - AI Service est en mode 'mock' (pas de clé) ou réel.
    """
    base_url = "http://localhost:8000/api/v1/notes"

    # Même si la DB est vide, ça doit renvoyer 200 et liste vide (ou remplie par backfill)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/search", json={"query": "strategy plan", "k": 3}
        )

        assert response.status_code == 200, f"Search failed: {response.text}"
        data = response.json()
        assert isinstance(data, list)
