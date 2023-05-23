from typing import List

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import get_settings
from models.questions import Question
from schemas import QuestionSchema, QuestionOutSchema
from exceptions import QuestionsAPIError

settings = get_settings()


async def get_questions_from_api(question_num: int) -> List[QuestionSchema]:
    async with httpx.AsyncClient() as client:
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


async def get_duplicate_questions(session: AsyncSession, questions: List[QuestionSchema]) -> List[QuestionSchema]:
    statement = select(Question).where(Question.at_api_id.in_([question.at_api_id for question in questions]))
    result = await session.execute(statement)
    duplicate_questions = result.scalars().all()
    return [QuestionSchema(**question.as_dict()) for question in duplicate_questions]


async def get_unique_questions(
        duplicate_questions: List[QuestionSchema],
        questions_from_api: List[QuestionSchema]
) -> List[QuestionSchema]:
    unique_questions_from_api = [
        question for question in questions_from_api if question not in duplicate_questions
    ]
    return unique_questions_from_api


async def get_last_question_or_dict(session: AsyncSession) -> QuestionOutSchema | dict:
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
    else:
        return {}


async def add_questions(session: AsyncSession, questions: List[QuestionSchema]) -> None:
    session.add_all([Question(**question.dict()) for question in questions])
    await session.commit()


async def questions(session: AsyncSession, question_num: int) -> QuestionOutSchema | dict:
    unique_questions = []
    while question_num != 0:
        questions_from_api = await get_questions_from_api(question_num)
        duplicate_questions = await get_duplicate_questions(session, questions_from_api)
        if not duplicate_questions:
            unique_questions.extend(questions_from_api)
            question_num = 0
        else:
            unique_question_from_api = await get_unique_questions(duplicate_questions, questions_from_api)
            unique_questions.extend(questions_from_api)
            question_num = question_num - len(unique_question_from_api)
    last_question = await get_last_question_or_dict(session)
    await add_questions(session, unique_questions)
    return last_question
