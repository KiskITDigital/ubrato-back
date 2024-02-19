import os
from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
async def health_status():
    return {
        "ok": True,
        "git_version": os.environ.get("GIT_VERSION", "non git version"),
    }
