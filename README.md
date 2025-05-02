
# PhoenixBot 🔥

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/build-live--simulator-yellowgreen)]()

PhoenixBot is a modular, live-data, paper trading crypto bot that trades based on RSI (Relative Strength Index) strategies using the Binance API.  
The bot fetches real-time BTC/USDT market data, simulates trades based on RSI thresholds, and visualizes wallet growth live.

---

## 📂 Project Structure
PhoenixBot/
│
├── testbot.py                  # Main bot runner (super clean coordinator)
│
├── utils/                       # Utility functions
│   ├── wallet.py                # Buying, selling, wallet checking logic
│   ├── logger.py                # Logging system
│   ├── live_plot.py             # Real-time wallet graph plotting
│   ├── market_data.py           # Fetch live prices and historical data
│
├── strategies/                  # Trading strategy logic
│   ├── rsi_strategy.py          # RSI-based buy/sell decision maker
│
├── config/                      # Configuration files
│   ├── settings.py              # Trade fees, thresholds, cooldowns, etc.
│
├── .env                         # Environment variables (API keys)
├── requirements.txt             # Required Python packages
└── README.md                    # Project summary (this file)

---

## 🚀 Setup Instructions

1. **Clone the repository** (if using GitHub):
   ```bash
   git clone https://github.com/your_username/PhoenixBot.git
   cd PhoenixBot
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Mac/Linux
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Binance API keys**:
   - Log in to your Binance account and generate a new API key and secret from the API Management section.
   - Create a `.env` file in the root folder (same directory as `testbot.py`).
   - Add your API keys to the `.env` file in the following format:
     ```
     BINANCE_API_KEY=your_api_key_here
     BINANCE_API_SECRET=your_api_secret_here
     ```
   - **Never share your `.env` file or API keys publicly.** The `.env` file should be kept private and is typically included in `.gitignore` to prevent accidental commits.

5. **Run the bot**:
   ```bash
   python testbot.py
   ```

## ⚙ Configuration

Adjust your trading settings in `config/settings.py`:

| Setting               | Description                                  |
|-----------------------|----------------------------------------------|
| TRADE_FEE             | Exchange fee per trade                       |
| COOLDOWN              | Minimum seconds between trades               |
| OVERSOLD_THRESHOLD    | RSI threshold to trigger a buy               |
| OVERBOUGHT_THRESHOLD  | RSI threshold to trigger a sell              |
| INITIAL_USD_BALANCE   | Starting USD balance                         |
| INITIAL_BTC_BALANCE   | Starting BTC balance                         |
| TRADE_SYMBOL          | Trading pair symbol (default: BTCUSDT)       |

## 📈 Features
* Live price fetching from Binance
* RSI calculation for trade decisions
* Cooldown system to avoid overtrading
* Real-time wallet performance graph
* Modular, extendable architecture (easy to add new strategies or utilities)
* Comprehensive logging system and time tracking for trades and events
* Paper trading (no real money at risk)

## Roadmap
	•	Add multi-strategy support (MACD, EMA crossover, etc.)
	•	Implement dynamic position sizing
	•	Build backtesting module
	•	Add notifications (email/Telegram alerts)

## Contributions

Pull requests and improvements are welcome! Please fork the repository and submit a pull request.

## Disclaimer

This project is for educational and paper trading purposes only. Trading cryptocurrencies carries risk. Use responsibly.

- **Never share your API keys or `.env` files publicly.**
- **Do not use real funds for paper trading.** Always use test or simulated accounts when experimenting.

-GeorgeD.Aguilar



