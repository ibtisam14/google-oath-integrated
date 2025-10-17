import time
import os

while True:
    print("⏳ Running fetch_weather command...")
    os.system("python manage.py fetch_weather")
    print("✅ Done! Waiting 1 hour before next run...\n")
    time.sleep(3600) 
