import httpx
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import get_settings
from models.questions import Question
from schemas import QuestionSchema

settings = get_settings()


async def get_question_from_api(question_num: int) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.QUESTIONS_API_URL}random?count={question_num}")
        return response.json()


async def get_duplicate_questions(session: AsyncSession, questions: list) -> Sequence:
    statement = select(Question).where(Question.at_api_id.in_([question["id"] for question in questions]))
    result = await session.execute(statement)
    return result.scalars().all()


async def handle_duplicate_questions(duplicate_questions: Sequence, questions_from_api: list) -> list:
    duplicate_questions = [QuestionSchema(**question.as_dict()) for question in duplicate_questions]
    questions_from_api = [
        QuestionSchema(
            at_api_id=question["id"], text=question["question"], **question
        ) for question in questions_from_api
    ]
    unique_questions_from_api = [
        question for question in questions_from_api if question not in duplicate_questions
    ]
    return unique_questions_from_api


async def add_questions(session: AsyncSession, question_num: int):
    are_questions_unique = False
    unique_questions = []
    while not are_questions_unique:
        questions_from_api = await get_question_from_api(question_num)
        duplicate_questions = await get_duplicate_questions(session, questions_from_api)
        if not duplicate_questions:
            unique_questions.extend([
                QuestionSchema(
                    at_api_id=question["id"], text=question["question"], **question
                ) for question in questions_from_api
            ])
            are_questions_unique = True
        else:
            unique_questions_from_api = await handle_duplicate_questions(duplicate_questions, questions_from_api)
            unique_questions.extend(unique_questions_from_api)
            question_num = question_num - len(unique_questions_from_api)
    session.add_all([Question(**unique_question.dict()) for unique_question in unique_questions])
    await session.commit()
