import requests
from django.http import JsonResponse
from django.conf import settings

def get_weather(request):
    city = request.GET.get('city', 'London') 
    api_key = getattr(settings, 'WEATHER_API_KEY', None)
    if not api_key:
        return JsonResponse({"error": "Weather API key not found"}, status=500)

    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch weather", "details": data}, status=response.status_code)

    return JsonResponse({
        "city": data["location"]["name"],
        "country": data["location"]["country"],
        "temperature_c": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"],
        "wind_kph": data["current"]["wind_kph"],
    })
