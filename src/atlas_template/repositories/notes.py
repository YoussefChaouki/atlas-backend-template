from collections.abc import Sequence
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from atlas_template.models import Note


async def create(session: AsyncSession, note_in: Any) -> Note:
    """
    Crée une note.
    Accepte un objet Pydantic ou un dict.
    """
    data = note_in.model_dump() if hasattr(note_in, "model_dump") else note_in
    db_note = Note(**data)
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    return db_note


async def get_by_id(session: AsyncSession, note_id: int) -> Note | None:
    """Récupère une note par son ID."""
    result = await session.execute(select(Note).where(Note.id == note_id))
    return result.scalars().first()


async def get_all(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[Note]:
    """Récupère toutes les notes avec pagination."""
    result = await session.execute(select(Note).offset(skip).limit(limit))
    return result.scalars().all()


async def search_similar_notes(
    session: AsyncSession, embedding: list[float], limit: int = 5
) -> Sequence[Note]:
    """
    Cherche les notes les plus proches par distance cosinus (pgvector).
    """
    stmt = select(Note).order_by(Note.embedding.cosine_distance(embedding)).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_embedding(
    session: AsyncSession, note_id: int, embedding: list[float]
) -> None:
    """
    Met à jour uniquement le champ embedding d'une note.
    """
    stmt = update(Note).where(Note.id == note_id).values(embedding=embedding)
    await session.execute(stmt)
    await session.commit()
