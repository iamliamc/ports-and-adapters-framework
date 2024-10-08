import yaml
import logging
import re
from typing import Optional


class RunningSettings:
    def __init__(
        self,
        run_web_server: bool = True,
        run_background_jobs: bool = True,
        local_development: bool = False,
        debug: bool = False,
    ):
        self.run_web_server = run_web_server
        self.run_background_jobs = run_background_jobs
        self.local_development = local_development
        self.debug = debug


class BackgroundJobsSettings:
    def __init__(
        self,
        name: str,
        broker: str,
        backend: str,
        task_always_eager: bool,
        task_eager_propagates: bool,
        admin_dashboard_user: str = "",
        admin_dashboard_user_password: str = "",
        result_backend: Optional[str] = None,
        cache_backend: Optional[str] = None,
        broker_connection_retry_on_startup: bool = True,
        task_track_started: bool = True,
        task_send_sent_event: bool = True,
    ):
        self.name = name
        self.broker = broker
        self.backend = backend
        self.task_always_eager = task_always_eager
        self.task_eager_propagates = task_eager_propagates
        self.admin_dashboard_user = admin_dashboard_user
        self.admin_dashboard_user_password = admin_dashboard_user_password
        self.result_backend = result_backend
        self.cache_backend = cache_backend
        self.broker_connection_retry_on_startup = broker_connection_retry_on_startup
        self.task_track_started = task_track_started
        self.task_send_sent_event = task_send_sent_event


class ConfigSettings:
    def __init__(
        self,
        log_level="INFO",
        sentry_url=None,
    ):
        self.log_level = log_level
        self.sentry_url = sentry_url


class DatabaseSettings:
    def __init__(self, connection=None):
        if None in [connection]:
            raise ValueError("Database connection string is required.")
        self.connection = connection


class NoSqlDatabaseSettings:
    def __init__(self, connection=None):
        if None in [connection]:
            raise ValueError("NoSql Database connection string is required.")
        self.connection = connection


class WebServerSettings:
    def __init__(
        self,
        debug=False,
        port=8000,
        swagger_relative_path=None,
        local_development=False,
        host="127.0.0.1",
    ):
        self.port = port
        self.debug = debug
        self.swagger_relative_path = swagger_relative_path
        self.local_development = local_development
        self.host = host


class Settings:
    def __init__(self, settings):
        self.running = RunningSettings(**settings.get("running", {}))
        self.config = ConfigSettings(**settings.get("config", {}))
        self.database = DatabaseSettings(**settings.get("database", {}))
        self.no_sql_database = NoSqlDatabaseSettings(
            **settings.get("no_sql_database", {})
        )
        self.web_server = WebServerSettings(**settings.get("web_server", {}))
        self.background_jobs = BackgroundJobsSettings(
            **settings.get("background_jobs", {})
        )


def load(path):
    with open(path, "r") as stream:
        settings = Settings(yaml.safe_load(stream))
        return settings


def log_config(app_settings, logger=None):
    if logger is None:
        logger = logging.getLogger()

    def _log(key, value, section):
        class_dict = getattr(value, "__dict__", None)

        if isinstance(value, dict):
            for v in value:
                _log(v, value[v], f"{section}|{key}")
        elif class_dict:
            for item in class_dict:
                value = getattr(class_dict, item, None)
                _log(item, value, f"{section}|{key}")
        else:
            # If it's the database section
            if re.search(r"^database", section):
                # Let's mask user and password for database connections'
                match = re.search(r"://(.+)?@", value)
                if match:
                    value = value.replace(match[1], "######")
            logger.info(f"{section} | {key} = {value}")

    logger.info(f"CURRENT SERVER SETTINGS | START")
    for setting in app_settings.__dict__:
        config = getattr(app_settings, setting, None)

        for key in config.__dict__:
            value = getattr(config, key, None)
            _log(key, value, setting)
    logger.info(f"CURRENT SERVER SETTINGS | END")
