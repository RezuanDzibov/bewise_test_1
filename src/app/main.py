from fastapi import FastAPI

from core.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)
