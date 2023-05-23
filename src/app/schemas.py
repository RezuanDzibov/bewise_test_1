import datetime

from pydantic import BaseModel, conint


class QuestionIn(BaseModel):
    question_num: conint(strict=True, ge=1)


class QuestionSchema(BaseModel):
    at_api_id: int
    text: str
    answer: str
    created_at: datetime.datetime
