
from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow Engineering API",
    description="Demo API for engineering knowledge graph ingestion",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "service": "TaskFlow Engineering API",
        "version": "0.1.0",
        "docs": "/docs",
    }
