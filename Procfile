# Procfile
web: uvicorn sensor_app.main:app --reload
worker: celery -A sensor_app.main.background_worker worker --loglevel=debug
flower: celery -A sensor_app.main.background_worker flower --conf=sensor_app/adapters/primary/background_job_server/flowerconfig.py
