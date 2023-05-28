import datetime

from pydantic import BaseModel, conint


class QuestionInSchema(BaseModel):
    question_num: conint(strict=True, ge=1, le=100)


class QuestionSchema(BaseModel):
    at_api_id: int
    text: str
    answer: str
    created_at: datetime.datetime


class QuestionOutSchema(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime

    class Config:
        fields = {"id": "at_api_id", "question": "text"}
        orm_mode = True
