import schedule
import time
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

django.setup()

from django.core.management import call_command

def job():
    print("⏳ Fetching weather data...")
    call_command('fetch_weather')

schedule.every(5).seconds.do(job)

try:
    print("🚀 Weather cron started...")
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Cron stopped manually.")
