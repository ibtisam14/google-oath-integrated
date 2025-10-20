# job/apps.py
from django.apps import AppConfig
from django.core.management import call_command
import threading

class JobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job'

    def ready(self):
        if getattr(self, 'scheduler_started', False):
            return
        self.scheduler_started = True

        def run_fetch_weather():
            while True:
                print("⏳ Auto fetching weather data...")
                call_command('fetch_weather')
                threading.Event().wait(60)  # waits 60 seconds between runs

        threading.Thread(target=run_fetch_weather, daemon=True).start()
        print("🚀 Weather scheduler started in background!")
