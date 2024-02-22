from exceptions import (
    internal_server_exception_handler,
    not_found_exception_handler,
    request_validation_exception_handler,
)
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from routers.v1 import auth, health, role

app = FastAPI(
    title="Ubrato API",
    version="0.1.0",
    servers=[
        {
            "url": "https://git.godmod.dev",
            "description": "development environment",
        },
    ],
)

app.include_router(auth.router)
app.include_router(health.router)
app.include_router(role.router)

app.add_exception_handler(
    RequestValidationError, request_validation_exception_handler
)
app.add_exception_handler(
    status.HTTP_404_NOT_FOUND, not_found_exception_handler
)
app.add_exception_handler(
    status.HTTP_500_INTERNAL_SERVER_ERROR, internal_server_exception_handler
)
