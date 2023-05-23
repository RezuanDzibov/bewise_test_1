from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from schemas import QuestionInSchema, QuestionOutSchema
import services
from exceptions import QuestionsAPIError

router = APIRouter()


@router.post("/")
async def add_questions(
        question_in: QuestionInSchema,
        session: AsyncSession = Depends(get_session)
) -> QuestionOutSchema | dict:
    try:
        return await services.questions(session=session, question_num=question_in.question_num)
    except QuestionsAPIError:
        raise HTTPException(status_code=503, detail="Please, try again")
