from datetime import datetime
from typing import Any, List, Optional, Tuple

import models
from fastapi import Depends
from repositories.database import get_db_connection
from repositories.exceptions import TENDERID_NOT_FOUND
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

    def create_tender(self, tender: Tender) -> Tuple[int, Optional[Exception]]:
        try:
            self.db.add(tender)
            self.db.commit()

            self.db.refresh(tender)

            return tender.id, None
        except SQLAlchemyError as err:
            return 0, Exception(err.code)

    def update_tender(
        self, tender: dict[str, Any], tender_id: int
    ) -> Optional[Exception]:
        try:
            tender_to_update = (
                self.db.query(Tender).filter(Tender.id == tender_id).first()
            )

            if tender_to_update:
                for key, value in tender.items():
                    setattr(tender_to_update, key, value)
                    tender_to_update.active = False
                    tender_to_update.verified = False

                self.db.commit()
                return None

            return Exception(TENDERID_NOT_FOUND.format(tender_id))

        except SQLAlchemyError as err:
            return Exception(err.code)

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
    ) -> Tuple[List[models.Tender], Optional[Exception]]:
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

            return tenders, None
        except SQLAlchemyError as err:
            return [], Exception(err.code)

    def get_tender_by_id(
        self, id: int
    ) -> Tuple[Optional[models.Tender], Optional[Exception]]:
        try:
            query = self.db.query(Tender).filter(Tender.id == id)
            return query.first(), None
        except SQLAlchemyError as err:
            return None, Exception(err.code)

    def update_verified_status(
        self, tender_id: str, status: bool
    ) -> Optional[Exception]:
        try:
            tender = (
                self.db.query(Tender).filter(Tender.id == tender_id).first()
            )

            if tender:
                tender.verified = status
                self.db.commit()
                return None

            return Exception(TENDERID_NOT_FOUND.format(tender_id))
        except SQLAlchemyError as err:
            self.db.rollback()
            return Exception(err.code)

    def update_active_status(
        self, tender_id: str, active: bool
    ) -> Optional[Exception]:
        try:
            tender = (
                self.db.query(Tender)
                .filter(Tender.active == tender_id)
                .first()
            )

            if tender:
                tender.active = active
                self.db.commit()
                return None

            return Exception(TENDERID_NOT_FOUND.format(tender_id))
        except SQLAlchemyError as err:
            self.db.rollback()
            return Exception(err.code)

    def get_count_active_tenders(
        self, object_group_id: Optional[int], service_type_id: Optional[int]
    ) -> Tuple[int, Optional[Exception]]:
        try:
            query = self.db.query(Tender).filter(
                Tender.active,
                Tender.reception_end > datetime.now(),
                object_group_id is None
                or Tender.object_group_id == object_group_id,
                service_type_id is None
                or Tender.services_types.any(service_type_id),
            )
            return query.count(), None
        except SQLAlchemyError as err:
            return [], Exception(err.code)
