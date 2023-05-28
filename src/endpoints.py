from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from dependencies import get_session, get_http_client
from exceptions import QuestionsAPIError
from schemas import QuestionInSchema, QuestionOutSchema
from services import fetch_and_insert_questions, get_last_question

router = APIRouter()


@router.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")


@router.post("/questions")
async def add_questions(
    question_in: QuestionInSchema,
    session: AsyncSession = Depends(get_session),
    http_client: AsyncClient = Depends(get_http_client),
) -> QuestionOutSchema | dict:
    question = await get_last_question(session)
    try:
        await fetch_and_insert_questions(
            session=session,
            http_client=http_client,
            question_num=question_in.question_num,
        )
    except QuestionsAPIError:
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unreachable, please try again later",
        )
    return question or {}
