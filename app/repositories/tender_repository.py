from datetime import datetime
from typing import List, Optional, Tuple

import models
from fastapi import Depends
from repositories.database import get_db_connection
from repositories.schemas import Tender
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session


class TenderRepository:
    db: scoped_session

    def __init__(
        self, db: scoped_session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def create_tender(self, tender: Tender) -> Optional[Exception]:
        try:
            self.db.add(tender)
            self.db.commit()

            return None
        except SQLAlchemyError as err:
            return Exception(err.code)

    def get_page_active_tenders(
        self, page: int, page_size: int
    ) -> Tuple[List[models.Tender], Optional[Exception]]:
        try:
            query = (
                self.db.query(Tender)
                .filter(Tender.active, Tender.reception_end > datetime.now())
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
