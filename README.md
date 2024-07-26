Create a python virtual environment for this project:
`python3 -m venv venv`

Activate your environment:
`source venv/bin/activate`

Install dependencies: 
`pip install -r requirements.txt`

Run tests: 
`pytest tests`

Running databases
`docker-compose up -d`

```
(venv) liamconsidine@CQQ27KJ4GL ports-and-adapters-framework % docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                    NAMES
0313c9bd6269   postgres:13   "docker-entrypoint.s…"   14 seconds ago   Up 13 seconds   0.0.0.0:5433->5432/tcp   ports-and-adapters-framework-postgres_test-1
0e97aa9f3fa1   postgres:13   "docker-entrypoint.s…"   14 seconds ago   Up 13 seconds   0.0.0.0:5432->5432/tcp   ports-and-adapters-framework-postgres_dev-1
```

To get into the database manually:
`docker exec -it CONTAINER_ID psql -U dev_user -d dev_db`
`docker-compose logs postgres_dev`

Basic postgres inspection: 
`\l` list databases
`\c dev_db` connect to the dev_db
`\dt` list tables


Do we want Alembic create migrations based on ORM models?

```
    alembic revision --autogenerate -m "create sensors table"
    alembic upgrade head
```

Run the application
`uvicorn sensor_app.main:app --reload`

Some type checking:

`mypy sensor_app`
```Success: no issues found in 20 source files```

### Swagger Documentation: 
http://localhost:8000/docs

### With Celery connected to postgres it creates these tables need to make tests work... 
```
                 List of relations
 Schema |        Name         |   Type   |  Owner
--------+---------------------+----------+----------
 public | alembic_version     | table    | dev_user
 public | celery_taskmeta     | table    | dev_user
 public | celery_tasksetmeta  | table    | dev_user
 public | sensors             | table    | dev_user
 public | sensors_id_seq      | sequence | dev_user
 public | task_id_sequence    | sequence | dev_user
 public | taskset_id_sequence | sequence | dev_user

 ```


 ### Flower: 
 Visit it at http://0.0.0.0:5555

```
 FastAPI background tasks are a good fit for lightweight applications that need to perform simple background tasks, such as logging or updating a database. They are simple to set up and integrate seamlessly with FastAPI web applications, making them a good choice for developers who want a simple and lightweight solution.

On the other hand, Celery is a good choice for more complex applications that need to handle a large volume of tasks, or require more advanced scheduling features. Celery’s distributed architecture allows it to handle large volumes of tasks, and its Celery Beat scheduling functionality makes it a powerful tool for scheduling periodic tasks.
```