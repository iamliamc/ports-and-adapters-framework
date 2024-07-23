import os
import pytest
import asyncpg
import dotenv
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

@pytest.fixture(scope='session')
def database_url():
    # Load environment variables from .env file
    load_dotenv()
    db_url = os.getenv('TEST_DATABASE_URL')
    if not db_url:
        raise ValueError("No TEST_DATABASE_URL set for pytest configuration")
    print(db_url)
    import pdb; pdb.set_trace()
    return db_url

@pytest.fixture(scope='function')
async def db_connection(database_url):
    conn = await asyncpg.connect(database_url)
    try:
        yield conn
    finally:
        await conn.close()

@pytest.fixture(scope='function', autouse=True)
async def clean_db(db_connection):
    tables = ['sensors']
    async with db_connection.transaction():
        for table in tables:
            await db_connection.execute(f'TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;')

@pytest.fixture(scope='session', autouse=True)
def run_migrations(database_url):
    """Run Alembic migrations before any tests are run."""
    alembic_cfg = Config("alembic.ini")  # Path to your alembic configuration file
    alembic_cfg.set_main_option('sqlalchemy.url', database_url)
    command.upgrade(alembic_cfg, "head")