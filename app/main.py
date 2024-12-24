from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.config import settings
from app.core.database import database
from app.routers.v1.endpoints import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await database.dispose()


app = FastAPI(
    title=settings.project.name,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

@app.get("/", tags=["status"])
async def health_check():
    return {
        "name": settings.project.name,
        "version": settings.project.version
    }

app.include_router(api_router, prefix=f"/{settings.project.v1_prefix}")