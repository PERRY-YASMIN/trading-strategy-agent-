# Architecture and Modules

This document explains the structure and responsibilities of each module.

## main.py

- Orchestrates the workflow.
- Runs the infinite loop on a fixed schedule.
- Avoids duplicate alerts by tracking the previous signal.

## data_fetcher.py

- Uses yfinance to fetch 5-minute OHLC data.
- Returns only the Close price series.
- Validates data before it is used.

## indicators.py

- Calculates simple moving averages.
- Detects crossover signals (BUY, SELL, None).
- Handles insufficient data safely.

## compressor.py

- Implements delta compression for price data.
- Stores a base price and a list of deltas.
- Can reconstruct the original series from compressed data.

## alert.py

- Sends formatted Discord alerts via webhook.
- Handles webhook errors and timeouts safely.
- Formats messages with symbol, signal, and price.

## config.py

- Stores all configuration settings.
- Validates required values at startup.
