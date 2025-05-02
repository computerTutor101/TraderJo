# utils/exchange_adapter.py

class ExchangeAdapter:
    """
    Abstract base class for any exchange or market data source.
    Every adapter must implement the following methods:
    """
    def get_price(self, symbol):
        raise NotImplementedError("get_price() must be implemented")

    def get_historical_closes(self, symbol, interval, lookback):
        raise NotImplementedError("get_historical_closes() must be implemented")

    def place_order(self, symbol, side, quantity):
        raise NotImplementedError("place_order() must be implemented")