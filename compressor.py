"""
Data Compressor Module

This module implements delta compression for financial time-series data.

WHY COMPRESSION HELPS:
- Stock prices don't change dramatically between consecutive 5-minute intervals
- Instead of storing full floating-point numbers (e.g., 150.23, 150.25, 150.24),
  we can store one base price and small differences (deltas)
- This reduces memory usage and makes data transfer faster

HOW DELTA COMPRESSION WORKS:
Example: Original prices = [100.50, 100.52, 100.48, 100.51]
Compressed format:
  - Base price: 100.50 (the first price)
  - Deltas: [+0.02, -0.04, +0.03] (differences from previous price)

This is especially efficient for financial data because price changes 
are typically small relative to the absolute price value.
"""

import pandas as pd


def compress_market_data(price_data):
    """
    Compress price data using delta compression.
    
    Stores the first price as a base, then stores only the differences
    (deltas) between consecutive prices.
    
    Args:
        price_data: pandas Series or list of closing prices
    
    Returns:
        Dictionary with 'base_price' and 'deltas' list, or None if data is invalid
    """
    # Handle invalid or empty data
    if price_data is None or len(price_data) == 0:
        print("Warning: Cannot compress empty data")
        return None
    
    # Convert to list if it's a pandas Series
    if isinstance(price_data, pd.Series):
        prices = price_data.tolist()
    else:
        prices = list(price_data)
    
    # Store the first price as our base
    base_price = prices[0]
    
    # Calculate deltas (differences between consecutive prices)
    deltas = []
    for i in range(1, len(prices)):
        # Delta = current price - previous price
        delta = prices[i] - prices[i - 1]
        deltas.append(delta)
    
    # Return compressed format
    compressed = {
        'base_price': base_price,
        'deltas': deltas,
        'original_length': len(prices)
    }
    
    print(f"Compressed {len(prices)} prices into 1 base + {len(deltas)} deltas")
    return compressed


def decompress_market_data(compressed_data):
    """
    Decompress delta-compressed price data back to original prices.
    
    Reconstructs the full price series from the base price and deltas
    by adding each delta sequentially.
    
    Args:
        compressed_data: Dictionary with 'base_price' and 'deltas'
    
    Returns:
        List of original prices, or None if decompression fails
    """
    # Validate compressed data
    if compressed_data is None:
        print("Warning: Cannot decompress None data")
        return None
    
    if 'base_price' not in compressed_data or 'deltas' not in compressed_data:
        print("Warning: Invalid compressed data format")
        return None
    
    # Extract base price and deltas
    base_price = compressed_data['base_price']
    deltas = compressed_data['deltas']
    
    # Start with the base price
    prices = [base_price]
    
    # Reconstruct each price by adding deltas
    current_price = base_price
    for delta in deltas:
        # Add the delta to get the next price
        current_price = current_price + delta
        prices.append(current_price)
    
    print(f"Decompressed {len(prices)} prices from compressed data")
    return prices


def calculate_compression_ratio(original_data, compressed_data):
    """
    Calculate compression efficiency.
    
    Shows the reduction in number of full price values stored.
    
    Args:
        original_data: Original price data (list or Series)
        compressed_data: Compressed data dictionary
    
    Returns:
        Float representing compression ratio (higher is better), or 0.0 if invalid
    """
    if original_data is None or compressed_data is None:
        return 0.0
    
    original_count = len(original_data)
    compressed_count = 1 + len(compressed_data['deltas'])
    
    if compressed_count == 0:
        return 0.0
    
    ratio = original_count / compressed_count
    print(f"Compression ratio: {ratio:.2f}x")
    print(f"(Original: {original_count} values, Compressed: {compressed_count} values)")
    
    return ratio
