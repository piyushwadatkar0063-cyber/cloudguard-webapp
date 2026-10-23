
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Deployment
from schemas import DeploymentCreate, DeploymentResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="CloudGuard API",
    description="Cloud deployment health and cost monitoring platform",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "project": "CloudGuard",
        "message": "CloudGuard API is running",
        "version": "1.0.0",
    }


@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )


@app.post(
    "/deployments",
    response_model=DeploymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_deployment(
    deployment_data: DeploymentCreate,
    db: Session = Depends(get_db),
):
    deployment = Deployment(**deployment_data.model_dump())
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment


@app.get("/deployments", response_model=list[DeploymentResponse])
def list_deployments(
    environment: str | None = Query(default=None, max_length=50),
    status_filter: Literal["success", "failed", "in_progress"] | None = Query(
        default=None,
        alias="status",
    ),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Deployment)

    if environment:
        query = query.filter(Deployment.environment == environment)

    if status_filter:
        query = query.filter(Deployment.status == status_filter)

    return (
        query.order_by(Deployment.created_at.desc(), Deployment.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@app.get(
    "/deployments/{deployment_id}",
    response_model=DeploymentResponse,
)
def get_deployment(
    deployment_id: int,
    db: Session = Depends(get_db),
):
    deployment = db.get(Deployment, deployment_id)

    if deployment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found",
        )

    return deployment
