from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from atlas_template.core.config import settings

# 1. Moteur Async
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 2. Factory de session
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# 3. Classe de base (SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass


# 4. Dependency Injection (Typée)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
