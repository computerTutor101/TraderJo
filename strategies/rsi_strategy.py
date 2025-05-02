# strategies/rsi_strategy.py

from utils.wallet import buy, sell
from utils.logger import log_event
from config import settings
import time


# This function will decide whether to buy, sell, or hold based on RSI
def evaluate_rsi_strategy(rsi, wallet, price, last_trade_time, trade_fee, start_time, warmup_duration):
    """
    Evaluates whether to buy, sell, or do nothing based on RSI values.

    Parameters:
    - rsi: list of RSI values
    - wallet: the trading wallet dictionary
    - price: current market price
    - last_trade_time: last timestamp a trade was made
    - trade_fee: the fee per trade
    - start_time: the timestamp when the bot started
    - warmup_duration: duration in seconds to wait before trading

    Returns:
    - Updated last_trade_time
    """
    now = time.time()
    current_rsi = rsi[-1]

    if time.time() - start_time < warmup_duration:
        if settings.PRINT_RSI_OUTPUT:
            print(f"⏳ Warming up... Current RSI: {rsi[-1]:.2f}")
        return last_trade_time

    # Track the average BTC buy price for smarter sell decisions
    if "avg_buy_price" not in wallet:
        wallet["avg_buy_price"] = 0.0
    if "total_btc_bought" not in wallet:
        wallet["total_btc_bought"] = 0.0

    # Enforce cooldown
    if now - last_trade_time < settings.COOLDOWN:
        return last_trade_time

    usd_balance = wallet.get("USD", 0)
    btc_balance = wallet.get("BTC", 0)

    # BUY signal logic
    if current_rsi < settings.OVERSOLD_THRESHOLD:
        usd_to_spend = usd_balance * settings.TRADE_PERCENTAGE
        if usd_to_spend < 1:
            log_event("❌ Not enough USD to perform trade.")
            return last_trade_time
        btc_bought = (usd_to_spend * (1 - trade_fee)) / price
        wallet["USD"] -= usd_to_spend
        wallet["BTC"] += btc_bought
        wallet["total_btc_bought"] += btc_bought
        total_cost = usd_to_spend
        wallet["avg_buy_price"] = ((wallet["avg_buy_price"] * (wallet["total_btc_bought"] - btc_bought)) + (price * btc_bought)) / wallet["total_btc_bought"]
        log_event(f"📢 BUY Signal - Bought BTC at ${price:.2f}")
        log_event(f"💼 Wallet: {wallet['USD']:.2f} USD, {wallet['BTC']:.6f} BTC")
        return now

    # SELL signal logic
    elif current_rsi > settings.OVERBOUGHT_THRESHOLD:
        btc_to_sell = btc_balance * settings.TRADE_PERCENTAGE
        if btc_to_sell * price < 1:
            log_event("❌ Not enough BTC to perform trade.")
            return last_trade_time
        avg_price = wallet.get("avg_buy_price", 0)
        profit_percentage = (price - avg_price) / avg_price
        if price <= avg_price or profit_percentage < settings.MIN_PROFIT_PERCENTAGE:
            log_event("❌ SELL skipped — below profit threshold.")
            return last_trade_time
        usd_gained = btc_to_sell * price * (1 - trade_fee)
        wallet["BTC"] -= btc_to_sell
        wallet["USD"] += usd_gained
        wallet["total_btc_bought"] -= btc_to_sell
        if wallet["total_btc_bought"] > 0:
            wallet["avg_buy_price"] = ((wallet["avg_buy_price"] * (wallet["total_btc_bought"] + btc_to_sell)) - (price * btc_to_sell)) / wallet["total_btc_bought"]
        else:
            wallet["avg_buy_price"] = 0
        log_event(f"📢 SELL Signal - Sold BTC at ${price:.2f}")
        log_event(f"💼 Wallet: {wallet['USD']:.2f} USD, {wallet['BTC']:.6f} BTC")
        return now

    # No trade
    log_event(f"No trade - RSI neutral. Current RSI: {current_rsi:.2f}")
    log_event(f"💼 Wallet: {wallet['USD']:.2f} USD, {wallet['BTC']:.6f} BTC (Total ${(wallet['USD'] + wallet['BTC'] * price):.2f})")
    return last_trade_time