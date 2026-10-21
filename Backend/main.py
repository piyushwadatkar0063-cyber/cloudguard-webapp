
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(
    title="CloudGuard API",
    description="Cloud deployment health and monitoring platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "project": "CloudGuard",
        "message": "CloudGuard API is running",
        "version": app.version,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
