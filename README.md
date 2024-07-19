Creating a ports and adapters (also known as hexagonal architecture) style application involves defining clear interfaces (ports) for communication with the outside world, and implementing these interfaces with specific technologies (adapters). Here's a step-by-step guide on how to structure a Python3 application using `asyncpg` for asynchronous database interactions and `pydantic` for data validation and serialization. We'll also use `alembic` for database migrations.

### Step 1: Setting Up the Project

First, let's set up the project structure:

```
my_app/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
├── my_app/
│   ├── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── db_adapter.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── ports.py
│   │   ├── services.py
│   ├── main.py
├── tests/
│   ├── __init__.py
│   ├── test_services.py
├── alembic.ini
├── requirements.txt
└── setup.py
```

### Step 2: Install Dependencies

Add the following dependencies to your `requirements.txt`:

```
asyncpg==0.23.0
pydantic==1.8.2
alembic==1.6.5
pytest==6.2.4
pytest-asyncio==0.14.0
```

### Step 3: Configure Alembic

Initialize Alembic by running:

```sh
alembic init alembic
```

Edit `alembic.ini` to configure your database URL.

Update `alembic/env.py` to use `asyncpg`:

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from my_app.core.models import Base  # Import your models here

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Step 4: Define the Core Domain Model

In `my_app/core/models.py`, define the `Sensor` model using `pydantic`:

```python
from pydantic import BaseModel
from typing import Optional

class Sensor(BaseModel):
    id: Optional[int] = None
    name: str
    value: float
```

### Step 5: Define the Ports

In `my_app/core/ports.py`, define the repository interface:

```python
from typing import Protocol, List
from my_app.core.models import Sensor

class SensorRepository(Protocol):
    async def create_sensor(self, sensor: Sensor) -> Sensor:
        pass

    async def get_sensor(self, sensor_id: int) -> Sensor:
        pass

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        pass

    async def delete_sensor(self, sensor_id: int) -> None:
        pass

    async def list_sensors(self) -> List[Sensor]:
        pass
```

### Step 6: Implement the Adapters

In `my_app/adapters/db_adapter.py`, implement the `SensorRepository` using `asyncpg`:

```python
import asyncpg
from typing import List
from my_app.core.models import Sensor
from my_app.core.ports import SensorRepository

class AsyncpgSensorRepository(SensorRepository):
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def _get_connection(self):
        return await asyncpg.connect(self.database_url)

    async def create_sensor(self, sensor: Sensor) -> Sensor:
        conn = await self._get_connection()
        async with conn.transaction():
            row = await conn.fetchrow(
                "INSERT INTO sensors (name, value) VALUES ($1, $2) RETURNING id, name, value",
                sensor.name, sensor.value
            )
        await conn.close()
        return Sensor(**row)

    async def get_sensor(self, sensor_id: int) -> Sensor:
        conn = await self._get_connection()
        row = await conn.fetchrow(
            "SELECT id, name, value FROM sensors WHERE id = $1",
            sensor_id
        )
        await conn.close()
        if row:
            return Sensor(**row)
        return None

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        conn = await self._get_connection()
        async with conn.transaction():
            row = await conn.fetchrow(
                "UPDATE sensors SET name = $1, value = $2 WHERE id = $3 RETURNING id, name, value",
                sensor.name, sensor.value, sensor.id
            )
        await conn.close()
        return Sensor(**row)

    async def delete_sensor(self, sensor_id: int) -> None:
        conn = await self._get_connection()
        async with conn.transaction():
            await conn.execute(
                "DELETE FROM sensors WHERE id = $1",
                sensor_id
            )
        await conn.close()

    async def list_sensors(self) -> List[Sensor]:
        conn = await self._get_connection()
        rows = await conn.fetch(
            "SELECT id, name, value FROM sensors"
        )
        await conn.close()
        return [Sensor(**row) for row in rows]
```

### Step 7: Create the Application Services

In `my_app/core/services.py`, implement the application services:

```python
from typing import List
from my_app.core.models import Sensor
from my_app.core.ports import SensorRepository

class SensorService:
    def __init__(self, repository: SensorRepository):
        self.repository = repository

    async def create_sensor(self, sensor: Sensor) -> Sensor:
        return await self.repository.create_sensor(sensor)

    async def get_sensor(self, sensor_id: int) -> Sensor:
        return await self.repository.get_sensor(sensor_id)

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        return await self.repository.update_sensor(sensor)

    async def delete_sensor(self, sensor_id: int) -> None:
        await self.repository.delete_sensor(sensor_id)

    async def list_sensors(self) -> List[Sensor]:
        return await self.repository.list_sensors()
```

### Step 8: Set Up Tests

In `tests/test_services.py`, set up the tests using `pytest` and `pytest-asyncio`:

