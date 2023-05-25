import asyncio
from asyncio import AbstractEventLoop
from datetime import datetime
from typing import Generator, AsyncGenerator

import pytest
from faker import Faker
from httpx import AsyncClient
from pytest_asyncio.plugin import SubRequest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.settings import get_settings
from main import app
from models import Base
from schemas import QuestionSchema


settings = get_settings()
fake = Faker()


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine() -> AsyncEngine:
    return create_async_engine(settings.SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope="function")
async def init_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="function")
async def session(init_tables: None, session_maker: session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def http_test_client() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="function")
async def questions(request: SubRequest) -> list[QuestionSchema]:
    questions_num = request.param if hasattr(request, "param") and isinstance(request.param, int) and request.param > 0 else 1
    questions = [
        QuestionSchema(
            at_api_id=fake.random_int(min=1, max=10000),
            text=fake.text(),
            answer=fake.text(max_nb_chars=50),
            created_at=datetime.utcnow()
        ) for _ in range(questions_num)
    ]
    return questions