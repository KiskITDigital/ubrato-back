from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from services.logs import LogsService


class ServiceException(HTTPException):
    status_code: int
    detail: str
    logs_service: LogsService

    def __init__(self, *args, logs_service: LogsService, **kwargs):
        self.logs_service = logs_service
        return super().__init__(*args, **kwargs)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors(), exclude={"input", "url"})},
    )


async def exception_handler(
    request: Request,
    exc: ServiceException,
) -> JSONResponse:
    id = await exc.logs_service.save_logs(
        request=request,
        status_code=exc.status_code,
        msg=exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code, content={"id": id, "msg": exc.detail}
    )
