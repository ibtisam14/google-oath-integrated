from django.apps import AppConfig

class JobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job'

    def ready(self):
        # Import only when the app is ready
        from .cron_runner import start_weather_cron
        print("🚀 Starting background weather cron...")
        start_weather_cron()
