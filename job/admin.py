from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature_c', 'condition', 'humidity', 'wind_kph', 'created_at')
    search_fields = ('city', 'condition')
    list_filter = ('city', 'condition')
    ordering = ('-created_at',)
