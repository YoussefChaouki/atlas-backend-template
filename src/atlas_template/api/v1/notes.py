from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from atlas_template.core.database import get_db
from atlas_template.repositories import notes as repo
from atlas_template.schemas.notes import (
    NoteCreate,
    NoteRead,
    NoteResponse,
    NoteSearchRequest,
)
from atlas_template.services import ai, embeddings

router = APIRouter()


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    new_note = await repo.create(db, note)

    background_tasks.add_task(embeddings.process_note_embedding, new_note.id)

    return new_note


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


@router.post("/search", response_model=list[NoteRead])
async def search_notes(
    search_req: NoteSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Recherche sémantique.
    """
    try:
        query_vector = await ai.get_embedding(search_req.query)
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"AI Service Error: {str(e)}"
        ) from e

    results = await repo.search_similar_notes(
        db, embedding=query_vector, limit=search_req.k
    )

    return results
