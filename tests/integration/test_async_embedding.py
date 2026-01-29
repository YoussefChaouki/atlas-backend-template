"""Integration test for async embedding generation."""

import asyncio
import os
import uuid

import asyncpg
import httpx
import pytest


def _build_test_dsn() -> str:
    """Build DSN from environment variables."""
    return (
        f"postgresql://{os.getenv('POSTGRES_USER', 'atlas')}:"
        f"{os.getenv('POSTGRES_PASSWORD', 'atlas_password')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB', 'atlas_db')}"
    )


@pytest.mark.asyncio
async def test_create_note_triggers_embedding(wait_for_api):
    """
    Test E2E : Crée une note et attend que l'embedding apparaisse en DB.
    Utilise le mode 'Mock' du service AI (donc pas d'appel OpenAI réel).

    IMPORTANT:
    - On NE teste PAS via /search (ranking/approx peut ne pas renvoyer la note).
    - On vérifie directement en DB: embedding IS NOT NULL.
    """
    base_url = "http://localhost:8000/api/v1/notes"
    unique_title = f"Async Test Note {uuid.uuid4()}"

    # 1. Create note via API
    async with httpx.AsyncClient() as client:
        payload = {
            "title": unique_title,
            "content": "This note should be processed in background.",
            "is_active": True,
        }
        response = await client.post(f"{base_url}/", json=payload)
        assert response.status_code == 201, response.text
        note_id = response.json()["id"]

    # 2. Poll database for embedding
    max_retries = 20
    poll_interval_s = 0.5

    dsn = (
        os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL") or _build_test_dsn()
    )
    # asyncpg doesn't like the "+asyncpg" suffix from SQLAlchemy URLs
    dsn = dsn.replace("postgresql+asyncpg://", "postgresql://")

    found = False
    conn = None

    try:
        # Connect to database (asyncpg.connect returns a coroutine, not a context manager)
        conn = await asyncpg.connect(dsn)

        for _attempt in range(max_retries):
            await asyncio.sleep(poll_interval_s)

            row = await conn.fetchrow(
                "SELECT embedding IS NOT NULL AS has_embedding FROM notes WHERE id = $1",
                note_id,
            )

            if row and row["has_embedding"]:
                found = True
                break

    finally:
        if conn:
            await conn.close()

    assert found, (
        f"Note {note_id} embedding was not generated after "
        f"{max_retries * poll_interval_s}s"
    )
