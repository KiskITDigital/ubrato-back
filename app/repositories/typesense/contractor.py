from typing import List

import typesense
from fastapi import Depends
from repositories.typesense.client import get_db_connection
from repositories.typesense.schemas import (
    TypesenseContractor,
    TypesenseContractorService,
)


class ContractorIndex:
    db: typesense.Client

    def __init__(
        self, db: typesense.Client = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def save(
        self,
        contractor: TypesenseContractor,
        cities: List[int],
        objects: List[int],
        services: List[TypesenseContractorService],
    ) -> None:
        self.db.collections["contractor_index"].documents.create(
            contractor.model_dump()
        )
        for city in cities:
            self.db.collections["contractor_city"].documents.create(
                {"contractor_id": contractor.id, "city_id": str(city)}
            )

        for object in objects:
            self.db.collections["contractor_object"].documents.create(
                {"contractor_id": contractor.id, "object_type_id": str(object)}
            )

        for service in services:
            self.db.collections["contractor_object"].documents.create(
                service.model_dump()
            )

    def update_locations(
        self,
        contractor_id: str,
        locations: List[int],
    ) -> None:
        self.db.collections["contractor_city"].documents.delete(
            {"filter_by": f"contractor_id:{contractor_id}"}
        )
        for location in locations:
            self.db.collections["contractor_city"].documents.create(
                {"contractor_id": contractor_id, "city_id": str(location)}
            )

    def update_objects(
        self,
        contractor_id: str,
        objects: List[int],
    ) -> None:
        self.db.collections["contractor_object"].documents.delete(
            {"filter_by": f"contractor_id: {contractor_id}"}
        )
        for object in objects:
            self.db.collections["contractor_object"].documents.create(
                {
                    "contractor_id": str(contractor_id),
                    "object_type_id": str(object),
                }
            )

    def update_services(
        self,
        contractor_id: str,
        services: List[TypesenseContractorService],
    ) -> None:
        self.db.collections["contractor_service"].documents.delete(
            {"filter_by": f"contractor_id: {contractor_id}"}
        )
        for service in services:
            self.db.collections["contractor_service"].documents.create(
                service.model_dump()
            )
