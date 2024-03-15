from exceptions import (
    AuthException,
    ServiceException,
    auth_exception_handler,
    exception_handler,
    request_validation_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from routers.v1 import auth, health, manager, role, tender, users

app = FastAPI(
    title="Ubrato API",
    version="0.1.0",
    servers=[
        {
            "url": "https://apiubrato.godmod.dev/docs",
            "description": "development environment",
        },
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(role.router)
app.include_router(manager.router)
app.include_router(tender.router)

app.add_exception_handler(
    RequestValidationError, request_validation_exception_handler
)

app.add_exception_handler(ServiceException, exception_handler)
app.add_exception_handler(AuthException, auth_exception_handler)
