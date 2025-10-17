from django.core.management import call_command
import datetime

def fetch_weather_job():
    """
    This function will be run automatically by django-crontab.
    It calls your existing 'fetch_weather' command.
    """
    print(f"[{datetime.datetime.now()}] ⏳ Running cron: Fetching weather data...")
    call_command('fetch_weather')
