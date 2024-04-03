from fastapi import HTTPException

SESSION_NOT_FOUND = "Session not found."
USERID_NOT_FOUND = "User with ID {} not found."
USER_EMAIL_NOT_FOUND = "User with email {} not found."
TENDERID_NOT_FOUND = "Tender with ID {} not found."
DATA_ALREADY_EXIST = "Such data has already been registered."
CITY_NOT_FOUNT = "City with id {} not found."


class RepositoryException(HTTPException):
    status_code: int
    detail: str
    sql_msg: str

    def __init__(self, *args, sql_msg: str, **kwargs) -> None:  # type: ignore
        self.sql_msg = sql_msg
        super().__init__(*args, **kwargs)
