from fastapi import APIRouter
from app.schemas.health import HealthResponse

health_router = APIRouter(tags=["system"])

@health_router.get(
    "/health",
    summary="Health check",
    description="Returns the current health status of the API service."
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")