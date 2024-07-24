import os
import logging
import asyncio
import pytest
import pytest_asyncio
import asyncpg
import dotenv
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

@pytest.fixture(scope="session")
def test_logger():
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    return logger


@pytest.fixture(scope='session')
def database_url():
    # Load environment variables from .env file
    load_dotenv()
    db_url = os.getenv('TEST_DATABASE_URL')
    if not db_url:
        raise ValueError("No TEST_DATABASE_URL set for pytest configuration")
    print(db_url)
    return db_url

async def truncate_all_tables():
        # List all table names in the database
    conn = await asyncpg.connect(os.getenv('TEST_DATABASE_URL'))
    try: 
        tables = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        
        table_names = [table['table_name'] for table in tables]

        # Generate TRUNCATE TABLE commands for all tables
        if table_names:
            truncate_commands = [f'TRUNCATE TABLE {table_name} CASCADE;' for table_name in table_names]
            truncate_query = ' '.join(truncate_commands)
            await conn.execute(truncate_query)
    finally:
        await conn.close()

@pytest_asyncio.fixture(scope='function')
async def db_connection(database_url):
    conn = await asyncpg.connect(database_url)
    try:
        yield conn
    finally:
        await conn.close()

@pytest_asyncio.fixture(scope='session', autouse=True)
def run_migrations(database_url, test_logger):
    """Run Alembic migrations before any tests are run."""
    alembic_cfg = Config("alembic.ini")  # Path to your alembic configuration file
    alembic_cfg.set_main_option('sqlalchemy.url', database_url)
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        test_logger.error(e)


@pytest_asyncio.fixture(scope='function', autouse=True)
async def clean_db():
    await truncate_all_tables()

    yield

    await truncate_all_tables()