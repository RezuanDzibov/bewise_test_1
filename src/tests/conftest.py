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
from services import _insert_questions

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
async def questions(request: SubRequest) -> list[QuestionSchema]:
    if hasattr(request, "param") and isinstance(request.param, int) and request.param > 0:
        questions_num = request.param
    else:
        questions_num = 1
    questions = [
        QuestionSchema(
            at_api_id=fake.random_int(min=1, max=10000),
            text=fake.text(),
            answer=fake.text(max_nb_chars=50),
            created_at=datetime.utcnow()
        ) for _ in range(questions_num)
    ]
    return questions


@pytest.fixture(scope="function")
@pytest.mark.parametrize("questions", [10], indirect=True)
async def last_question_in_db(session: AsyncSession, questions: list[QuestionSchema]) -> QuestionSchema:
    await _insert_questions(session, questions)
    await session.commit()
    return questions[-1]


@pytest.fixture(scope="function")
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(timeout=settings.QUESTIONS_API_TIMEOUT) as client:
        yield client
