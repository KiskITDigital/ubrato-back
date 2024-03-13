from exceptions import (
    AuthException,
    ServiceException,
    auth_exception_handler,
    exception_handler,
    request_validation_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from routers.v1 import auth, health, manager, role, tender

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
app.include_router(manager.router)
app.include_router(tender.router)

app.add_exception_handler(
    RequestValidationError, request_validation_exception_handler
)

app.add_exception_handler(ServiceException, exception_handler)
app.add_exception_handler(AuthException, auth_exception_handler)
