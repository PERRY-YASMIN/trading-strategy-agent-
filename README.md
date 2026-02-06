# Trading Monitor & Alert Bot

An automated Python bot that monitors stock prices, detects trading signals using moving average crossovers, and sends real-time alerts to Discord.
## 📋 Overview

This bot continuously tracks stock market data and uses technical analysis to identify potential buy and sell opportunities. When a trading signal is detected, it immediately sends a formatted notification to your Discord channel, helping you stay informed without constantly watching the market.
## ✨ Features

- **Automated Monitoring**: Checks stock prices every 5 minutes
- **Moving Average Crossover Strategy**: Detects buy/sell signals using short and long-term moving averages
- **Backtesting Engine**: Test the strategy on historical data with performance metrics (win rate, returns, drawdown)
- **Data Compression**: Efficient storage using delta compression for time-series data
- **Discord Notifications**: Sends formatted alerts with emojis and price information
- **Smart Alerts**: Only notifies when NEW signals appear (prevents duplicate alerts)
- **Beginner-Friendly**: Clean, well-commented code that's easy to understand and modify

## 📊 How the Trading Signal Works
The bot uses a **Moving Average Crossover Strategy**, one of the most popular technical analysis methods:

### What are Moving Averages?
A moving average smooths out price fluctuations by calculating the average price over a specific time period. This helps identify trends.

- **Short-term MA (5 periods)**: Responds quickly to recent price changes
- **Long-term MA (20 periods)**: Shows the overall trend direction

### Signal Detection
**🟢 BUY Signal - Bullish Crossover**
Occurs when the short-term MA crosses ABOVE the long-term MA
Indicates upward momentum - price is gaining strength
Suggests it might be a good time to buy

**🔴 SELL Signal - Bearish Crossover**
Occurs when the short-term MA crosses BELOW the long-term MA
Indicates downward momentum - price is losing strength
Suggests it might be a good time to sell
### Example

```
Day 1: Short MA = $100, Long MA = $102 (Short is below)
Day 2: Short MA = $103, Long MA = $102 (Short crosses above) → BUY SIGNAL! 🟢
```
## 💾 Data Compression with ScaleDown

The bot implements **delta compression** to efficiently handle large amounts of price data:
### Why Compression Matters

Stock prices at 5-minute intervals generate thousands of data points. Storing full floating-point numbers (e.g., 150.23, 150.25, 150.24) for each data point consumes significant memory.
### How Delta Compression Works

Instead of storing every full price, we store:
1. **Base Price**: The first price point (e.g., 150.23)
2. **Deltas**: Only the differences between consecutive prices (e.g., +0.02, -0.01)

### Example
**Original Data:**
```
```
[150.23, 150.25, 150.24, 150.27, 150.25]
```

**Compressed Data:**
```
Base: 150.23
Deltas: [+0.02, -0.01, +0.03, -0.02]
### Benefits

- **Smaller Numbers**: Deltas are typically small (±0.01 to ±1.00) vs. full prices (100.00+)
- **Memory Efficient**: Reduces storage space and speeds up data processing
- **Perfect for Time-Series**: Stock prices change gradually, making this highly effective

This compression technique is inspired by ScaleDown principles - optimizing data storage while preserving accuracy.
## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Discord account with webhook access

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
This will install:
- `yfinance` - Fetches stock data from Yahoo Finance
- `pandas` - Data processing and analysis
- `numpy` - Mathematical operations
- `requests` - Sends HTTP requests to Discord
### Step 2: Configure Discord Webhook

1. Open Discord and navigate to your server
2. Go to **Server Settings** → **Integrations** → **Webhooks**
3. Click **New Webhook** or **Create Webhook**
4. Customize the webhook name and select a channel
5. Click **Copy Webhook URL**
6. Open `config.py` and replace the placeholder with your webhook URL:

```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_ACTUAL_WEBHOOK_URL"
```

### Step 3: Customize Settings (Optional)
Edit `config.py` to change:

```python
STOCK_SYMBOL = "AAPL"              # Change to any stock ticker
FETCH_INTERVAL_MINUTES = 5         # How often to check
LOOKBACK_PERIOD_DAYS = 30          # Historical data period
SHORT_MA_WINDOW = 5                # Short-term moving average
LONG_MA_WINDOW = 20                # Long-term moving average
```
### Step 4: Run the Bot

```bash
python main.py
```
The bot will start monitoring and display status updates in the console. Press `Ctrl+C` to stop.

## � Backtesting - Test the Strategy on Historical Data

**🎯 NEW FEATURE**: Before running the bot live, you can test the Moving Average Crossover strategy on historical data to see how it would have performed.

### Why Backtest?

- **Evaluate Strategy Performance**: See win rate, total return, and maximum drawdown
- **Build Confidence**: Understand how the strategy behaves in different market conditions
- **Risk-Free Testing**: Test on historical data before risking real money
- **Optimize Parameters**: Experiment with different MA windows to find what works best

### Running a Backtest

**Default (6 months):**
```bash
python main.py --backtest
```

