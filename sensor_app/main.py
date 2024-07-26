# setup
import logging
from celery import Celery
from sensor_app import settings
import sensor_app.adapters.secondary.persistence_sql as ps
import sensor_app.adapters.secondary.background_jobs_celery as bjc
from sensor_app.adapters.primary.web_server.fast_api_app import create_fastapi_app
from sensor_app.adapters.secondary.background_jobs_celery.background_jobs_repo import create_celery_app, BackgroundJobsRepository

def serve():
    try:
        if app_settings.running.run_web_server is True:
            # REST server
            app = create_fastapi_app(
                web_server_settings=app_settings.web_server,
                background_jobs_repo=bjc.CeleryBackgroundJobRepo(app_settings.background_jobs),
                sensor_repo=ps.AsyncpgSensorRepository(
                    app_settings.database.connection
                ),
            )
            return app

    except Exception as e:
        logger.exception(e)

def start_background_worker() -> Celery:
    try: 
        if app_settings.running.run_background_jobs is True:
            app = create_celery_app(
                background_job_settings=app_settings.background_jobs,
                sensor_repo=ps.AsyncpgSensorRepository(
                    app_settings.database.connection
                )
            )
            return app
    except Exception as e:
        logger.exception(e)

app_settings = settings.load("./sensor_app/settings.yaml")

if (
    app_settings.config.sentry_url
    and app_settings.running.local_development is not True
):
    # TODO configure observability
    None

logger = logging.getLogger()

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(app_settings.config.log_level)

settings.log_config(app_settings, logger)
background_worker = start_background_worker()
app = serve()
