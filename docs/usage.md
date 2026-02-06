# Usage and Workflow

This document describes how the bot operates during runtime.

## Runtime Flow

Each cycle performs the following steps:

1. Fetch latest 5-minute stock data for the last 30 days.
2. Compress the time-series using delta compression.
3. Calculate short and long moving averages.
4. Detect crossover signals.
5. Send a Discord alert if a new signal appears.
6. Sleep for 5 minutes, then repeat.

## Signals

- BUY: short moving average crosses above the long moving average.
- SELL: short moving average crosses below the long moving average.
- None: no crossover detected.

## Logging

The bot prints readable logs for each step so you can track progress and debug issues.
