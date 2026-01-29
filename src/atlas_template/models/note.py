"""Note model definition."""

from pgvector.sqlalchemy import Vector
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from atlas_template.models.base import Base, TimestampMixin


class Note(Base, TimestampMixin):
    """Note entity with vector embedding support."""

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)

    def __repr__(self) -> str:
        return f"<Note(id={self.id}, title='{self.title[:20]}...')>"
