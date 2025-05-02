import numpy as np

# Compute RSI (Relative Strength Index) for a given series of closing prices
def compute_rsi(closes, period=14):
    """
    Calculate the RSI for a list of closing prices.

    :param closes: List or array of closing prices.
    :param period: The lookback period for calculating RSI (default is 14).
    :return: An array with RSI values.
    """
    closes = np.array(closes)
    deltas = np.diff(closes)  # Calculate the difference between consecutive closes
    seed = deltas[:period]    # Initial period of data for the first RSI value
    up = seed[seed >= 0].sum() / period  # Average gain
    down = -seed[seed < 0].sum() / period  # Average loss
    rs = up / down if down != 0 else 0  # Relative strength (RS)
    rsi = np.zeros_like(closes)
    rsi[:period] = 100. - 100. / (1. + rs)  # Initialize RSI for first 'period' values

    # Compute RSI for the rest of the data
    for i in range(period, len(closes)):
        delta = deltas[i - 1]
        upval = max(delta, 0)
        downval = max(-delta, 0)
        
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)  # Calculate the RSI for each point

    return rsi