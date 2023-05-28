from sqlalchemy.ext.asyncio import AsyncSession

from schemas import QuestionSchema
from services import get_last_question


async def test_questions_exist(
    session: AsyncSession, last_question_in_db: QuestionSchema
):
    last_question = await get_last_question(session)

    assert last_question.id == last_question_in_db.at_api_id


async def test_questions_not_exist(session: AsyncSession):
    assert await get_last_question(session) is None
