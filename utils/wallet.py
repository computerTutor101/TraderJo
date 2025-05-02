# Check wallet balance and log it
def check_wallet(price, wallet):
    total_value = wallet["USD"] + wallet["BTC"] * price
    print(f"💼 Wallet: {wallet['USD']:.2f} USD, {wallet['BTC']:.6f} BTC (Total ${total_value:.2f})")
    return total_value

def validate_price(price):
    if price <= 0:
        print("❌ Invalid price.")
        return False
    return True

def is_wallet_initialized(wallet):
    if wallet["USD"] <= 0 and wallet["BTC"] <= 0:
        print("❌ Wallet is uninitialized! Cannot trade.")
        return False
    return True

def validate_trade_fee(trade_fee):
    if trade_fee < 0 or trade_fee > 1:
        print("❌ Invalid trade fee. Must be between 0 and 1.")
        return False
    return True

def log_wallet(wallet):
    print(f"💼 Wallet: {wallet['USD']:.2f} USD, {wallet['BTC']:.6f} BTC")

# Perform a buy operation
def buy(price, wallet, trade_fee):
    if not validate_price(price):
        return
    if not is_wallet_initialized(wallet):
        return
    if not validate_trade_fee(trade_fee):
        return

    usd_balance = wallet["USD"]
    if usd_balance <= 0:
        print("❌ BUY skipped — insufficient USD available.")
        return

    usd_spent = usd_balance * 0.05
    btc_bought = (usd_spent / price) * (1 - trade_fee)
    wallet["USD"] -= usd_spent
    wallet["BTC"] += btc_bought
    print(f"📢 BUY SIGNAL - Bought {btc_bought:.6f} BTC at ${price:.2f}")
    log_wallet(wallet)

# Perform a sell operation
def sell(price, wallet, trade_fee):
    if not validate_price(price):
        return
    if not is_wallet_initialized(wallet):
        return
    if not validate_trade_fee(trade_fee):
        return

    btc_balance = wallet["BTC"]
    if btc_balance <= 0:
        print("❌ SELL skipped — no BTC available.")
        return

    if btc_balance < 0.01:  # Minimum threshold for selling
        print("❌ Not enough BTC to perform trade.")
        return

    btc_sold = btc_balance * 0.05
    usd_gained = (btc_sold * price) * (1 - trade_fee)
    wallet["BTC"] -= btc_sold
    wallet["USD"] += usd_gained
    print(f"📢 SELL SIGNAL - Sold {btc_sold:.6f} BTC at ${price:.2f}")
    log_wallet(wallet)