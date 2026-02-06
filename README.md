# Trading Strategy Agent (Beginner Version)

A simplified financial monitoring agent that uses data compression to analyze market patterns and send alerts.

## Features
- 📊 Real-time stock data fetching from Yahoo Finance
- 🗜️ Market data compression using ScaleDown techniques
- ⚡ Simple moving average crossover strategy
- 🔔 Discord/Slack/Email alerts (no actual trading)
- 📈 Historical data visualization

## Simplified Technical Approach
Instead of full automated trading, this agent:
1. Monitors 3-5 popular stocks (AAPL, TSLA, MSFT)
2. Compresses 30-day price history by 70%
3. Identifies simple buy/sell signals
4. Sends alerts for manual review

## Getting Started
1. Clone repo: `git clone https://github.com/yourname/trading-agent-beginner`
2. Install: `pip install -r requirements.txt`
3. Set up alerts in `config/settings.yaml`
4. Run: `python src/agent_orchestrator.py`

## How Compression Helps
- **Before:** 30 days × 5 stocks × 100 data points = 15,000 data points
- **After compression:** Same info in 4,500 data points (70% reduction)
- **Result:** Faster analysis, lower memory usage, reduced API calls
