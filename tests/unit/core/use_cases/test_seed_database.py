import pytest
from sensor_app.core.use_cases.seed_database import SeedDatabase


@pytest.fixture
def use_case_seed_database(no_sql_device_type_repo, no_sql_device_repo, no_sql_installation_repo):
    return SeedDatabase(
        installation_repo=no_sql_installation_repo,
        device_type_repo=no_sql_device_type_repo,
        device_repo=no_sql_device_repo,
    )

@pytest.mark.asyncio
async def test_seed_database(use_case_seed_database):
    await use_case_seed_database(seed_filepath="tests/unit/core/use_cases/test_seed.json")