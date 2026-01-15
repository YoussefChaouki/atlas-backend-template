from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from atlas_template.core.database import get_db
from atlas_template.repositories import notes as repo
from atlas_template.schemas.notes import NoteCreate, NoteResponse

router = APIRouter()


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    return await repo.create(db, note)


@router.get("/", response_model=list[NoteResponse])
async def read_notes(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await repo.get_all(db, skip, limit)


@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    db_note = await repo.get_by_id(db, note_id)
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return db_note