```python
import pytest
import asyncio
from my_app.core.models import Sensor
from my_app.core.services import SensorService
from my_app.adapters.db_adapter import AsyncpgSensorRepository

DATABASE_URL = "postgresql://user:password@localhost/test_db"

@pytest.fixture
async def sensor_service():
    repository = AsyncpgSensorRepository(DATABASE_URL)
    return SensorService(repository)

@pytest.mark.asyncio
async def test_create_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    assert created_sensor.id is not None
    assert created_sensor.name == "Test Sensor"
    assert created_sensor.value == 123.45

@pytest.mark.asyncio
async def test_get_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    fetched_sensor = await sensor_service.get_sensor(created_sensor.id)
    assert fetched_sensor == created_sensor

@pytest.mark.asyncio
async def test_update_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    created_sensor.value = 678.90
    updated_sensor = await sensor_service.update_sensor(created_sensor)
    assert updated_sensor.value == 678.90

@pytest.mark.asyncio
async def test_delete_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45

)
    created_sensor = await sensor_service.create_sensor(sensor)
    await sensor_service.delete_sensor(created_sensor.id)
    deleted_sensor = await sensor_service.get_sensor(created_sensor.id)
    assert deleted_sensor is None

@pytest.mark.asyncio
async def test_list_sensors(sensor_service):
    sensor1 = Sensor(name="Test Sensor 1", value=123.45)
    sensor2 = Sensor(name="Test Sensor 2", value=678.90)
    await sensor_service.create_sensor(sensor1)
    await sensor_service.create_sensor(sensor2)
    sensors = await sensor_service.list_sensors()
    assert len(sensors) >= 2
```

### Step 9: Run Alembic Migrations

Create the `sensors` table using Alembic:

```sh
alembic revision --autogenerate -m "create sensors table"
alembic upgrade head
```

Make sure to define the `sensors` table in your models for Alembic to pick up the schema.

### Step 10: Running the Tests

Finally, run the tests using `pytest`:

```sh
pytest
```

This structure follows the ports and adapters architecture, with clear separation between the core domain logic, the repository interface (port), and the database adapter implementation. The tests ensure that the core services function correctly, independently of the specific database implementation.

Sure! Here's how to proceed with creating the migration script and setting up a Docker container for the tests using `docker-compose`.

### Step 1: Create the Migration Script

First, let's define the migration script for the `sensors` table. Assuming you have already set up Alembic, you can generate the initial migration script:

```sh
alembic revision --autogenerate -m "create sensors table"
```

Edit the generated migration script in `alembic/versions/<revision_id>_create_sensors_table.py` to include the schema for the `sensors` table:

```python
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '<revision_id>'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'sensors',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('value', sa.Float, nullable=False)
    )

def downgrade():
    op.drop_table('sensors')
```

### Step 2: Create a Docker Compose File

Create a `docker-compose.yml` file to define the services required for running the tests. This includes a PostgreSQL container for the database.

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: test_db
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  alembic:
    image: python:3.9
    volumes:
      - .:/app
    working_dir: /app
    command: >
      sh -c "pip install -r requirements.txt &&
             alembic upgrade head"

volumes:
  db_data:
```

### Step 3: Update the Database URL in Configuration

Update your database URL in the configuration to match the settings in `docker-compose.yml`:

```python
DATABASE_URL = "postgresql://user:password@db/test_db"
```

### Step 4: Run the Docker Compose Services

Start the Docker services:

```sh
docker-compose up -d
```

This will start the PostgreSQL container and run the Alembic migrations.

### Step 5: Run the Tests

Run the tests in the context of the Docker Compose setup:

```sh
docker-compose run --rm alembic pytest
```

### Step 6: Cleanup

After running the tests, you can stop and remove the containers:

```sh
docker-compose down
```

This setup ensures that your tests run against a containerized PostgreSQL database, providing a consistent and isolated environment for testing.

To ensure the test database is cleaned between tests, you can use a fixture in `pytest` that truncates all tables before each test runs. This guarantees a clean state for every test. 

Here’s how to implement it:

### Step 1: Create a Truncation Fixture

Create a `conftest.py` file in your `tests` directory, which will contain the `pytest` fixtures:

```python
import pytest
import asyncpg

DATABASE_URL = "postgresql://user:password@db/test_db"

@pytest.fixture(scope='function')
async def db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
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
```

### Step 2: Update Tests to Use the Fixture

Update your test cases to use the `db_connection` fixture. This fixture will automatically clean the database before each test function.

Here’s an example of how your test file would look:

```python
import pytest
from my_app.core.models import Sensor
from my_app.core.services import SensorService
from my_app.adapters.db_adapter import AsyncpgSensorRepository

DATABASE_URL = "postgresql://user:password@db/test_db"

@pytest.fixture
async def sensor_service():
    repository = AsyncpgSensorRepository(DATABASE_URL)
    return SensorService(repository)

@pytest.mark.asyncio
async def test_create_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    assert created_sensor.id is not None
    assert created_sensor.name == "Test Sensor"
    assert created_sensor.value == 123.45

@pytest.mark.asyncio
async def test_get_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    fetched_sensor = await sensor_service.get_sensor(created_sensor.id)
    assert fetched_sensor == created_sensor

@pytest.mark.asyncio
async def test_update_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    created_sensor.value = 678.90
    updated_sensor = await sensor_service.update_sensor(created_sensor)
    assert updated_sensor.value == 678.90

@pytest.mark.asyncio
async def test_delete_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    await sensor_service.delete_sensor(created_sensor.id)
    deleted_sensor = await sensor_service.get_sensor(created_sensor.id)
    assert deleted_sensor is None

@pytest.mark.asyncio
async def test_list_sensors(sensor_service):
    sensor1 = Sensor(name="Test Sensor 1", value=123.45)
    sensor2 = Sensor(name="Test Sensor 2", value=678.90)
    await sensor_service.create_sensor(sensor1)
    await sensor_service.create_sensor(sensor2)
    sensors = await sensor_service.list_sensors()
    assert len(sensors) >= 2
```

### Step 3: Run the Tests

Run the tests as before:

```sh
docker-compose run --rm alembic pytest
```

This setup ensures that the database is cleaned before each test runs, maintaining a consistent state across tests.