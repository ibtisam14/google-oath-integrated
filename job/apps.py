# job/apps.py
from django.apps import AppConfig
import threading
import time
import requests
import os


class JobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job'

    def ready(self):
        """
        Start a background thread after Django is ready,
        to schedule weather updates every 60 seconds.
        """

        # ✅ Prevent duplicate thread from Django's autoreloader
        if os.environ.get('RUN_MAIN') != 'true':
            return

        def start_scheduler():
            # Wait a few seconds to ensure Django DB is ready
            time.sleep(5)

            from django.conf import settings
            from django.utils import timezone
            from job.models import WeatherData

            def fetch_weather():
                try:
                    city = "Karachi"
                    api_key = settings.WEATHER_API_KEY
                    if not api_key:
                        print("⚠️ WEATHER_API_KEY not found")
                        return

                    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
                    response = requests.get(url)
                    data = response.json()

                    if response.status_code != 200:
                        print(f"❌ Failed to fetch weather: {data}")
                    else:
                        weather = WeatherData.objects.create(
                            city=data["location"]["name"],
                            temperature_c=data["current"]["temp_c"],
                            condition=data["current"]["condition"]["text"],
                            humidity=data["current"]["humidity"],
                            wind_kph=data["current"]["wind_kph"],
                        )
                        print(f"✅ [{timezone.now()}] Saved weather for {weather.city}")

                except Exception as e:
                    print(f"⚠️ Weather fetch error: {e}")

                # Schedule the next run after 60 seconds
                threading.Timer(60, fetch_weather).start()

            # Start first fetch
            fetch_weather()

        threading.Thread(target=start_scheduler, daemon=True).start()
