from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from atlas_template.models import Note
from atlas_template.schemas.notes import NoteCreate


async def create(db: AsyncSession, note_in: NoteCreate) -> Note:
    """Crée une note en base."""
    db_note = Note(**note_in.model_dump())
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Note]:
    """Récupère la liste paginée."""
    result = await db.execute(select(Note).offset(skip).limit(limit))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, note_id: int) -> Note | None:
    """Récupère une note par son ID."""
    result = await db.execute(select(Note).where(Note.id == note_id))
    return result.scalar_one_or_none()
