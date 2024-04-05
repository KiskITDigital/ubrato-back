import typesense
from fastapi import Depends
from repositories.typesense.client import get_db_connection
from repositories.typesense.schemas import TypesenseTender


class TenderIndex:
    db: typesense.Client

    def __init__(
        self, db: typesense.Client = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def save(self, tender: TypesenseTender) -> None:
        self.db.collections["tender_index"].documents.create(tender.__dict__)

    def update(self, tender: TypesenseTender) -> None:
        self.db.collections["tender_index"].documents.update(
            tender.__dict__, {"filter_by": f"id:{tender.id}"}
        )
