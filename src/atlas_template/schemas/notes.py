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


class NoteResponse(NoteBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
