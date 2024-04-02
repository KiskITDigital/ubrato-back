from models.user import UserPrivateDTO
from repositories.schemas import Organization


def test_create_user(user_service):
    org = Organization(
        id="org_123123",
        brand_name="test",
        short_name="ooo test",
        inn="123",
        okpo="123",
        ogrn="123",
        kpp="123",
        tax_code=123,
        address="st. test",
    )

    created_user = user_service.create(
        email="test@example.com",
        phone="+79999999999",
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


def test_get_user_by_email(user_service, created_user):
    user = user_service.get_by_email(email=created_user.email)

    assert user == created_user


def test_get_user_by_id(user_service, created_user):
    user = user_service.get_by_id(id=created_user.id)

    assert user == UserPrivateDTO(**created_user.__dict__)


def test_get_upd_avatar(user_service, created_user):
    user_service.upd_avatar(user_id=created_user.id, avatar="/new/link")

    user = user_service.get_by_id(id=created_user.id)

    assert user.avatar == "/new/link"
    assert user.avatar != created_user.avatar


def test_password_valid(user_service, created_user):
    result = user_service.password_valid(
        hashed_password=created_user.password, password="password"
    )

    assert result is True
