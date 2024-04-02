import datetime
import os
import sys

import psycopg2
import pytest
from repositories import TenderRepository, UserRepository
from repositories.schemas import Organization, Tender, User
from schemas.create_tender import CreateTenderRequest
from services import ManagerService, TenderService, UserService
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

# Get the path of the parent directory of 'app' (i.e., the project root)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "docker-compose.yml")


@pytest.fixture(scope="session")
def docker_compose_command() -> str:
    return ""


@pytest.fixture(scope="session")
def docker_cleanup() -> str:
    return "down"


def is_responsive(docker_ip, port):
    try:
        psycopg2.connect(
            database="postgres",
            user="postgres",
            password="12345",
            host=docker_ip,
            port=port,
        )
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def db_instance(docker_ip):
    """Ensure that postgres is up and responsive."""

    port = 35432
    dsn = "postgresql+psycopg2://postgres:12345@{}:{}/test?sslmode=disable".format(
        docker_ip, port
    )

    engine = create_engine(dsn, pool_size=20, max_overflow=0)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db: scoped_session[Session] = scoped_session(SessionLocal)
    yield db


@pytest.fixture(scope="session")
def session(db_instance):
    """
    Create a Session, close after test session, uses `db_instance` fixture
    """

    db_connection = db_instance
    yield db_connection
    db_connection.close()


@pytest.fixture(scope="module")
def user_repository(session):
    yield UserRepository(db=session)
    session.query(Organization).delete()
    session.flush()
    session.query(User).delete()
    session.commit()


@pytest.fixture(scope="module")
def tender_repository(session):
    yield TenderRepository(db=session)
    session.query(Tender).delete()
    session.flush()
    session.query(Organization).delete()
    session.flush()
    session.query(User).delete()
    session.commit()


@pytest.fixture(scope="module")
def user_service(user_repository):
    return UserService(user_repository=user_repository)


@pytest.fixture(scope="module")
def tender_service(tender_repository):
    return TenderService(tender_repository=tender_repository)


@pytest.fixture(scope="module")
def manager_service(user_repository, tender_repository):
    return ManagerService(
        user_repository=user_repository, tender_repository=tender_repository
    )


@pytest.fixture(scope="function")
def created_user(user_service, session):
    org = Organization(
        id="org_456",
        brand_name="foobar",
        short_name="ooo foobar",
        inn="456",
        okpo="456",
        ogrn="456",
        kpp="456",
        tax_code=456,
        address="st. foobar",
    )

    created_user = user_service.create(
        email="example@test.com",
        phone="+79899898989",
        password="password",
        first_name="John",
        middle_name="Doe",
        last_name="Smith",
        is_contractor=False,
        avatar="/usr/avatar",
        org=org,
    )

    yield created_user
    session.query(Organization).filter_by(user_id=created_user.id).delete()
    session.flush()
    session.query(User).filter_by(id=created_user.id).delete()
    session.commit()


@pytest.fixture(scope="function")
def created_tender(tender_service, created_user, session):
    tender = CreateTenderRequest(
        name="Office cleaning",
        price=100000,
        is_contract_price=False,
        location="Moscow",
        floor_space=200,
        description="I need to clean office in Moscow city.",
        attachments=["some.link", "foo.bar"],
        wishes="As quickly as possible",
        services_groups=[1],
        services_types=[1],
        reception_start=datetime.datetime.now(),
        reception_end=datetime.datetime.now() + datetime.timedelta(days=30),
        work_start=datetime.datetime.now(),
        work_end=datetime.datetime.now(),
        object_group_id=1,
        object_type_id=1,
    )

    created_tender = tender_service.create_tender(tender, created_user.id)

    yield created_tender
    session.query(Tender).filter_by(id=created_tender.id).delete()
    session.commit()
