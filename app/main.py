from exceptions import (
    not_found_exception_handler,
    request_validation_exception_handler,
)
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from routers.v1 import auth, health

app = FastAPI()

app.include_router(auth.router)
app.include_router(health.router)

app.add_exception_handler(
    RequestValidationError, request_validation_exception_handler
)

app.add_exception_handler(
    status.HTTP_404_NOT_FOUND, not_found_exception_handler
)
