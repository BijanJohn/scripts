# Script for automating turning on and off the hot saunas at yoga studio
import requests
import schedule
import time
from datetime import datetime

# Sauna configuration (update with your actual credentials)
SAUNAS = {
    "sauna_1": {"url": "https://api.huum.eu/action/home", "auth": ("email", "password")},
    "sauna_2": {"url": "https://api.huum.eu/action/home", "auth": ("email", "password")}
}

def start_sauna(sauna_name):
    sauna = SAUNAS[sauna_name]
    url = f"{sauna['url']}/start"
    payload = {"targetTemperature": 85}
    response = requests.post(url, auth=sauna['auth'], json=payload)
    print(f"[{datetime.now()}] Started {sauna_name}: {response.status_code} - {response.text}")

def stop_sauna(sauna_name):
    sauna = SAUNAS[sauna_name]
    url = f"{sauna['url']}/stop"
    response = requests.post(url, auth=sauna['auth'])
    print(f"[{datetime.now()}] Stopped {sauna_name}: {response.status_code} - {response.text}")

def get_status(sauna_name):
    sauna = SAUNAS[sauna_name]
    url = f"{sauna['url']}/status"
    response = requests.get(url, auth=sauna['auth'])
    print(f"[{datetime.now()}] Status of {sauna_name}: {response.status_code} - {response.text}")

def schedule_tasks():
    # Schedule the saunas to start in the morning and stop at 9 PM
    schedule.every().day.at("06:30").do(lambda: start_sauna("sauna_1"))
    schedule.every().day.at("06:30").do(lambda: start_sauna("sauna_2"))
    schedule.every().day.at("21:00").do(lambda: stop_sauna("sauna_1"))
    schedule.every().day.at("21:00").do(lambda: stop_sauna("sauna_2"))
    
    print("Scheduled sauna automation running...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check schedule every minute

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Control HUUM sauna via API.")
    parser.add_argument("--start", choices=SAUNAS.keys(), help="Start a specific sauna")
    parser.add_argument("--stop", choices=SAUNAS.keys(), help="Stop a specific sauna")
    parser.add_argument("--status", choices=SAUNAS.keys(), help="Get status of a specific sauna")
    args = parser.parse_args()
    
    if args.start:
        start_sauna(args.start)
    elif args.stop:
        stop_sauna(args.stop)
    elif args.status:
        get_status(args.status)
    else:
        schedule_tasks()
