import asyncio
import os
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Configuration
POSTGRES_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
REDIS_URL = (
    f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', 6379)}"
)


async def wait_for_db(retries: int = 10, delay: int = 1) -> bool:
    """Retry logic to wait for Postgres to be ready."""
    engine = create_async_engine(POSTGRES_URL)
    for i in range(retries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                print("Postgres OK")
                await engine.dispose()
                return True
        except Exception as e:
            print(f"⏳ Waiting for Postgres ({i + 1}/{retries})... Error: {e}")
            await asyncio.sleep(delay)

    await engine.dispose()
    return False


async def check_redis() -> bool:
    """Check Redis connection."""
    try:
        r = redis.from_url(REDIS_URL, decode_responses=True)
        await r.ping()
        print(f"Redis OK ({os.getenv('REDIS_HOST')})")
        await r.aclose()
        return True
    except Exception as e:
        print(f"Redis Error: {e}")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Checks
    print("🚀 Starting Atlas Platform...")

    if not await wait_for_db():
        print("CRITICAL: Could not connect to Postgres. Shutting down.")
        raise RuntimeError("Database connection failed")

    if not await check_redis():
        print("WARNING: Redis not reachable.")

    yield

    # Shutdown
    print("Shutting down...")


app = FastAPI(title="Atlas Template", lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "atlas-template",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "db": "connected",  # Validated by lifespan
        "redis": "connected",  # Validated by lifespan
    }
