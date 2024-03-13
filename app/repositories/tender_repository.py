from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.orm import scoped_session
from fastapi import Depends

from models import tender_model
from repositories.database import get_db_connection
from repositories.schemas import Tender
from sqlalchemy.exc import SQLAlchemyError


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
        self,
        page: int,
        page_size: int
    ) -> Tuple[List[tender_model.Tender], Optional[Exception]]:
        try:
            query = self.db.query(Tender).filter(
                Tender.active == True,
                Tender.reception_end > datetime.now()
            ).order_by(Tender.reception_end.desc()).limit(page_size).offset((page - 1) * page_size)
            tenders: List[tender_model.Tender] = []

            for tender in query:
                tenders.append(tender_model.Tender(**tender.__dict__))

            return tenders, None
        except SQLAlchemyError as err:
            return [], Exception(err.code)