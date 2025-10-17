from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature_c = models.FloatField()
    condition = models.CharField(max_length=100)
    humidity = models.FloatField()
    wind_kph = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temperature_c}°C"
