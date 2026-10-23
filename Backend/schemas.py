
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DeploymentCreate(BaseModel):
    application_name: str = Field(min_length=1, max_length=100)
    environment: str = Field(min_length=1, max_length=50)
    status: str = Field(pattern="^(success|failed|in_progress)$")


class DeploymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_name: str
    environment: str
    status: str
    created_at: datetime
