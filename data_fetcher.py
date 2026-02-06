"""
Data Fetcher Module

This module fetches stock market data using the yfinance library.
yfinance connects to Yahoo Finance and downloads historical price data
for any stock symbol (like AAPL, GOOGL, etc.).

We fetch data at 5-minute intervals to monitor short-term price movements
and extract only the closing prices for analysis.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_stock_data(symbol, period_days=30):
    """
    Fetch historical stock data at 5-minute intervals.
    
    This function downloads stock price data from Yahoo Finance
    and returns only the closing prices for the specified period.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        period_days: Number of days to look back (default: 30)
    
    Returns:
        pandas Series with closing prices, or None if fetch fails
    """
    try:
        # Create a yfinance Ticker object for the stock
        stock = yf.Ticker(symbol)
        
        # Calculate the date range for fetching data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        # Download 5-minute interval data
        # interval options: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        data = stock.history(
            start=start_date,
            end=end_date,
            interval="5m"
        )
        
        # Check if data was successfully fetched
        if data.empty:
            print(f"Warning: No data received for {symbol}")
            return None
        
        # Extract and return only the closing prices
        closing_prices = data['Close']
        
        print(f"Successfully fetched {len(closing_prices)} data points for {symbol}")
        return closing_prices
        
    except Exception as e:
        # Catch any errors (network issues, invalid symbol, etc.)
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None


def fetch_latest_price(symbol):
    """
    Fetch the most recent closing price for a stock.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
        Float with latest price, or None if fetch fails
    """
    try:
        stock = yf.Ticker(symbol)
        
        # Get just the last 2 days of 5-minute data
        data = stock.history(period="2d", interval="5m")
        
        if data.empty:
            print(f"Warning: No data received for {symbol}")
            return None
        
        # Return the most recent closing price
        latest_price = data['Close'].iloc[-1]
        return latest_price
        
    except Exception as e:
        print(f"Error fetching latest price for {symbol}: {str(e)}")
        return None


def validate_data(data):
    """
    Validate fetched data for completeness.
    
    Checks if the data exists and contains values.
    
    Args:
        data: Market data to validate (pandas Series or DataFrame)
    
    Returns:
        Boolean indicating if data is valid
    """
    # Check if data exists
    if data is None:
        return False
    
    # For pandas objects, use .empty attribute
    if isinstance(data, (pd.Series, pd.DataFrame)):
        return not data.empty
    
    # For other types, check length
    return len(data) > 0
