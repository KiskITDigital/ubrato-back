from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from repositories import LogsRepository
from repositories.database import SessionLocal
from repositories.exceptions import RepositoryException
from services.exceptions import AuthException, ServiceException
from services.logs import LogsService
from sqlalchemy.orm import scoped_session

__all__ = ["AuthException", "ServiceException"]


class LogsDependency:
    def __init__(self) -> None:
        self.logs_service = LogsService(
            logs_repository=LogsRepository(scoped_session(SessionLocal))
        )

    async def __call__(self) -> LogsService:
        return self.logs_service


logs_dependency = LogsDependency()


async def auth_exception_handler(
    request: Request,
    exc: AuthException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code, content={"msg": exc.detail}
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": jsonable_encoder(exc.errors(), exclude={"input", "url"})
        },
    )


async def service_exception_handler(
    request: Request,
    exc: ServiceException,
) -> JSONResponse:
    logs_service: LogsService = await logs_dependency()
    id = await logs_service.save_logs(
        request=request,
        status_code=exc.status_code,
        msg=exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code, content={"id": id, "msg": str(exc.detail)}
    )


async def repository_exception_handler(
    request: Request,
    exc: RepositoryException,
) -> JSONResponse:
    logs_service: LogsService = await logs_dependency()
    id = await logs_service.save_logs(
        request=request,
        status_code=exc.status_code,
        msg=exc.sql_msg,
    )
    return JSONResponse(
        status_code=exc.status_code, content={"id": id, "msg": str(exc.detail)}
    )
