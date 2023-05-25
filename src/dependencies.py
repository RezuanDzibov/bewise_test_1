from typing import AsyncGenerator

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import SessionLocal
from core.settings import get_settings

settings = get_settings()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_http_client() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(timeout=settings.QUESTIONS_API_TIMEOUT) as client:
        yield client
