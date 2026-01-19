from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from atlas_template.core.database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    content: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    # DateTime avec Timezone obligatoire pour apps sérieuses
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
