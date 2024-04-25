import datetime
import json
import os
import random
import string
import sys
import uuid

import asyncpg
import pytest
from repositories import typesense
from repositories.postgres.schemas import Organization, Tender
from repositories.postgres.tender import TenderRepository
from repositories.postgres.user import UserRepository
from repositories.typesense.tender import TenderIndex
from schemas.create_tender import CreateTenderRequest
from services.manager import ManagerService
from services.tenders import TenderService
from services.user import UserService
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


def generate_random_email():
    username = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=5)
    )
    domain = "".join(random.choices(string.ascii_lowercase, k=3))
    return f"{username}@{domain}.com"


def generate_random_phone():
    return "+7999" + "".join(random.choices(string.digits, k=7))


def generate_random_name():
    names = ["John", "Alice", "Bob", "Emma", "Michael"]
    name = random.choice(names)
    return name


def generate_random_number():
    return random.randint(1000, 9999)


async def postgres_is_responsive(dsn):
    try:
        conn = await asyncpg.connect(dsn=dsn.replace("+asyncpg", ""))

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applied_migrations (
                migration_file TEXT PRIMARY KEY
            )
        """
        )

        migration_dir = "./app/repositories/postgres/migration"
        migration_files = sorted(os.listdir(migration_dir))

        for migration_file in migration_files:
            if migration_file.endswith(".up.sql"):
                if await conn.fetchval(
                    """
                    SELECT 1 FROM applied_migrations WHERE migration_file = $1
                """,
                    migration_file,
                ):
                    print(f"Migration already applied: {migration_file}")
                    continue

                with open(
                    os.path.join(migration_dir, migration_file), "r"
                ) as f:
                    sql = f.read()
                await conn.execute(sql)
                print(f"Applied migration: {migration_file}")

                await conn.execute(
                    """
                    INSERT INTO applied_migrations (migration_file) VALUES ($1)
                """,
                    migration_file,
                )

        await conn.close()

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


@pytest.fixture(scope="session")
async def postgres_session():
    dsn = os.getenv("DB_DSN", "localhost")

    await_time = datetime.datetime.now() + datetime.timedelta(seconds=30)

    while await postgres_is_responsive(dsn=dsn) is False:
        if datetime.datetime.now() > await_time:
            raise Exception("Waiting time is up")

    engine = create_async_engine(dsn.format("+asyncpg"))
    async_session_maker = async_sessionmaker(autocommit=False, bind=engine)
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
def typesense_session():
    client = typesense.get_db_connection()
    yield client


@pytest.fixture(scope="session")
def tender_index(typesense_session):
    folder_path = os.path.join("./app/repositories/typesense/migration")
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as f:
                data = json.load(f)
                typesense_session.collections.create(data)

    yield TenderIndex(db=typesense_session)


@pytest.fixture(scope="session")
async def user_repository(postgres_session):
    return UserRepository(db=postgres_session)


@pytest.fixture(scope="session")
async def tender_repository(postgres_session):
    return TenderRepository(db=postgres_session)


@pytest.fixture(scope="session")
async def user_service(user_repository):
    return UserService(user_repository=user_repository)


@pytest.fixture(scope="session")
async def tender_service(tender_repository, tender_index):
    return TenderService(
        tender_repository=tender_repository, tender_index=tender_index
    )


@pytest.fixture(scope="session")
async def manager_service(user_repository, tender_repository):
    return ManagerService(
        user_repository=user_repository, tender_repository=tender_repository
    )


@pytest.fixture(scope="function")
async def created_user(user_service, postgres_session):
    org = Organization(
        id="org_" + str(uuid.uuid4()),
        brand_name="foobar",
        full_name="ooo full foobar",
        short_name="ooo foobar",
        inn=str(generate_random_number()),
        okpo=str(generate_random_number()),
        ogrn=str(generate_random_number()),
        kpp=str(generate_random_number()),
        tax_code=456,
        address="st. foobar",
        email="mail@foo.bar",
        phone="+79998989999",
    )

    created_user = await user_service.create(
        email=generate_random_email(),
        phone=generate_random_phone(),
        password="password",
        first_name=generate_random_name(),
        middle_name=generate_random_name(),
        last_name=generate_random_name(),
        is_contractor=False,
        avatar="/usr/avatar",
        org=org,
    )

    return created_user


@pytest.fixture(scope="function")
async def created_tender(tender_service, created_user, postgres_session):
    tender = CreateTenderRequest(
        name="Office cleaning",
        price=100000,
        is_contract_price=False,
        city_id=1,
        floor_space=200,
        description="I need to clean office in Moscow city.",
        attachments=["some.link", "foo.bar"],
        wishes="As quickly as possible",
        services_types=[1],
        reception_start=datetime.datetime.now(),
        reception_end=datetime.datetime.now() + datetime.timedelta(days=30),
        work_start=datetime.datetime.now(),
        work_end=datetime.datetime.now(),
        objects_types=[1],
    )

    created_tender = await tender_service.create_tender(
        tender, created_user.id
    )

    yield created_tender
    await postgres_session.execute(
        delete(Tender).where(Tender.id == created_tender.id)
    )
