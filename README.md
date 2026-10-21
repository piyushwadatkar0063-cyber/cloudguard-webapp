# CloudGuard

A cloud-based application deployment health,
monitoring, and cost management platform.

## Current features
- FastAPI backend
- Root API endpoint
- Application health endpoint
- Automated endpoint tests

## Local development

Activate the backend virtual environment and run:

python -m uvicorn main:app --reload

Run tests:

python -m pytest -v