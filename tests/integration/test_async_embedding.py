import asyncio

import httpx
import pytest


@pytest.mark.asyncio
async def test_create_note_triggers_embedding(wait_for_api):
    """
    Test E2E : Crée une note et attend que l'embedding apparaisse en DB.
    Utilise le mode 'Mock' du service AI (donc pas d'appel OpenAI réel).
    """
    base_url = "http://localhost:8000/api/v1/notes"

    async with httpx.AsyncClient() as client:
        payload = {
            "title": "Async Test Note",
            "content": "This note should be processed in background.",
            "is_active": True,
        }
        response = await client.post(f"{base_url}/", json=payload)
        assert response.status_code == 201
        note_id = response.json()["id"]

    max_retries = 10
    found = False

    async with httpx.AsyncClient() as client:
        for _ in range(max_retries):
            await asyncio.sleep(0.5)

            search_res = await client.post(
                f"{base_url}/search", json={"query": "Async Test Note", "k": 1}
            )

            if search_res.status_code == 200:
                results = search_res.json()
                if any(n["id"] == note_id for n in results):
                    found = True
                    break

    assert found, f"Note {note_id} was not indexed/embedded after {max_retries * 0.5}s"
