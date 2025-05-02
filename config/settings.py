# config/settings.py

# Trading and strategy settings
TRADE_FEE = 0.001  # 0.1% fee per trade
COOLDOWN = 90  # seconds minutes cooldown between trades
OVERSOLD_THRESHOLD = 35 # RSI threshold for buying
OVERBOUGHT_THRESHOLD = 50  # RSI threshold for selling

TRADE_PERCENTAGE = 0.05  # Percentage of available USD to use for each trade

# Wallet initial settings
INITIAL_USD_BALANCE = 1000.0
INITIAL_BTC_BALANCE = 0.0

# Symbol Settings
TRADE_SYMBOL = "BTCUSDT"
EXCHANGE_NAME = "Binance"  # Name of the exchange platform


# Bot Metadata
BOT_NAME = "PhoenixBot"
VERSION = "1.0"

# Bot behavior settings
WARMUP_DURATION = 5 * 60  # Time to wait (in seconds) before starting to trade
PRINT_RSI_OUTPUT = True  # If True, prints RSI at each data point
MIN_PROFIT_THRESHOLD = 0.003  # Minimum profit percentage required to trigger a sell