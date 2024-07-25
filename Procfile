# Procfile
web: uvicorn sensor_app.main:app --reload
worker: celery -A sensor_app.main.background_worker worker --loglevel=debug
