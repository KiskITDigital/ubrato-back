from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from exceptions import request_validation_exception_handler
from routers.v1 import auth, health

app = FastAPI()

app.include_router(auth.router)
app.include_router(health.router)

app.add_exception_handler(
    RequestValidationError, request_validation_exception_handler
)
