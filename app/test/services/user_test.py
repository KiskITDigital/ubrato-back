import pytest
from repositories.postgres.schemas import Organization

from app.test.conftest import (
    generate_random_email,
    generate_random_number,
    generate_random_phone,
)


@pytest.mark.asyncio
async def test_create_user(user_service):
    org = Organization(
        id="org_" + str(generate_random_number()),
        brand_name="test",
        full_name="ooo full test",
        short_name="ooo test",
        inn=str(generate_random_number()),
        okpo=str(generate_random_number()),
        ogrn=str(generate_random_number()),
        kpp=str(generate_random_number()),
        tax_code=123,
        address="st. test",
        email=generate_random_email(),
        phone=generate_random_phone(),
    )

    created_user, created_org = await user_service.create(
        email=generate_random_email(),
        phone=generate_random_phone(),
        password="password",
        first_name="John",
        middle_name="Doe",
        last_name="Smith",
        is_contractor=False,
        avatar="/usr/avatar",
        org=org,
    )

    assert created_user.password != "password"
    assert created_user.id != ""
    await user_service.user_repository.db.close()
