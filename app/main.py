
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.tasks import router as tasks_router
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="TaskFlow Engineering API",
    description="Task management API for the engineering knowledge graph demo",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(tasks_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "TaskFlow Engineering API",
        "version": "0.2.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
