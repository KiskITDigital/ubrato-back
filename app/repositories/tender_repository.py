from datetime import datetime
from typing import Any, List, Optional

import models
from fastapi import Depends
from repositories.database import get_db_connection
from repositories.exceptions import TENDERID_NOT_FOUND, RepositoryException
from repositories.schemas import Tender
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session


class TenderRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create_tender(self, tender: Tender) -> int:
        try:
            self.db.add(tender)
            self.db.commit()

            self.db.refresh(tender)

            return tender.id
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def update_tender(self, tender: dict[str, Any], tender_id: int):
        try:
            tender_to_update = (
                self.db.query(Tender).filter(Tender.id == tender_id).first()
            )

            if tender_to_update is None:
                raise RepositoryException(
                    status_code=404, detail=tender_id, sql_msg=""
                )

            for key, value in tender.items():
                setattr(tender_to_update, key, value)
                tender_to_update.active = False
                tender_to_update.verified = False

            self.db.commit()
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_page_tenders(
        self,
        page: int,
        page_size: int,
        object_group_id: Optional[int],
        object_type_id: Optional[int],
        service_type_ids: Optional[List[int]],
        service_group_ids: Optional[List[int]],
        floor_space_from: Optional[int],
        floor_space_to: Optional[int],
        price_from: Optional[int],
        price_to: Optional[int],
        text: Optional[str],
        active: Optional[bool],
        verified: Optional[bool],
        user_id: Optional[str],
    ) -> models.Tender:
        try:
            query = (
                self.db.query(Tender)
                .filter(
                    Tender.reception_end > datetime.now(),
                    object_group_id is None
                    or Tender.object_group_id == object_group_id,
                    object_type_id is None
                    or Tender.object_type_id == object_type_id,
                    service_type_ids is None
                    or or_(
                        *(
                            Tender.services_types.any(service_type_id)
                            for service_type_id in service_type_ids
                        )
                    ),
                    service_group_ids is None
                    or or_(
                        *(
                            Tender.services_groups.any(service_group_id)
                            for service_group_id in service_group_ids
                        )
                    ),
                    floor_space_from is None
                    or Tender.floor_space >= floor_space_from,
                    floor_space_to is None
                    or Tender.floor_space <= floor_space_to,
                    price_from is None or Tender.price >= price_from,
                    price_to is None or Tender.price <= price_to,
                    text is None or Tender.document_tsv.match(text),
                    active is None or Tender.active == active,
                    verified is None or Tender.verified == verified,
                    user_id is None or Tender.user_id == user_id,
                )
                .order_by(Tender.reception_end.desc())
                .limit(page_size)
                .offset((page - 1) * page_size)
            )
            tenders: List[models.Tender] = []

            for tender in query:
                tenders.append(models.Tender(**tender.__dict__))

            return tenders
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_tender_by_id(self, tender_id: int) -> models.Tender:
        try:
            tender = (
                self.db.query(Tender).filter(Tender.id == tender_id).first()
            )
            if tender is None:
                raise RepositoryException(
                    status_code=404,
                    detail=TENDERID_NOT_FOUND.format(tender_id),
                    sql_msg="",
                )

            return tender
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def update_verified_status(self, tender_id: str, status: bool):
        try:
            tender = (
                self.db.query(Tender).filter(Tender.id == tender_id).first()
            )

            if tender is None:
                raise RepositoryException(
                    status_code=404,
                    detail=TENDERID_NOT_FOUND.format(tender_id),
                    sql_msg="",
                )

            tender.verified = status
            self.db.commit()
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def update_active_status(self, tender_id: str, active: bool):
        try:
            tender = (
                self.db.query(Tender)
                .filter(Tender.active == tender_id)
                .first()
            )

            if tender is None:
                raise RepositoryException(
                    status_code=404,
                    detail=TENDERID_NOT_FOUND.format(tender_id),
                    sql_msg="",
                )
            tender.active = active
            self.db.commit()

        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )

    def get_count_active_tenders(
        self, object_group_id: Optional[int], service_type_id: Optional[int]
    ) -> int:
        try:
            query = self.db.query(Tender).filter(
                Tender.active,
                Tender.reception_end > datetime.now(),
                object_group_id is None
                or Tender.object_group_id == object_group_id,
                service_type_id is None
                or Tender.services_types.any(service_type_id),
            )
            return query.count()
        except SQLAlchemyError as err:
            raise RepositoryException(
                status_code=500,
                detail=err.code,
                sql_msg=err._message(),
            )
