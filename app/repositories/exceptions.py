from fastapi import HTTPException

SESSION_NOT_FOUND = "Session not found"
USERID_NOT_FOUND = "User with ID {} not found."
USER_EMAIL_NOT_FOUND = "User with email {} not found."
TENDERID_NOT_FOUND = "Tender with ID {} not found"
ORG_ALREADY_REG = "Organization with such data has already been registered"
USER_ALREADY_REG = "User with such data has already been registered"


class RepositoryException(HTTPException):
    status_code: int
    detail: str
    sql_msg: str

    def __init__(self, *args, sql_msg: str, **kwargs):
        self.sql_msg = sql_msg
        return super().__init__(*args, **kwargs)
