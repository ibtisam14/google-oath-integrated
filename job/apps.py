from django.apps import AppConfig
import threading
import time
from django.core.management import call_command

class JobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job'

    def ready(self):
        if hasattr(self, 'scheduler_started'):
            return
        self.scheduler_started = True

        def run_cron_jobs():
            time.sleep(5)
            while True:
                print("⏳ Running fetch_weather command...")
                call_command('fetch_weather') 
                print("✅ Done! Waiting 5 second before next run...")
                time.sleep(5)

        thread = threading.Thread(target=run_cron_jobs, daemon=True)
        thread.start()
        print("🚀 Weather scheduler started in background!")
