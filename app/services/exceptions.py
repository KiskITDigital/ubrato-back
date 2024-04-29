from fastapi import HTTPException

ERROR_WHILE_CREATE_USER = "Internal error when creating a user"
USER_EMAIL_NOT_FOUND = "User with email {} not found."
USER_NOT_FOUND = "User not found."
SESSION_EXPIRED = "Session expired"
NO_BARRIER_TOKEN = "No barrier token"
INVALID_BARRIER = "Bearer token is invalid"
INVALID_SERVICES_COUNT = "Tender cannot be without services"
INVALID_OBJECTS_COUNT = "Tender cannot be without objects"
EXPIRED_RESET_CODE = "This reset code has expired"


class ServiceException(HTTPException):
    status_code: int
    detail: str

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)


class AuthException(HTTPException):
    status_code: int
    detail: str

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
