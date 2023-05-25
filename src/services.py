from typing import List

import httpx
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import get_settings
from exceptions import QuestionsAPIError
from models.questions import Question
from schemas import QuestionSchema, QuestionOutSchema

settings = get_settings()


async def _get_questions_from_api(client: httpx.AsyncClient, question_num: int) -> List[QuestionSchema]:
    try:


        response = await client.get(f"{settings.QUESTIONS_API_URL}random?count={question_num}")
        response.raise_for_status()
    except httpx.HTTPError:
        raise QuestionsAPIError
    return [
        QuestionSchema(
            at_api_id=question["id"], text=question["question"], **question
        ) for question in response.json()
    ]


async def get_last_question(session: AsyncSession) -> QuestionOutSchema | None:
    statement = select(Question).order_by(Question.id.desc())
    result = await session.execute(statement)
    question = result.scalar()
    if question:
        return QuestionOutSchema.from_orm(question)
    return None


async def _insert_questions(session: AsyncSession, questions: list[QuestionSchema]) -> int:
    statement = insert(Question).values([question.dict() for question in questions]).on_conflict_do_nothing()
    statement = statement.returning(Question)
    result = await session.execute(statement)
    return len(result.scalars().all())


async def fetch_and_insert_questions(
        session: AsyncSession,
        http_client: httpx.AsyncClient,
        question_num: int
) -> None:
    while question_num > 0:
        questions_from_api = await _get_questions_from_api(http_client, question_num)
        added_question_num = await _insert_questions(session, questions_from_api)
        question_num -= added_question_num
    await session.commit()