**Custom period (e.g., 12 months):**
```bash
python main.py --backtest 12
```

### Sample Backtest Output

```
============================================================
Starting Backtest for AAPL
Period: 6 months | Initial Capital: $10,000.00
============================================================

Fetching 6 months of historical data...
Loaded 126 trading days of data

📈 BUY  | 2025-09-15 | Price: $155.23 | Shares: 64.42
✅ SELL | 2025-10-02 | Price: $162.45 | P/L: $465.13 (+4.65%)
📈 BUY  | 2025-11-08 | Price: $158.90 | Shares: 65.86
❌ SELL | 2025-12-01 | Price: $156.20 | P/L: -$177.82 (-1.70%)

============================================================
BACKTEST RESULTS
============================================================

📊 Trading Performance:
   Total Trades:        8
   Winning Trades:      5 ✅
   Losing Trades:       3 ❌
   Win Rate:            62.50%

💰 Financial Performance:
   Initial Capital:     $10,000.00
   Final Capital:       $11,245.67
   Total Return:        $1,245.67
   Return %:            +12.46%

📈 Trade Statistics:
   Avg Profit/Trade:    $155.71
   Best Trade:          $623.45
   Worst Trade:         -$289.12
   Max Drawdown:        5.23%

Verdict: 🎉 Excellent Performance!
============================================================
```

### Understanding the Metrics

- **Win Rate**: Percentage of trades that were profitable
- **Total Return**: Overall profit or loss from all trades
- **Avg Profit/Trade**: Average gain (or loss) per trade
- **Max Drawdown**: Largest peak-to-trough decline (risk indicator)

### Testing the Alert System

Before running the bot, test that Discord alerts work correctly:

```bash
python main.py --test
```

This sends test BUY and SELL alerts to verify your webhook configuration.

## �📁 Project Structure
```
trading_bot/
├── main.py              # Main loop and orchestration
├── data_fetcher.py      # Fetches stock data from Yahoo Finance
├── compressor.py        # Delta compression implementation
├── indicators.py        # Moving average calculations and signal detection
├── alert.py             # Discord webhook notifications
├── backtest.py          # Backtesting engine for strategy evaluation
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── docs/                # Detailed documentation
```

## 🔧 Configuration Options
| Setting | Description | Default |
|---------|-------------|---------|
| `STOCK_SYMBOL` | Stock ticker to monitor | "AAPL" |
| `FETCH_INTERVAL_MINUTES` | Check frequency | 5 minutes |
| `LOOKBACK_PERIOD_DAYS` | Historical data range | 30 days |
| `SHORT_MA_WINDOW` | Short-term MA period | 5 |
| `LONG_MA_WINDOW` | Long-term MA period | 20 |
| `DISCORD_WEBHOOK_URL` | Discord webhook URL | (must configure) |

