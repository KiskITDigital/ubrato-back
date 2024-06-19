import uuid
from typing import Dict, List, Optional

from config import get_config
from fastapi import Depends, status
from repositories.postgres.database import get_db_connection
from repositories.postgres.exceptions import RepositoryException
from repositories.postgres.schemas import (
    Document,
    DocumentType,
    VerificationRequest,
)
from schemas import models
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class VerificationRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

    async def get_doc_types(self) -> Dict[str, int]:
        query = await self.db.execute(select(DocumentType))

        doc_types: Dict[str, int] = {}

        for doc_type in query.scalars().all():
            doc_types[doc_type.name] = doc_type.id

        return doc_types

    async def save_docs(
        self,
        document: Document,
    ) -> None:
        self.db.add(document)
        await self.db.commit()

    async def get_user_doc(
        self,
        user_id: str,
    ) -> List[models.VerificationDoc]:
        query = await self.db.execute(
            select(Document, DocumentType.name)
            .join(DocumentType)
            .where(Document.user_id == user_id)
        )
        docs: List[models.VerificationDoc] = []

        for doc_info in query.all():
            doc, type_name = doc_info._tuple()
            docs.append(
                models.VerificationDoc(
                    id=doc.id,
                    type=type_name,
                    link=doc.url,
                )
            )

        return docs

    async def get_doc_by_id(self, doc_id: str) -> Document:
        query = await self.db.execute(
            select(Document).where(Document.id == doc_id)
        )
        document = query.scalar_one_or_none()
        if document is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["document_not_found"]
                .format(doc_id),
                sql_msg="",
            )
        return document

    async def delete_doc_by_id(self, doc_id: str) -> None:
        doc = await self.get_doc_by_id(doc_id=doc_id)
        await self.db.delete(doc)
        await self.db.commit()

    async def create_verification_requests(self, user_id: str) -> None:
        self.db.add(
            VerificationRequest(
                id=str(uuid.uuid4()),
                user_id=user_id,
            )
        )
        await self.db.commit()

    async def response_verification_requests(
        self, verf_id: str, is_verified: bool, msg: Optional[str]
    ) -> None:
        query = await self.db.execute(
            select(VerificationRequest).where(
                VerificationRequest.id == verf_id
            )
        )
        verf_req = query.scalar_one_or_none()
        if verf_req is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["verified_request_not_found"]
                .format(verf_id),
                sql_msg="",
            )

        verf_req.verified = is_verified
        verf_req.verified_at = func.current_timestamp()
        verf_req.msg = msg

        await self.db.commit()

    async def get_verf_by_id(self, verf_id: str) -> VerificationRequest:
        query = await self.db.execute(
            select(VerificationRequest).where(
                VerificationRequest.id == verf_id
            )
        )
        verf_req = query.scalar_one_or_none()
        if verf_req is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_config()
                .Localization.config["errors"]["verified_request_not_found"]
                .format(verf_id),
                sql_msg="",
            )
        return verf_req

    async def get_verification_history(
        self, user_id: str
    ) -> List[models.VerificationInfo]:
        query = await self.db.execute(
            select(VerificationRequest).where(
                VerificationRequest.user_id == user_id
            )
        )

        verf_req_list: List[models.VerificationInfo] = []

        for verf_req in query.scalars().all():
            verf_req_list.append(
                models.VerificationInfo(
                    id=verf_req.id,
                    verified=verf_req.verified,
                    msg=verf_req.msg,
                    verified_at=verf_req.verified_at,
                    created_at=verf_req.created_at,
                )
            )
        return verf_req_list
