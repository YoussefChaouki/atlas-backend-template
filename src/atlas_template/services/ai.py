import os
import random

from openai import AsyncOpenAI


async def get_embedding(text: str) -> list[float]:
    """
    Génère un embedding via OpenAI.
    Si OPENAI_API_KEY est absente ou vaut 'mock', retourne un vecteur aléatoire (DEV/TEST mode).
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key.lower() == "mock":
        return [random.random() for _ in range(1536)]

    client = AsyncOpenAI(api_key=api_key)
    text = text.replace("\n", " ")

    try:
        response = await client.embeddings.create(
            input=[text], model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"OpenAI Error: {e}")
        raise e
