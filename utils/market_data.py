# utils/market_data.py

from binance.client import Client
from utils.logger import log_event

def get_live_price(client, symbol="BTCUSDT"):
    """
    Fetch the current price for a given symbol from Binance.
    """
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        log_event(f"Error fetching live price from Binance: {e}")
        return None

def get_historical_klines(client, symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, lookback="100 minutes ago UTC"):
    """
    Fetch historical Kline (candlestick) data from Binance.
    """
    try:
        klines = client.get_historical_klines(symbol, interval, lookback)
        closes = [float(kline[4]) for kline in klines]  # Close prices
        return closes
    except Exception as e:
        log_event(f"Error fetching historical klines from Binance: {e}")
        return None