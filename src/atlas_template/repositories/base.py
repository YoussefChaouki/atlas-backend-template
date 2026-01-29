"""Generic repository base class for CRUD operations."""

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from atlas_template.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations.

    Usage:
        class NoteRepository(BaseRepository[Note]):
            def __init__(self):
                super().__init__(Note)
    """

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def create(self, session: AsyncSession, obj_in: Any) -> ModelType:
        """Create a new record."""
        data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in
        db_obj = self.model(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, session: AsyncSession, id: int) -> ModelType | None:
        """Get a record by ID."""
        result = await session.execute(
            select(self.model).where(self.model.id == id)  # type: ignore[attr-defined]
        )
        return result.scalars().first()

    async def get_all(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        """Get all records with pagination."""
        result = await session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: Any,
    ) -> ModelType:
        """Update a record."""
        update_data = (
            obj_in.model_dump(exclude_unset=True)
            if hasattr(obj_in, "model_dump")
            else obj_in
        )
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, db_obj: ModelType) -> None:
        """Delete a record."""
        await session.delete(db_obj)
        await session.commit()
