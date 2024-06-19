from fastapi import HTTPException


class RepositoryException(HTTPException):
    status_code: int
    detail: str
    sql_msg: str

    def __init__(self, *args, sql_msg: str, **kwargs) -> None:  # type: ignore
        self.sql_msg = sql_msg
        super().__init__(*args, **kwargs)
