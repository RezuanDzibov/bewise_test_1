from copy import copy

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from models import Question
from schemas import QuestionSchema
from services import _insert_questions


@pytest.mark.parametrize("questions", [1], indirect=True)
async def test_insert_one_question(session: AsyncSession, questions: list[QuestionSchema]):
    inserted_num = await _insert_questions(session, questions)
    statement = select(func.count()).select_from(Question)
    result = await session.execute(statement)
    questions_in_db_num = result.scalar()
    assert inserted_num == questions_in_db_num


@pytest.mark.parametrize("questions", [10], indirect=True)
async def test_insert_many_questions(session: AsyncSession, questions: list[QuestionSchema]):
    inserted_num = await _insert_questions(session, questions)
    statement = select(func.count()).select_from(Question)
    result = await session.execute(statement)
    questions_in_db_num = result.scalar()
    assert inserted_num == questions_in_db_num


@pytest.mark.parametrize("questions", [10], indirect=True)
async def test_insert_with_duplicates(session: AsyncSession, questions: list[QuestionSchema]):
    questions_copy = questions.copy()
    questions_copy.append(copy(questions[0]))
    inserted_num = await _insert_questions(session, questions_copy)
    assert inserted_num == len(questions)
