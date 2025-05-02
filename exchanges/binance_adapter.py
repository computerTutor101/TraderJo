# exchanges/binance_adapter.py

import os
from dotenv import load_dotenv
from binance.client import Client
from utils.exchange_adapter import ExchangeAdapter

class BinanceAdapter(ExchangeAdapter):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        self.client = Client(api_key, api_secret, testnet=True)

    def get_price(self, symbol):
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])

    def get_historical_closes(self, symbol, interval="1m", lookback="100 minutes ago UTC"):
        klines = self.client.get_historical_klines(symbol, interval, lookback)
        return [float(kline[4]) for kline in klines]

    def place_order(self, symbol, side, quantity):
        # Simulate order
        return f"{side.upper()} order placed for {quantity} {symbol}"