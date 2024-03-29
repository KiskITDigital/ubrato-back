from datetime import datetime
from typing import Any, List, Optional

import models
from fastapi import Depends, status
from repositories.database import get_db_connection
from repositories.exceptions import TENDERID_NOT_FOUND, RepositoryException
from repositories.schemas import Tender
from sqlalchemy import and_
from sqlalchemy.orm import Session, scoped_session


class TenderRepository:
    db: scoped_session[Session]

    def __init__(
        self, db: scoped_session[Session] = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create_tender(self, tender: Tender) -> int:
        self.db.add(tender)
        self.db.commit()

        self.db.refresh(tender)

        return tender.id

    def update_tender(self, tender: dict[str, Any], tender_id: int) -> None:
        tender_to_update = (
            self.db.query(Tender).filter(Tender.id == tender_id).first()
        )

        if tender_to_update is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=tender_id,
                sql_msg="",
            )

        for key, value in tender.items():
            setattr(tender_to_update, key, value)
            tender_to_update.active = False
            tender_to_update.verified = False

        self.db.commit()

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
    ) -> List[models.Tender]:
        reception_end_condition = Tender.reception_end > datetime.now()

        object_group_condition = (object_group_id is None) or (
            Tender.object_group_id == object_group_id
        )

        object_type_condition = (object_type_id is None) or (
            Tender.object_type_id == object_type_id
        )

        service_type_condition = (service_type_ids is None) or and_(
            *(
                Tender.services_types.any(service_type_id)  # type: ignore
                for service_type_id in service_type_ids
            )
        )

        service_group_condition = (service_group_ids is None) or and_(
            *(
                Tender.services_groups.any(service_group_id)  # type: ignore
                for service_group_id in service_group_ids
            )
        )

        floor_space_from_condition = (floor_space_from is None) or (
            Tender.floor_space >= floor_space_from
        )

        floor_space_to_condition = (floor_space_to is None) or (
            Tender.floor_space <= floor_space_to
        )

        price_from_condition = (price_from is None) or (
            Tender.price >= price_from
        )

        price_to_condition = (price_to is None) or (
            Tender.price <= price_to
        )

        text_condition = (text is None) or Tender.document_tsv.match(text)

        active_condition = (active is None) or (Tender.active == active)

        verified_condition = (verified is None) or (
            Tender.verified == verified
        )

        user_id_condition = (user_id is None) or (
            Tender.user_id == user_id
        )

        query = (
            self.db.query(Tender)
            .filter(
                and_(
                    reception_end_condition,
                    object_group_condition,  # type: ignore
                    object_type_condition,  # type: ignore
                    service_type_condition,  # type: ignore
                    service_group_condition,  # type: ignore
                    floor_space_from_condition,  # type: ignore
                    floor_space_to_condition,  # type: ignore
                    price_from_condition,  # type: ignore
                    price_to_condition,  # type: ignore
                    text_condition,  # type: ignore
                    active_condition,  # type: ignore
                    verified_condition,  # type: ignore
                    user_id_condition,  # type: ignore
                )
            )
            .order_by(Tender.reception_end.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        tenders: List[models.Tender] = []

        for tender in query:
            tenders.append(models.Tender(**tender.__dict__))

        return tenders

    def get_tender_by_id(self, tender_id: int) -> models.Tender:
        tender = (
            self.db.query(Tender).filter(Tender.id == tender_id).first()
        )
        if tender is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=TENDERID_NOT_FOUND.format(tender_id),
                sql_msg="",
            )

        return models.Tender(**tender.__dict__)

    def update_verified_status(self, tender_id: int, verified: bool) -> None:
        tender = (
            self.db.query(Tender).filter(Tender.id == tender_id).first()
        )

        if tender is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=TENDERID_NOT_FOUND.format(tender_id),
                sql_msg="",
            )

        tender.verified = verified
        self.db.commit()

    def update_active_status(self, tender_id: int, active: bool) -> None:
        tender = (
            self.db.query(Tender).filter(Tender.id == tender_id).first()
        )

        if tender is None:
            raise RepositoryException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=TENDERID_NOT_FOUND.format(tender_id),
                sql_msg="",
            )
        tender.active = active
        self.db.commit()

    def get_count_active_tenders(
        self, object_group_id: Optional[int], service_type_id: Optional[int]
    ) -> int:
        query = self.db.query(Tender).filter(
            Tender.active,
            Tender.reception_end > datetime.now(),
            object_group_id is None  # type: ignore
            or Tender.object_group_id == object_group_id,
            service_type_id is None  # type: ignore
            or Tender.services_types.any(service_type_id),  # type: ignore
        )
        return query.count()
