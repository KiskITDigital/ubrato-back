import datetime
import os
import sys

import psycopg2
import pytest
from repositories.postgres import TenderRepository, UserRepository
from repositories.postgres.schemas import Organization, Tender, User
from repositories.typesense.client import get_db_connection
from repositories.typesense.tender import TenderIndex
from schemas.create_tender import CreateTenderRequest
from services import ManagerService, TenderService, UserService
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

# Get the path of the parent directory of 'app' (i.e., the project root)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.insert(0, project_root)


def postgres_is_responsive(db_addr, port):
    try:
        conn = psycopg2.connect(
            database="test",
            user="postgres",
            password="12345",
            host=db_addr,
            port=port,
        )
        migration_dir = "./app/repositories/postgres/migration"
        migration_files = sorted(os.listdir(migration_dir))

        cursor = conn.cursor()

        for migration_file in migration_files:
            if migration_file.endswith(".up.sql"):
                with open(
                    os.path.join(migration_dir, migration_file), "r"
                ) as f:
                    sql = f.read()
                cursor.execute(sql)
                conn.commit()
                print(f"Applied migration: {migration_file}")
        conn.close()

        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def postgres_db_instance():
    port = 5432
    db_addr = os.getenv("DB_ADDR", "localhost")

    dsn = "postgresql+psycopg2://postgres:12345@{}:{}/test?sslmode=disable".format(
        db_addr, port
    )

    await_time = datetime.datetime.now() + datetime.timedelta(seconds=30)

    while postgres_is_responsive(db_addr=db_addr, port=port) is False:
        if datetime.datetime.now() > await_time:
            raise Exception(f"Waiting time is up. Addr: {dsn}")

    engine = create_engine(dsn, pool_size=20, max_overflow=0)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db: scoped_session[Session] = scoped_session(SessionLocal)

    yield db


@pytest.fixture(scope="session")
def typesense_session():
    client = get_db_connection()
    yield client


@pytest.fixture(scope="session")
def postgres_session(postgres_db_instance):
    db_connection = postgres_db_instance
    yield db_connection
    db_connection.close()


@pytest.fixture(scope="module")
def user_repository(postgres_session):
    yield UserRepository(db=postgres_session)
    postgres_session.query(Organization).delete()
    postgres_session.flush()
    postgres_session.query(User).delete()
    postgres_session.commit()


@pytest.fixture(scope="module")
def tender_repository(postgres_session):
    yield TenderRepository(db=postgres_session)
    postgres_session.query(Tender).delete()
    postgres_session.flush()
    postgres_session.query(Organization).delete()
    postgres_session.flush()
    postgres_session.query(User).delete()
    postgres_session.commit()


@pytest.fixture(scope="module")
def tender_index(typesense_session):
    yield TenderIndex(db=typesense_session)


@pytest.fixture(scope="module")
def user_service(user_repository):
    return UserService(user_repository=user_repository)


@pytest.fixture(scope="module")
def tender_service(tender_repository, tender_index):
    return TenderService(
        tender_repository=tender_repository, tender_index=tender_index
    )


@pytest.fixture(scope="module")
def manager_service(user_repository, tender_repository):
    return ManagerService(
        user_repository=user_repository, tender_repository=tender_repository
    )


@pytest.fixture(scope="function")
def created_user(user_service, postgres_session):
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
    postgres_session.query(Organization).filter_by(user_id=created_user.id).delete()
    postgres_session.flush()
    postgres_session.query(User).filter_by(id=created_user.id).delete()
    postgres_session.commit()


@pytest.fixture(scope="function")
def created_tender(tender_service, created_user, postgres_session):
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
        reception_start=datetime.datetime.now(),
        reception_end=datetime.datetime.now() + datetime.timedelta(days=30),
        work_start=datetime.datetime.now(),
        work_end=datetime.datetime.now(),
        object_group_id=1,
        object_type_id=1,
    )

    created_tender = tender_service.create_tender(tender, created_user.id)

    yield created_tender
    postgres_session.query(Tender).filter_by(id=created_tender.id).delete()
    postgres_session.commit()
