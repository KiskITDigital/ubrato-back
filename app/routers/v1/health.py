import os

from fastapi import APIRouter
from schemas.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/", response_model=HealthResponse)
async def health_status() -> HealthResponse:
    return HealthResponse(
        ok=True, version=os.environ.get("GIT_VERSION", "non git version")
    )
