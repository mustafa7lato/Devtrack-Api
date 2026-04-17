from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.core.database import engine, Base

app = FastAPI(title=settings.APP_NAME)

app.include_router(router, prefix=settings.API_V1_STR)

Base.metadata.create_all(bind=engine)
