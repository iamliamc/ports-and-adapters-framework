# setup
import logging
from sensor_app import settings
import sensor_app.adapters.secondary.persistence_sql as ps
from sensor_app.core.use_cases import sensor as sensor_use_case
from sensor_app.adapters.primary.web_server.fast_api_app import create_fastapi_app


def serve():
    try:
        if app_settings.running.run_web_server is True:
            # REST server
            app = create_fastapi_app(
                web_server_settings=app_settings.web_server,
                sensor_repo=ps.AsyncpgSensorRepository(
                    app_settings.database.connection
                ),
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
app = serve()
