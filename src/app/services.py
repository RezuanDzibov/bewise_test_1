from typing import Optional, List

import httpx
from sqlalchemy import select, Sequence
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


async def get_duplicate_questions(session: AsyncSession, questions: List[QuestionSchema]) -> Sequence:
    statement = select(Question).where(Question.at_api_id.in_([question.at_api_id for question in questions]))
    result = await session.execute(statement)
    return result.scalars().all()


async def get_unique_questions(duplicate_questions: Sequence, questions_from_api: List[QuestionSchema]) -> list:
    duplicate_questions = [QuestionSchema(**question.as_dict()) for question in duplicate_questions]
    unique_questions_from_api = [
        question for question in questions_from_api if question not in duplicate_questions
    ]
    return unique_questions_from_api


async def get_last_question(session: AsyncSession) -> Optional:
    statement = select(Question).order_by(Question.id.desc())
    result = await session.execute(statement)
    return result.scalar()


async def add_questions(session: AsyncSession, question_num: int) -> dict | QuestionOutSchema:
    unique_questions = []
    while question_num != 0:
        questions_from_api = await get_questions_from_api(question_num)
        duplicate_questions = await get_duplicate_questions(session, questions_from_api)
        if not duplicate_questions:
            unique_questions.extend(questions_from_api)
            question_num = 0
        else:
            unique_questions_from_api = await get_unique_questions(duplicate_questions, questions_from_api)
            unique_questions.extend(unique_questions_from_api)
            question_num = question_num - len(unique_questions_from_api)
    last_question_in_db = await get_last_question(session)
    session.add_all([Question(**unique_question.dict()) for unique_question in unique_questions])
    await session.commit()
    if last_question_in_db:
        return QuestionOutSchema(
            id=last_question_in_db.at_api_id,
            question=last_question_in_db.text,
            answer=last_question_in_db.answer,
            created_at=last_question_in_db.created_at
        )
    else:
        return {}
