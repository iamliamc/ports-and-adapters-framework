import logging
import pytest
import pytest_asyncio
import asyncpg
import asyncio
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime import migration
from sqlalchemy import create_engine
from motor.motor_asyncio import AsyncIOMotorClient
from sensor_app.adapters.secondary.persistence_sql.sensor_repo import (
    AsyncpgSensorRepository,
)
from sensor_app.adapters.secondary.persistence_mongodb.sensor_repo import (
    MongoDBSensorRepository,
)
from sensor_app.adapters.secondary.persistence_mongodb.seed_repo import (
    MongoDBSeedRepository,
)
from sensor_app.adapters.secondary.persistence_mongodb.device_type_repo import (
    MongoDBDeviceTypeRepository,
)
from sensor_app.adapters.secondary.persistence_mongodb.device_repo import (
    MongoDBDeviceRepository,
)
from tests.integration import settings

test_settings = settings.load()


@pytest.fixture(scope="session")
def conftest_settings():
    return test_settings


@pytest.fixture(scope="session")
def test_logger():
    logger = logging.getLogger()
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    return logger


@pytest.fixture(scope="session")
def database_url(test_logger):
    # Load environment variables from .env file
    db_url = test_settings.database.connection
    if not db_url:
        raise ValueError(
            "No test_settings.database.connection set for pytest configuration need to update tests/test_settings.yaml"
        )
    test_logger.debug(db_url)
    return db_url


@pytest.fixture(scope="session")
def no_sql_database_url(test_logger):
    # Load environment variables from .env file
    db_url = test_settings.no_sql_database.connection
    if not db_url:
        raise ValueError(
            "No test_settings.no_sql_database.connection set for pytest configuration need to update tests/test_settings.yaml"
        )
    test_logger.debug(db_url)
    return db_url


async def get_table_names():
    # List all table names in the database
    conn = await asyncpg.connect(test_settings.database.connection)

    tables = await conn.fetch(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """
    )
    return tables


async def truncate_all_tables():
    conn = await asyncpg.connect(test_settings.database.connection)
    try:
        tables = await get_table_names()
        table_names = [table["table_name"] for table in tables]

        if "alembic_version" in table_names:
            table_names.remove("alembic_version")

        # Generate TRUNCATE TABLE commands for all data tables
        if table_names:
            truncate_commands = [
                f"TRUNCATE TABLE {table_name} CASCADE;" for table_name in table_names
            ]
            truncate_query = " ".join(truncate_commands)
            await conn.execute(truncate_query)
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="function")
async def db_connection(database_url):
    conn = await asyncpg.connect(database_url)
    try:
        yield conn
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def run_migrations(database_url, test_logger):
    """Run Alembic migrations before any tests are run."""
    alembic_cfg = Config("alembic.ini")  # Path to your alembic configuration file
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    # Get the Alembic script directory
    script_directory = ScriptDirectory.from_config(alembic_cfg)

    # Create an SQLAlchemy engine
    engine = create_engine(database_url)

    # Get the current revision in the database
    with engine.connect() as connection:
        context = migration.MigrationContext.configure(connection)
        current_revision = context.get_current_revision()

    # Get the latest revision (HEAD) from the script directory
    head_revision = script_directory.get_current_head()
    if current_revision != head_revision:
        test_logger.info(
            f"Running migrations from {current_revision} to {head_revision}"
        )
        try:
            table_names = await get_table_names()
            if "alemibic_version" not in table_names:
                command.stamp(alembic_cfg, "base")
            command.upgrade(alembic_cfg, "head")
        except Exception as e:
            test_logger.error(f"Failed attempt to run migrations: {e}")
            raise
    else:
        test_logger.info("Already at HEAD. No migration needed.")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db():
    await truncate_all_tables()

    yield

    await truncate_all_tables()


@pytest_asyncio.fixture(scope="session")
async def no_sql_db_client(no_sql_database_url):
    """Fixture to create and close an async database client."""
    client = AsyncIOMotorClient(no_sql_database_url)
    client.get_io_loop = asyncio.get_event_loop
    yield client

    client.close()


async def truncate_all_mongodb_collections(no_sql_db_client):
    database = no_sql_db_client.get_default_database()  # get db based on db name in URL
    # Cleanup after each test
    collections = await database.list_collection_names()
    for collection in collections:
        await database[collection].delete_many({})


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_no_sql_db(no_sql_db_client):
    await truncate_all_mongodb_collections(no_sql_db_client=no_sql_db_client)

    yield

    await truncate_all_mongodb_collections(no_sql_db_client=no_sql_db_client)


@pytest.fixture
def sensor_repo(conftest_settings):
    return AsyncpgSensorRepository(conftest_settings.database.connection)


@pytest.fixture
def no_sql_sensor_repo(conftest_settings):
    return MongoDBSensorRepository(conftest_settings.no_sql_database.connection)

@pytest.fixture
def no_sql_seed_repo(conftest_settings):
    return MongoDBSeedRepository(conftest_settings.no_sql_database.connection)

@pytest.fixture
def no_sql_device_type_repo(conftest_settings):
    return MongoDBDeviceTypeRepository(conftest_settings.no_sql_database.connection)

@pytest.fixture
def no_sql_device_repo(conftest_settings):
    return MongoDBDeviceRepository(conftest_settings.no_sql_database.connection)