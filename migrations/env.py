import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path
from typing import Any, cast

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Fix Path pour src-layout
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# --- IMPORT MODELS ---
import atlas_template.models  # noqa: F401
from atlas_template.core.config import settings
from atlas_template.core.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # 1. Récupère la section config (ou vide si None)
    section = config.get_section(config.config_ini_section) or {}

    # 2. On "cast" brutalement en Dict[str, Any] pour calmer Mypy
    # Mypy refuse qu'on passe un Dict[str, str] là où on attend Dict[str, Any]
    configuration = cast(dict[str, Any], section)

    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
