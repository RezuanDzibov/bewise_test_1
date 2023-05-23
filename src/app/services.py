from typing import List

import httpx
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import get_settings
from models.questions import Question
from schemas import QuestionSchema, QuestionOutSchema
from exceptions import QuestionsAPIError

settings = get_settings()


async def get_questions_from_api(client: httpx.AsyncClient, question_num: int) -> List[QuestionSchema]:
    try:
        response = await client.get(
            f"{settings.QUESTIONS_API_URL}random?count={question_num}",
            timeout=settings.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return [
            QuestionSchema(
                at_api_id=question["id"], text=question["question"], **question
                ) for question in response.json()
            ]
    except httpx.HTTPError:
        raise QuestionsAPIError


async def get_duplicate_questions(session: AsyncSession, questions: list[QuestionSchema]) -> list[QuestionSchema]:
    statement = select(Question).where(Question.at_api_id.in_([question.at_api_id for question in questions]))
    result = await session.execute(statement)
    duplicate_questions = result.scalars().all()
    return [QuestionSchema(**question.as_dict()) for question in duplicate_questions]


async def get_unique_questions(
        duplicate_questions: list[QuestionSchema],
        questions_from_api: list[QuestionSchema]
) -> list[QuestionSchema]:
    unique_questions_from_api = [
        question for question in questions_from_api if question not in duplicate_questions
    ]
    return unique_questions_from_api


async def get_last_question(session: AsyncSession) -> QuestionOutSchema | None:
    statement = select(Question).order_by(Question.id.desc())
    result = await session.execute(statement)
    question = result.scalar()
    if question:
        return QuestionOutSchema(
            id=question.at_api_id,
            question=question.text,
            answer=question.answer,
            created_at=question.created_at
        )
    return None


async def add_questions(session: AsyncSession, questions: list[QuestionSchema]) -> int:
    statement = insert(Question).values([question.dict() for question in questions]).on_conflict_do_nothing()
    statement = statement.returning(Question)
    result = await session.execute(statement)
    await session.commit()
    return len(result.scalars().all())


async def questions(
        session: AsyncSession,
        http_client: httpx.AsyncClient,
        question_num: int
) -> QuestionOutSchema | dict:
    last_question = await get_last_question(session)
    while True:
        questions_from_api = await get_questions_from_api(http_client, question_num)
        duplicate_questions = await get_duplicate_questions(session, questions_from_api)
        if not duplicate_questions:
            await add_questions(session, questions_from_api)
            break
        else:
            unique_question_from_api = await get_unique_questions(duplicate_questions, questions_from_api)
            added_question_num = await add_questions(session, unique_question_from_api)
            question_num -= added_question_num
    return last_question or {}
