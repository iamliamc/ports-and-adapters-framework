import os
import yaml
from sensor_app.settings import (
    DatabaseSettings,
    NoSqlDatabaseSettings,
    WebServerSettings,
    BackgroundJobsSettings,
    RunningSettings,
)


class Settings:
    def __init__(self, settings):
        self.database = DatabaseSettings(**settings.get("database", {}))
        self.no_sql_database = NoSqlDatabaseSettings(
            **settings.get("no_sql_database", {})
        )
        self.web_server_settings = WebServerSettings(**settings.get("web_server"))
        self.background_jobs = BackgroundJobsSettings(**settings.get("background_jobs"))
        self.running = RunningSettings(**settings.get("running"))


def load(path=os.path.join("tests", "integration", "test_settings.yaml")):
    if os.path.isfile(path):
        with open(path, "r") as stream:
            settings = yaml.safe_load(stream)

    else:
        settings = {}

    return Settings(settings)
