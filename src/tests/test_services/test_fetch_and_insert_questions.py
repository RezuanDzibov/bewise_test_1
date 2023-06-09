import json

import pytest
from httpx import AsyncClient
from pytest_httpserver import HTTPServer
from pytest_mock import MockerFixture
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings
from exceptions import QuestionsAPIError
from models import Question
from schemas import QuestionSchema, QuestionOutSchema
from services import fetch_and_insert_questions, _insert_questions


async def test_insert_questions_without_duplicates(
    session: AsyncSession, http_client: AsyncClient
):
    await fetch_and_insert_questions(
        session=session, http_client=http_client, question_num=10
    )
    statement = select(func.count()).select_from(Question)

    result = await session.execute(statement)

    questions_in_db_num = result.scalar()
    assert questions_in_db_num == 10


@pytest.mark.parametrize("questions", [13], indirect=True)
async def test_insert_questions_with_duplicates(
    httpserver: HTTPServer,
    mocker: MockerFixture,
    session: AsyncSession,
    http_client: AsyncClient,
    questions: list[QuestionSchema],
):
    await _insert_questions(session=session, questions=questions[:3])
    mocker.patch(
        "services.settings", Settings(QUESTIONS_API_URL=httpserver.url_for("/"))
    )
    httpserver.expect_request("/random", query_string="count=10").respond_with_json(
        [
            json.loads(
                QuestionOutSchema(
                    id=question.at_api_id, question=question.text, **question.dict()
                ).json()
            )
            for question in questions[:10]
        ]
    )
    httpserver.expect_request("/random", query_string="count=3").respond_with_json(
        [
            json.loads(
                QuestionOutSchema(
                    id=question.at_api_id, question=question.text, **question.dict()
                ).json()
            )
            for question in questions[10:]
        ]
    )

    await fetch_and_insert_questions(
        session=session, http_client=http_client, question_num=10
    )

    statement = select(func.count()).select_from(Question)
    result = await session.execute(statement)

    questions_in_db_num = result.scalar()
    assert 13 == questions_in_db_num


@pytest.mark.parametrize("questions", [10], indirect=True)
async def test_api_fails_on_second_request(
    httpserver: HTTPServer,
    mocker: MockerFixture,
    session: AsyncSession,
    http_client: AsyncClient,
    questions: list[QuestionSchema],
):
    duplicate_questions = [question for question in questions[:3]]
    await _insert_questions(session=session, questions=duplicate_questions)
    mocker.patch(
        "services.settings", Settings(QUESTIONS_API_URL=httpserver.url_for("/"))
    )
    httpserver.expect_request("/random", query_string="count=10").respond_with_json(
        [
            json.loads(
                QuestionOutSchema(
                    id=question.at_api_id, question=question.text, **question.dict()
                ).json()
            )
            for question in questions
        ]
    )
    httpserver.expect_request("/random", query_string="count=3").respond_with_data(
        "API Failed(", status=503
    )

    with pytest.raises(QuestionsAPIError):
        await fetch_and_insert_questions(
            session=session, http_client=http_client, question_num=10
        )

    statement = select(func.count()).select_from(Question)
    result = await session.execute(statement)

    questions_in_db_num = result.scalar()
    assert 0 == questions_in_db_num
