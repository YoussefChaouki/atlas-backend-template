import asyncio
import os
import random
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from atlas_template.models import Note

# URL localhost pour script externe
DATABASE_URL = "postgresql+asyncpg://atlas:atlas_password@localhost:5432/atlas_db"


async def main():
    print("Starting Backfill...")
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        # 1. Nettoyage des données existantes
        await session.execute(text("TRUNCATE TABLE notes RESTART IDENTITY;"))

        # 2. Création de données dummy avec vecteurs
        print("Creating notes with dummy embeddings...")

        notes_data = [
            ("Project Atlas Plan", "Strategy for 2026 AI Engineering path."),
            ("Grocery List", "Milk, eggs, bread, coffee."),
            ("Python Tips", "Use async/await for I/O bound tasks."),
        ]

        for title, content in notes_data:
            fake_embedding = [random.random() for _ in range(1536)]

            note = Note(title=title, content=content, embedding=fake_embedding)
            session.add(note)

        await session.commit()
        print(f"Inserted {len(notes_data)} notes with embeddings.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
