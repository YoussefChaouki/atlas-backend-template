from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=100, description="Titre (3-100 chars)"
    )
    content: str = Field(..., min_length=5, description="Contenu explicite")
    is_active: bool = True


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class NoteResponse(NoteBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Texte à rechercher")
    k: int = Field(5, ge=1, le=50, description="Nombre de résultats max")
