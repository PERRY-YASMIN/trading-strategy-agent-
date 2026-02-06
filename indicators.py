"""
Technical Indicators Module

Calculates technical indicators for market analysis, focusing on
Moving Averages and crossover signals for trading decisions.

MOVING AVERAGE CROSSOVER STRATEGY:
- When a short-term MA crosses above a long-term MA = BULLISH signal (BUY)
- When a short-term MA crosses below a long-term MA = BEARISH signal (SELL)
- This strategy identifies momentum shifts in price trends
"""

import pandas as pd


def calculate_moving_average(price_data, window):
    """
    Calculate Simple Moving Average (SMA).
    
    A moving average smooths out price data by calculating the average
    of the last N prices (where N = window). This helps identify trends
    by filtering out short-term price noise.
    
    Example: For window=5 and prices [100, 102, 101, 103, 105]
             MA = (100 + 102 + 101 + 103 + 105) / 5 = 102.2
    
    Args:
        price_data: pandas Series or list of closing prices
        window: Number of periods to average (e.g., 5 for 5-period MA)
    
    Returns:
        pandas Series with moving average values, or None if insufficient data
    """
    # Check if we have enough data
    if price_data is None or len(price_data) < window:
        print(f"Warning: Need at least {window} data points for MA calculation")
        return None
    
    # Convert to pandas Series if it's a list
    if isinstance(price_data, list):
        price_series = pd.Series(price_data)
    else:
        price_series = price_data
    
    # Calculate rolling moving average
    # .rolling(window) creates a sliding window of size 'window'
    # .mean() calculates the average for each window
    moving_avg = price_series.rolling(window=window).mean()
    
    return moving_avg


def detect_ma_crossover(price_data, short_window, long_window):
    """
    Detect Moving Average crossover signals for trading.
    
    TRADING LOGIC:
    - Calculate short-term MA (fast, responsive to recent prices)
    - Calculate long-term MA (slow, shows overall trend)
    - Compare the two:
        * If short MA crosses ABOVE long MA → BUY signal (bullish)
        * If short MA crosses BELOW long MA → SELL signal (bearish)
        * Otherwise → No signal (hold position)
    
    Args:
        price_data: pandas Series or list of closing prices
        short_window: Period for short-term MA (e.g., 5)
        long_window: Period for long-term MA (e.g., 20)
    
    Returns:
        "BUY", "SELL", or None
    """
    # Validate inputs
    if price_data is None or len(price_data) < long_window:
        print(f"Warning: Need at least {long_window} data points for crossover detection")
        return None
    
    # Calculate both moving averages
    short_ma = calculate_moving_average(price_data, short_window)
    long_ma = calculate_moving_average(price_data, long_window)
    
    # Check if calculations succeeded
    if short_ma is None or long_ma is None:
        return None
    
    # We need at least 2 time points to detect a crossover
    if len(short_ma) < 2 or len(long_ma) < 2:
        return None
    
    # Get current values (most recent time point)
    short_current = short_ma.iloc[-1]
    long_current = long_ma.iloc[-1]
    
    # Get previous values (one step back)
    short_previous = short_ma.iloc[-2]
    long_previous = long_ma.iloc[-2]
    
    # Check for NaN values (not enough data for calculation)
    if pd.isna(short_current) or pd.isna(long_current):
        return None
    if pd.isna(short_previous) or pd.isna(long_previous):
        return None
    
    # DETECT BULLISH CROSSOVER (BUY signal)
    # Short MA was below long MA, now it's above
    if short_previous <= long_previous and short_current > long_current:
        print("🔔 BULLISH CROSSOVER: Short MA crossed above Long MA")
        return "BUY"
    
    # DETECT BEARISH CROSSOVER (SELL signal)
    # Short MA was above long MA, now it's below
    elif short_previous >= long_previous and short_current < long_current:
        print("🔔 BEARISH CROSSOVER: Short MA crossed below Long MA")
        return "SELL"
    
    # No crossover detected
    else:
        return None


def get_latest_ma_values(price_data, short_window, long_window):
    """
    Get the current values of both moving averages for display/logging.
    
    Args:
        price_data: pandas Series or list of closing prices
        short_window: Period for short-term MA
        long_window: Period for long-term MA
    
    Returns:
        Dictionary with 'short_ma' and 'long_ma' values, or None
    """
    if price_data is None or len(price_data) < long_window:
        return None
    
    short_ma = calculate_moving_average(price_data, short_window)
    long_ma = calculate_moving_average(price_data, long_window)
    
    if short_ma is None or long_ma is None:
        return None
    
    # Get the most recent non-NaN values
    short_value = short_ma.iloc[-1]
    long_value = long_ma.iloc[-1]
    
    if pd.isna(short_value) or pd.isna(long_value):
        return None
    
    # Get current price
    if isinstance(price_data, pd.Series):
        current_price = round(price_data.iloc[-1], 2)
    else:
        current_price = round(price_data[-1], 2)
    
    return {
        'short_ma': round(short_value, 2),
        'long_ma': round(long_value, 2),
        'current_price': current_price
    }
