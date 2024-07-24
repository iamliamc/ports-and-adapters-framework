import os
import yaml
from sensor_app.settings import DatabaseSettings

class Settings:
    def __init__(self, settings):
        self.database = DatabaseSettings(**settings.get("database", {}))

def load(path=os.path.join("tests", "integration", "test_settings.yaml")):
    if os.path.isfile(path):
        with open(path, "r") as stream:
            settings = yaml.safe_load(stream)

    else:
        settings = {}

    return Settings(settings)