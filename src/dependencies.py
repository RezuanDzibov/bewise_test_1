from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionLocal


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_http_client() -> AsyncClient:
    async with AsyncClient() as client:
        yield client
