from typing import List

from fastapi import Depends
from repositories.postgres import DraftTenderRepository, TagsRepository
from repositories.postgres.schemas import DraftTender
from schemas import models
from schemas.create_draft_tender import CreateDraftTenderRequest


class DraftTenderService:
    tags_repository: TagsRepository
    tender_repository: DraftTenderRepository

    def __init__(
        self,
        tags_repository: TagsRepository = Depends(),
        tender_repository: DraftTenderRepository = Depends(),
    ) -> None:
        self.tags_repository = tags_repository
        self.tender_repository = tender_repository

    async def create_tender(
        self, tender: CreateDraftTenderRequest, user_id: str
    ) -> models.DraftTender:
        created_tender = await self.tender_repository.create_tender(
            tender=DraftTender(
                user_id=user_id,
                name=tender.name,
                price=tender.price,
                is_contract_price=tender.is_contract_price,
                is_nds_price=tender.is_nds_price,
                city_id=tender.city_id,
                floor_space=tender.floor_space,
                description=tender.description,
                wishes=tender.wishes,
                specification=tender.specification,
                attachments=tender.attachments,
                reception_start=tender.reception_start,
                reception_end=tender.reception_end,
                work_start=tender.work_start,
                work_end=tender.work_end,
            ),
            service_type_ids=tender.services_types,
            object_type_ids=tender.objects_types,
        )

        return await self.tender_repository.get_draft_tender_by_id(
            tender_id=created_tender.id
        )

    async def get_by_id(self, id: int) -> models.DraftTender:
        return await self.tender_repository.get_draft_tender_by_id(
            tender_id=id
        )

    async def update_tender(
        self, tender: CreateDraftTenderRequest, id: int
    ) -> None:
        await self.tender_repository.update_draft_tender(
            tender=tender.__dict__,
            id=id,
        )

    async def delete_tender(self, id: int) -> None:
        await self.tender_repository.delete_draft_tender(
            id=id,
        )

    async def get_user_tenders(self, user_id: str) -> List[models.DraftTender]:
        return await self.tender_repository.get_user_tenders(
            user_id=user_id,
        )
