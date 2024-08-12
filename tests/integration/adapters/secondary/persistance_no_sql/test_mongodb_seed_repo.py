import pytest
from sensor_app.core.domain.entities import Sensor


@pytest.mark.asyncio
async def test_initalize_database(no_sql_seed_repo, test_logger):
    await no_sql_seed_repo.initalize_database(seed_filepath="tests/integration/adapters/secondary/persistance_no_sql/test_seed.json")