## 📝 Example Output
```
=============================================================
[2026-02-06 14:30:00] Iteration #1
=============================================================

📊 Fetching data for AAPL...
✓ Fetched 5000 price data points
   Latest Price: $175.23

💾 Compressing data...
Compressed 5000 prices into 1 base + 4999 deltas

📈 Calculating indicators...
   Current Price: $175.23
   Short MA: $175.50
   Long MA: $174.20

🔔 Signal Status: BUY
   🚨 NEW BUY SIGNAL DETECTED!
   📤 Sending Discord alert...
   ✓ Discord alert sent successfully for AAPL BUY signal

⏳ Waiting 5 minutes until next check...
## ⚠️ Disclaimer

**THIS BOT IS FOR EDUCATIONAL PURPOSES ONLY**
- This software is provided as-is for learning and experimentation
- **NOT financial advice** - do not use this as the sole basis for trading decisions
- Stock trading involves substantial risk of loss
- Past performance does not guarantee future results
- Always do your own research and consult with a qualified financial advisor
- The developers assume no responsibility for any financial losses incurred

**Use at your own risk.**

## 📚 Learning Resources
If you're new to trading or technical analysis:

- [Moving Average Crossover Strategy Explained](https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp)
- [Yahoo Finance API Documentation](https://python-yahoofinance.readthedocs.io/)
- [Discord Webhooks Guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
## 🤝 Contributing

This is a learning project. Feel free to:
- Modify the code for your needs
- Add new indicators or features
- Experiment with different trading strategies
- Share improvements with others

## 📄 License
MIT License - See LICENSE file for details

### What are Moving Averages?

A moving average smooths out price fluctuations by calculating the average price over a specific time period. This helps identify trends.

- **Short-term MA (5 periods)**: Responds quickly to recent price changes
- **Long-term MA (20 periods)**: Shows the overall trend direction

### Signal Detection

**🟢 BUY Signal - Bullish Crossover**
- Occurs when the short-term MA crosses ABOVE the long-term MA
- Indicates upward momentum - price is gaining strength
- Suggests it might be a good time to buy

**🔴 SELL Signal - Bearish Crossover**
- Occurs when the short-term MA crosses BELOW the long-term MA
- Indicates downward momentum - price is losing strength
- Suggests it might be a good time to sell

### Example

```
Day 1: Short MA = $100, Long MA = $102 (Short is below)
Day 2: Short MA = $103, Long MA = $102 (Short crosses above) → BUY SIGNAL! 🟢
```

## 💾 Data Compression with ScaleDown

The bot implements **delta compression** to efficiently handle large amounts of price data:

### Why Compression Matters

Stock prices at 5-minute intervals generate thousands of data points. Storing full floating-point numbers (e.g., 150.23, 150.25, 150.24) for each data point consumes significant memory.

### How Delta Compression Works

Instead of storing every full price, we store:
1. **Base Price**: The first price point (e.g., 150.23)
2. **Deltas**: Only the differences between consecutive prices (e.g., +0.02, -0.01)

### Example

**Original Data:**
```
[150.23, 150.25, 150.24, 150.27, 150.25]
```

**Compressed Data:**
```
Base: 150.23
Deltas: [+0.02, -0.01, +0.03, -0.02]
```

### Benefits

- **Smaller Numbers**: Deltas are typically small (±0.01 to ±1.00) vs. full prices (100.00+)
- **Memory Efficient**: Reduces storage space and speeds up data processing
- **Perfect for Time-Series**: Stock prices change gradually, making this highly effective

This compression technique is inspired by ScaleDown principles - optimizing data storage while preserving accuracy.

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Discord account with webhook access

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `yfinance` - Fetches stock data from Yahoo Finance
- `pandas` - Data processing and analysis
- `numpy` - Mathematical operations
- `requests` - Sends HTTP requests to Discord

### Step 2: Configure Discord Webhook

1. Open Discord and navigate to your server
2. Go to **Server Settings** → **Integrations** → **Webhooks**
3. Click **New Webhook** or **Create Webhook**
4. Customize the webhook name and select a channel
5. Click **Copy Webhook URL**
6. Open `config.py` and replace the placeholder with your webhook URL:

```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_ACTUAL_WEBHOOK_URL"
```

### Step 3: Customize Settings (Optional)

Edit `config.py` to change:

```python
STOCK_SYMBOL = "AAPL"              # Change to any stock ticker
FETCH_INTERVAL_MINUTES = 5         # How often to check
LOOKBACK_PERIOD_DAYS = 30          # Historical data period
SHORT_MA_WINDOW = 5                # Short-term moving average
LONG_MA_WINDOW = 20                # Long-term moving average
```

### Step 4: Run the Bot

```bash
python main.py
```

The bot will start monitoring and display status updates in the console. Press `Ctrl+C` to stop.

## 📁 Project Structure

```
trading_bot/
├── main.py              # Main loop and orchestration
├── data_fetcher.py      # Fetches stock data from Yahoo Finance
├── compressor.py        # Delta compression implementation
├── indicators.py        # Moving average calculations and signal detection
├── alert.py             # Discord webhook notifications
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `STOCK_SYMBOL` | Stock ticker to monitor | "AAPL" |
| `FETCH_INTERVAL_MINUTES` | Check frequency | 5 minutes |
| `LOOKBACK_PERIOD_DAYS` | Historical data range | 30 days |
| `SHORT_MA_WINDOW` | Short-term MA period | 5 |
| `LONG_MA_WINDOW` | Long-term MA period | 20 |
| `DISCORD_WEBHOOK_URL` | Discord webhook URL | (must configure) |

## 📝 Example Output

```
=============================================================
[2026-02-06 14:30:00] Iteration #1
=============================================================

📊 Fetching data for AAPL...
✓ Fetched 5000 price data points
   Latest Price: $175.23

💾 Compressing data...
Compressed 5000 prices into 1 base + 4999 deltas

📈 Calculating indicators...
   Current Price: $175.23
   Short MA: $175.50
   Long MA: $174.20

🔔 Signal Status: BUY
   🚨 NEW BUY SIGNAL DETECTED!
   📤 Sending Discord alert...
   ✓ Discord alert sent successfully for AAPL BUY signal

⏳ Waiting 5 minutes until next check...
```

## ⚠️ Disclaimer

**THIS BOT IS FOR EDUCATIONAL PURPOSES ONLY**

- This software is provided as-is for learning and experimentation
- **NOT financial advice** - do not use this as the sole basis for trading decisions
- Stock trading involves substantial risk of loss
- Past performance does not guarantee future results
- Always do your own research and consult with a qualified financial advisor
- The developers assume no responsibility for any financial losses incurred

**Use at your own risk.**

## 📚 Learning Resources

If you're new to trading or technical analysis:

- [Moving Average Crossover Strategy Explained](https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp)
- [Yahoo Finance API Documentation](https://python-yahoofinance.readthedocs.io/)
- [Discord Webhooks Guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

## 🤝 Contributing

This is a learning project. Feel free to:
- Modify the code for your needs
- Add new indicators or features
- Experiment with different trading strategies
- Share improvements with others

## 📄 License

MIT License - See LICENSE file for details
>>>>>>> 72e75dd (Testing Successful v1.0)
