import uuid

from fastapi import Depends, Request
from repositories.logs_repository import LogsRepository
from repositories.schemas import Logs


class LogsService:
    logs_repository: LogsRepository

    def __init__(
        self, logs_repository: LogsRepository = Depends(LogsRepository)
    ) -> None:
        self.logs_repository = logs_repository

    async def save_logs(
        self, request: Request, status_code: int, msg: str
    ) -> str:
        body = await request.body()
        method = request.method
        url = str(request.url)
        id = "err_" + str(uuid.uuid4())
        logs = Logs(
            id="err_" + str(uuid.uuid4()),
            method=method,
            url=url,
            body=body.decode("utf-8"),
            code=status_code,
            msg=msg,
        )
        self.logs_repository.save(logs)
        return id
