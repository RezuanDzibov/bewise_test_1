from sqlalchemy.ext.asyncio import AsyncSession

from schemas import QuestionSchema
from services import get_last_question


async def test_success(session: AsyncSession, last_question_in_db: QuestionSchema):
    last_question = await get_last_question(session)
    assert last_question.id == last_question_in_db.at_api_id
