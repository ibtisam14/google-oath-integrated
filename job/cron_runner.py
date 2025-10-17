import threading
import time
from django.core.management import call_command

def start_weather_cron():
    """
    This function runs 'fetch_weather' every 5 seconds in the background.
    """
    def run():
        while True:
            print("⏳ Fetching weather data...")
            call_command('fetch_weather') 
            time.sleep(5)  

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
