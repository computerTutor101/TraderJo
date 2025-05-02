import time
import datetime
import matplotlib.pyplot as plt
from strategies.rsi_strategy import RSIStrategy  # Import the RSI strategy
from utils.logger import log_event, get_price, get_klines
from utils.wallet import check_wallet
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API keys from the environment
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

# Initialize wallet
wallet = {"USD": 1000.0, "BTC": 0.0}
trade_fee = 0.001  # 0.1% fee per trade
last_trade_time = 0
cooldown = 5 * 60  # 5 minutes in seconds
oversold_threshold = 30
overbought_threshold = 70

# Tracking wallet value history
wallet_history = []
timestamps = []

# Main Loop
def main():
    global last_trade_time
    log_event("PhoenixBot v1.2 Starting...")
    strategy = RSIStrategy(wallet, cooldown, trade_fee, oversold_threshold, overbought_threshold)
    plt.ion()  # Interactive mode ON

    while True:
        price = get_price()
        closes = get_klines()
        if not price or not closes:
            time.sleep(60)
            continue

        strategy.should_trade(closes, price, log_event)

        # Record wallet history
        total = check_wallet(price, wallet)
        wallet_history.append(total)
        timestamps.append(datetime.datetime.now())

        # Update live plot
        plt.clf()
        plt.plot(timestamps, wallet_history, label="Wallet Value ($)")
        plt.title("PhoenixBot Wallet Growth")
        plt.xlabel("Time")
        plt.ylabel("Wallet Value (USD)")
        plt.legend()
        plt.grid()
        plt.pause(0.01)

        # Delay
        time.sleep(60)

if __name__ == "__main__":
    main()