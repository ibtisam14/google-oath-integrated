from django.apps import AppConfig
import threading
import time
import requests


class JobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job'

    def ready(self):
        """
        This runs automatically when Django starts.
        It launches a background thread that fetches weather data every 60 seconds.
        """
        from django.conf import settings
        from django.utils import timezone
        from job.models import WeatherData  # ✅ imported here (after apps are ready)

        def fetch_weather_periodically():
            while True:
                try:
                    city = "Karachi"
                    api_key = settings.WEATHER_API_KEY
                    if not api_key:
                        print("⚠️ WEATHER_API_KEY not found")
                        time.sleep(60)
                        continue

                    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
                    response = requests.get(url)
                    data = response.json()

                    if response.status_code != 200:
                        print(f"❌ Failed to fetch weather: {data}")
                        time.sleep(60)
                        continue

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

                # Sleep for 60 seconds (1 minute)
                time.sleep(60)

        # 🧵 Start the periodic weather fetch in a daemon thread
        threading.Thread(target=fetch_weather_periodically, daemon=True).start()
