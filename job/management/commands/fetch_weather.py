from django.core.management.base import BaseCommand
from django.conf import settings
from job.models import WeatherData
import requests

class Command(BaseCommand):
    help = "Fetch weather data and store it in the database"

    def handle(self, *args, **kwargs):
        city = "Karachi"
        api_key = settings.WEATHER_API_KEY
        if not api_key:
            self.stdout.write(self.style.ERROR("⚠️ WEATHER_API_KEY not found"))
            return

        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"❌ Failed to fetch weather: {data}"))
            return

        weather = WeatherData.objects.create(
            city=data["location"]["name"],
            temperature_c=data["current"]["temp_c"],
            condition=data["current"]["condition"]["text"],
            humidity=data["current"]["humidity"],
            wind_kph=data["current"]["wind_kph"],
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Saved weather for {weather.city}"))
