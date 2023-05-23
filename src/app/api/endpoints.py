from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import QuestionInSchema, QuestionOutSchema
from services import questions
from dependencies import get_session, get_http_client
from exceptions import QuestionsAPIError

router = APIRouter()


@router.post("/")
async def add_questions(
        question_in: QuestionInSchema,
        session: AsyncSession = Depends(get_session),
        http_client: AsyncClient = Depends(get_http_client)
) -> QuestionOutSchema | dict:
    try:
        return await questions(session=session, http_client=http_client, question_num=question_in.question_num)
    except QuestionsAPIError:
        raise HTTPException(status_code=503, detail="Please, try again")
