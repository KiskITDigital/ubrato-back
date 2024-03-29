from exceptions import (
    AuthException,
    ServiceException,
    auth_exception_handler,
    internal_exception_hander,
    repository_exception_handler,
    request_validation_exception_handler,
    service_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from repositories.exceptions import RepositoryException
from routers.v1 import auth, health, manager, role, tender, users

app = FastAPI(
    title="Ubrato API",
    version="0.1.0",
    servers=[
        {
            "url": "https://api.ubrato.ru/",
            "description": "development environment",
        },
    ],
)

origins = [
    "http://ubrato.ru",
    "https://ubrato.ru",
    "http://dev.ubrato.ru",
    "https://dev.ubrato.ru",
    "http://localhost",
    "http://localhost:5174",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(role.router)
app.include_router(manager.router)
app.include_router(tender.router)

app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,  # type: ignore
)
app.add_exception_handler(
    ServiceException,
    service_exception_handler  # type: ignore
)
app.add_exception_handler(
    RepositoryException,
    repository_exception_handler,  # type: ignore
)
app.add_exception_handler(
    AuthException,
    auth_exception_handler  # type: ignore
)
app.add_exception_handler(
    Exception,
    internal_exception_hander  # type: ignore
)
