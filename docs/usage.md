# Usage and Workflow

This document describes how to run the bot and how it operates during runtime.

## Available Commands

### 1. Run the Bot (Live Monitoring)

```bash
python main.py
```

Starts the bot in live monitoring mode. It will:
- Fetch stock data every 5 minutes
- Calculate moving averages
- Detect crossover signals
- Send Discord alerts when new signals appear
- Run continuously until you press `Ctrl+C`

### 2. Backtest the Strategy

```bash
# Default: 6 months of historical data
python main.py --backtest

# Custom period: specify number of months
python main.py --backtest 12   # Test 12 months
python main.py --backtest 3    # Test 3 months
```

Runs the strategy on historical data to evaluate performance. Shows:
- Win rate
- Total return
- Maximum drawdown
- Trade history

See [backtesting.md](backtesting.md) for detailed information.

### 3. Test Alert System

```bash
python main.py --test
```

Sends test BUY and SELL alerts to Discord to verify your webhook configuration. Use this before running the bot live.

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
