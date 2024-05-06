from pydantic import BaseModel


class AddDocumentResponse(BaseModel):
    id: str
