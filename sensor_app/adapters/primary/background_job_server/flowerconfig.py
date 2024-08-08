from sensor_app.main import app_settings


# Max tasks: 10000
max_tasks = 1000

# Enable debug logging: 'DEBUG'

if app_settings.running.run_background_jobs:
    logging = "DEBUG"
else:
    logging = "INFO"

# Web server address: '0.0.0.0'
address = "0.0.0.0"

# Refresh dashboards automatically: True
auto_refresh = True

# Run the http server on a given port: 5555
port = 5555

# Enable support of X-Real-Ip and X-Scheme headers: True
xheaders = True

# A database file to use if persistent mode is enabled: 'sensor_app/adapters/primary/background_job_server/flower.db'
db = "sensor_app/adapters/primary/background_job_server/flower.db"

# Enable persistent mode. If the persistent mode is enabled Flower saves the current state and reloads on restart
persistent = True

background_job_settings = app_settings.background_jobs

# Auth for admin panel: ['user:password']
if (
    background_job_settings.admin_dashboard_user
    and background_job_settings.admin_dashboard_user_password
):
    basic_auth = [
        f"{background_job_settings.admin_dashboard_user}:{background_job_settings.admin_dashboard_user_password}"
    ]
