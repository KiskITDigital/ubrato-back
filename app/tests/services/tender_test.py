from datetime import datetime

from repositories.postgres.schemas import Tender
from schemas.create_tender import CreateTenderRequest


def test_created_tender(tender_service, created_user, postgres_session):
    tender = CreateTenderRequest(
        name="Office cleaning",
        price=100000,
        is_contract_price=False,
        city_id=1,
        floor_space=200,
        description="I need to clean office in Moscow city.",
        attachments=["some.link", "foo.bar"],
        wishes="As quickly as possible",
        services_groups=[1],
        services_types=[1],
        reception_start=datetime.now(),
        reception_end=datetime.now(),
        work_start=datetime.now(),
        work_end=datetime.now(),
        object_group_id=1,
        object_type_id=1,
    )

    created_tender = tender_service.create_tender(tender, created_user.id)
    postgres_session.query(Tender).filter_by(id=created_tender.id).delete()
    postgres_session.commit()


def test_get_page_tenders(created_tender, tender_service):
    tedners = tender_service.get_page_tenders(
        page=1,
        page_size=10,
        object_group_id=1,
        object_type_id=1,
        service_group_ids=[1],
        service_type_ids=[1],
        floor_space_from=0,
        floor_space_to=300,
        price_from=50000,
        price_to=150000,
        verified=False,
        user_id=created_tender.user_id,
    )

    assert tedners[0] == created_tender


def test_get_by_id(created_tender, tender_service):
    tender = tender_service.get_by_id(tender_id=created_tender.id)

    assert tender == created_tender
