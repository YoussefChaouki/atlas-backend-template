"""Pydantic schemas for Note entity."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    """Base schema for Note with common fields."""

    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Note title (3-200 chars)",
    )
    content: str = Field(
        ...,
        min_length=5,
        description="Note content",
    )
    is_active: bool = Field(default=True)


class NoteCreate(NoteBase):
    """Schema for creating a new Note."""

    pass


class NoteUpdate(BaseModel):
    """Schema for updating a Note (all fields optional)."""

    title: str | None = Field(None, min_length=3, max_length=200)
    content: str | None = Field(None, min_length=5)
    is_active: bool | None = None


class NoteRead(NoteBase):
    """Schema for reading a Note with all fields."""

    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class NoteResponse(NoteBase):
    """Schema for API responses (lighter than NoteRead)."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteSearchRequest(BaseModel):
    """Schema for semantic search requests."""

    query: str = Field(
        ...,
        min_length=1,
        description="Search query text",
    )
    k: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Number of results to return",
    )
