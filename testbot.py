import os
import time
import datetime

# Enable RSI output printing
PRINT_RSI_OUTPUT = True
from utils.wallet import check_wallet, buy, sell
from utils.rsi_calculator import compute_rsi  # Import the real RSI calculation
from utils.logger import log_event
from utils.live_plot import setup_plot, update_plot
from strategies.rsi_strategy import evaluate_rsi_strategy
from config.settings import TRADE_FEE, COOLDOWN, OVERSOLD_THRESHOLD, OVERBOUGHT_THRESHOLD, INITIAL_USD_BALANCE, INITIAL_BTC_BALANCE, TRADE_SYMBOL
from utils.rate_limiter import RateLimiter
from exchanges.binance_adapter import BinanceAdapter

rate_limiter = RateLimiter(max_calls_per_minute=100)

# Initialize the Binance adapter (handles its own keys)
adapter = BinanceAdapter()

# Initialize wallet
wallets = {
    "rsi_bot": {
        "USD": INITIAL_USD_BALANCE,
        "BTC": INITIAL_BTC_BALANCE
    }
}
trade_fee = TRADE_FEE
last_trade_time = 0

# Tracking wallet value history
wallet_histories = {
    "rsi_bot": [],
    # "ma_bot": [],  # (we'll add more later!)
}
timestamps = []

# Set the warmup period (equivalent to the RSI period)
RSI_PERIOD = 14  # Standard RSI period

def main():
    global last_trade_time
    log_event("Testing Bot v1.0 Starting...")
    timestamp = datetime.datetime.now().strftime("%I:%M:%S %p %m/%d/%Y")
    log_event(f"🕒 Start Time: {timestamp}")
    start_time = time.time()
    warmup_duration = RSI_PERIOD * 60  # Wait at least RSI_PERIOD minutes before first trade
    setup_plot()

    # Warmup period: wait until we have enough data for the first trade
    collected_data = 0

    while True:
        rate_limiter.wait_if_unsafe()
        price = adapter.get_price(TRADE_SYMBOL)
        rate_limiter.record_call()

        rate_limiter.wait_if_unsafe()
        closes = adapter.get_historical_closes(TRADE_SYMBOL)
        rate_limiter.record_call()

        if not price or not closes:
            time.sleep(60)
            continue

        # Collect data until we have enough for RSI calculation
        if collected_data < RSI_PERIOD:
            collected_data += 1
            elapsed_time = time.time() - start_time
            # Calculate remaining time based on remaining data points
            remaining_points = RSI_PERIOD - collected_data
            estimated_remaining_time = remaining_points * 30  # Reflect actual sleep time of 30 seconds
            mins, secs = divmod(int(estimated_remaining_time), 60)
            bar_length = 20
            filled_length = int(bar_length * collected_data / RSI_PERIOD)
            bar = "#" * filled_length + "-" * (bar_length - filled_length)
            print(f"\r⏳ Warming up... [{bar}] {collected_data}/{RSI_PERIOD} RSI points | ~{mins}m {secs}s remaining", end="", flush=True)
            time.sleep(30)  # Speed up the warmup by reducing sleep time to 30 seconds
            continue
        
        # Once we have enough data, compute the RSI and proceed with trading
        rsi = compute_rsi(closes)  # Use the real RSI calculation

        if PRINT_RSI_OUTPUT:
            print(f"Current RSI: {rsi[-1]}")  # Print the most recent RSI value

        log_event(f"RSI: {rsi[-1]}")

        # Now evaluate the RSI strategy (only after the warmup is done)
        last_trade_time = evaluate_rsi_strategy(
            rsi,
            wallets["rsi_bot"],
            price,
            last_trade_time,
            trade_fee,
            start_time,
            warmup_duration
        )

        # Record wallet history
        total = check_wallet(price, wallets["rsi_bot"])
        wallet_histories["rsi_bot"].append(total)
        timestamps.append(datetime.datetime.now())

        # Log wallet status after trade evaluation
        log_event(f"Wallet Status: {wallets['rsi_bot']}")

        # Update live plot using external live_plot module
        current_balance = total
        current_rsi = rsi[-1] if isinstance(rsi, (list, tuple)) and len(rsi) > 0 else None
        update_plot(timestamps, wallet_histories, current_balance, current_rsi)

        # Delay for 60 seconds before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()