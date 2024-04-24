import uuid

from fastapi import Depends, Request
from repositories.postgres import LogsRepository
from repositories.postgres.schemas import Logs


class LogsService:
    logs_repository: LogsRepository

    def __init__(
        self, logs_repository: LogsRepository = Depends(LogsRepository)
    ) -> None:
        self.logs_repository = logs_repository

    # TODO: save headers
    async def save_logs(
        self, request: Request, status_code: int, msg: str
    ) -> str:
        body = await request.body()
        method = request.method
        url = str(request.url)
        id = "err_" + str(uuid.uuid4())
        logs = Logs(
            id=id,
            method=method,
            url=url,
            body=body.decode("utf-8"),
            code=status_code,
            msg=msg,
        )
        await self.logs_repository.save(logs)
        return id
