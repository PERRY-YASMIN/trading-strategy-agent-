# Setup and Configuration

This guide explains how to set up and run the Trading Monitor & Alert Bot from scratch.

## Prerequisites

- Python 3.8 or newer
- Internet access (Yahoo Finance data and Discord webhook)

## Install Dependencies

From the project root (trading_bot):

```
pip install -r requirements.txt
```

## Configure Settings

Open config.py and update the following values:

- STOCK_SYMBOL: stock ticker to monitor
- FETCH_INTERVAL_MINUTES: how often to check prices
- LOOKBACK_PERIOD_DAYS: history window for indicators
- SHORT_MA_WINDOW: short moving average period
- LONG_MA_WINDOW: long moving average period
- DISCORD_WEBHOOK_URL: your Discord webhook URL

Example:

```
STOCK_SYMBOL = "AAPL"
FETCH_INTERVAL_MINUTES = 5
LOOKBACK_PERIOD_DAYS = 30
SHORT_MA_WINDOW = 5
LONG_MA_WINDOW = 20
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
```

## Run the Bot

```
python main.py
```

Stop with Ctrl+C.
