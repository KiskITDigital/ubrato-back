from fastapi import HTTPException


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
