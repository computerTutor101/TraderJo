import requests
import datetime

log_file = "logs/trades_log.txt"

# Logs events to the file and prints them to the console
def log_event(message):
    with open(log_file, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")
    print(message)

# Logs the settings to the log file and console
def log_settings(settings):
    log_event("Settings:")
    for key, value in settings.items():
        log_event(f"  {key}: {value}")

# Logs the start time and returns it
def log_start_time():
    start_time = datetime.datetime.now()
    log_event(f"Start Time: {start_time}")
    return start_time

# Logs the end time and total runtime given the start time
def log_end_time(start_time):
    end_time = datetime.datetime.now()
    runtime = end_time - start_time
    log_event(f"End Time: {end_time}")
    log_event(f"Total Runtime: {runtime}")

# Fetches the current BTC price from Binance API
def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data['price'])
    except Exception as e:
        log_event(f"Error fetching price: {e}")
        return None

# Fetches the last 100 candlesticks (1-minute interval) from Binance API
def get_klines():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
    try:
        response = requests.get(url)
        data = response.json()
        closes = [float(entry[4]) for entry in data]  # Close prices from the candlesticks
        return closes
    except Exception as e:
        log_event(f"Error fetching klines: {e}")
        return None