"""Database configuration and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from atlas_template.core.config import settings
from atlas_template.models.base import Base

# Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Session Factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection for database sessions."""
    async with AsyncSessionLocal() as session:
        yield session


# Re-export Base for migrations compatibility
__all__ = ["Base", "engine", "AsyncSessionLocal", "get_db"]
