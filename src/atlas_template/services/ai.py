import os

from openai import AsyncOpenAI


async def get_embedding(text: str) -> list[float]:
    """
    Génère un embedding via OpenAI (text-embedding-3-small).
    Lazy instantiation du client pour éviter les erreurs au boot si pas de clé.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    client = AsyncOpenAI(api_key=api_key)

    # Normalisation basique recommandée par OpenAI
    clean_text = text.replace("\n", " ")

    response = await client.embeddings.create(
        input=[clean_text], model="text-embedding-3-small"
    )

    return response.data[0].embedding
