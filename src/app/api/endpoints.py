from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from schemas import QuestionInSchema, QuestionOutSchema
import services

router = APIRouter()


@router.post("/")
async def add_questions(
        question_in: QuestionInSchema,
        session: AsyncSession = Depends(get_session)
) -> QuestionOutSchema | dict:
    return await services.add_questions(session=session, question_num=question_in.question_num)
