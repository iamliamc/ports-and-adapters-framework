import logging
import pytest
import pytest_asyncio
import asyncpg
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime import migration
from sqlalchemy import create_engine

from tests.integration import settings

test_settings = settings.load()

@pytest.fixture(scope='session')
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
        raise ValueError("No test_settings.database.connection set for pytest configuration need to update tests/test_settings.yaml")
    test_logger.debug(db_url)
    return db_url


async def truncate_all_tables():
    # List all table names in the database
    conn = await asyncpg.connect(test_settings.database.connection)
    try:
        tables = await conn.fetch(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
        )

        table_names = [table["table_name"] for table in tables]
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
def run_migrations(database_url, test_logger):
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
