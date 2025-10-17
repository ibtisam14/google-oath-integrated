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
            call_command('fetch_weather')  # calls your existing command
            time.sleep(5)  # runs every 5 seconds (for testing)

    # Run the function in a separate thread so it doesn't block Django
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
