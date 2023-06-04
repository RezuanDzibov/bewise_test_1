from fastapi import FastAPI

from core.settings import get_settings
from endpoints import router as questions_router

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(questions_router, tags=["questions"])
