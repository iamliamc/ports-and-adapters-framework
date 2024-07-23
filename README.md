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