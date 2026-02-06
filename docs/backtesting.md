# Backtesting Guide

The backtesting engine allows you to evaluate the Moving Average Crossover strategy on historical data before deploying it in live trading. This is a crucial step in understanding how the strategy performs under different market conditions.

## 📊 What is Backtesting?

Backtesting is the process of testing a trading strategy on historical data to see how it would have performed in the past. While past performance doesn't guarantee future results, backtesting helps you:

- **Understand strategy behavior**: See how often signals are generated
- **Measure profitability**: Calculate total returns and win rate
- **Assess risk**: Measure maximum drawdown and losing streaks
- **Build confidence**: Test before risking real money
- **Optimize parameters**: Experiment with different MA settings

## 🚀 Quick Start

### Basic Backtest (6 months)

```bash
python main.py --backtest
```

This runs a backtest on 6 months of historical daily data using your configured stock symbol (default: AAPL).

### Custom Period

```bash
python main.py --backtest 12    # Test 12 months
python main.py --backtest 3     # Test 3 months
python main.py --backtest 24    # Test 2 years
```

## 📈 Understanding the Results

### Sample Output

```
============================================================
Starting Backtest for AAPL
Period: 6 months | Initial Capital: $10,000.00
============================================================

Fetching 6 months of historical data...
Loaded 126 trading days of data

📈 BUY  | 2025-09-15 | Price: $155.23 | Shares: 64.42
✅ SELL | 2025-10-02 | Price: $162.45 | P/L: $465.13 (+4.65%)
📈 BUY  | 2025-10-12 | Price: $161.90 | Shares: 64.85
✅ SELL | 2025-10-25 | Price: $168.20 | P/L: $408.56 (+3.89%)
📈 BUY  | 2025-11-08 | Price: $158.90 | Shares: 66.32
❌ SELL | 2025-12-01 | Price: $156.20 | P/L: -$179.06 (-1.70%)

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

### Key Metrics Explained

#### Trading Performance

- **Total Trades**: Number of complete buy-sell cycles executed
- **Winning Trades**: Trades that closed with a profit ✅
- **Losing Trades**: Trades that closed with a loss ❌
- **Win Rate**: Percentage of winning trades (winning trades / total trades × 100)

#### Financial Performance

- **Initial Capital**: Starting balance ($10,000 by default)
- **Final Capital**: Ending balance after all trades
- **Total Return**: Net profit or loss in dollars
- **Return %**: Percentage gain or loss on initial capital

#### Trade Statistics

- **Avg Profit/Trade**: Average profit (or loss) per trade
- **Best Trade**: Largest single trade profit
- **Worst Trade**: Largest single trade loss
- **Max Drawdown**: Largest peak-to-trough decline (measures risk)

### Performance Ratings

The backtest engine provides an automatic verdict:

- 🎉 **Excellent Performance**: Return > 10%
- ✅ **Profitable Strategy**: Return > 0%
- ➖ **Break Even**: Return = 0%
- ⚠️ **Needs Improvement**: Return < 0%

## 🔍 How the Backtest Works

### 1. Data Fetching

The engine fetches daily historical data for the specified period using Yahoo Finance API.

```python
# For 6 months backtest
df = fetch_stock_data(symbol="AAPL", period="6mo", interval="1d")
```

### 2. Indicator Calculation

Moving averages are calculated for each day:

- Short MA (default: 5 periods)
- Long MA (default: 20 periods)

### 3. Signal Detection

The engine scans through historical data day by day, detecting crossover signals:

- **BUY Signal**: Short MA crosses above Long MA → Enter long position
- **SELL Signal**: Short MA crosses below Long MA → Exit long position

### 4. Trade Simulation

When a BUY signal occurs:
- Calculate number of shares that can be purchased with available cash
- Record entry price and date
- Set position to "LONG"

When a SELL signal occurs:
- Calculate profit/loss: (exit price - entry price) × shares
- Convert shares back to cash
- Record the trade with all details

### 5. Performance Calculation

After all trades are complete:
- Sum total profits and losses
- Calculate win rate
- Compute maximum drawdown from portfolio value history
- Generate comprehensive report

## 📝 Interpreting Results

### What Makes a Good Strategy?

There's no single "perfect" number, but here are general guidelines:

#### Win Rate
- **< 40%**: Poor - strategy loses more than it wins
- **40-50%**: Fair - break even or slightly profitable
- **50-60%**: Good - reliable strategy
- **> 60%**: Excellent - strong edge (but verify sample size)

#### Return (6 months)
- **< 0%**: Losing strategy
- **0-5%**: Modest returns
- **5-10%**: Good returns
- **> 10%**: Excellent returns (but consider risk)

#### Maximum Drawdown
- **< 5%**: Low risk - conservative strategy
- **5-10%**: Moderate risk - acceptable
- **10-20%**: High risk - aggressive strategy
- **> 20%**: Very high risk - consider reducing position size

### Context Matters

Always consider:

1. **Market Conditions**: Bull markets inflate results; bear markets deflate them
2. **Sample Size**: More trades = more reliable statistics (aim for 20+ trades)
3. **Timeframe**: Longer backtests provide more robust results
4. **Comparison**: Compare to buy-and-hold strategy for the same period

## 🔧 Customizing the Backtest

### Change the Stock Symbol

Edit `config.py`:

```python
STOCK_SYMBOL = "TSLA"  # Test on Tesla instead
```

### Adjust MA Parameters

Experiment with different moving average windows:

```python
SHORT_MA_WINDOW = 10   # Slower short MA
LONG_MA_WINDOW = 50    # Longer long MA
```

More conservative settings (larger windows) generate fewer signals but may be more reliable.

### Modify Initial Capital

Edit `backtest.py`:

```python
engine = BacktestEngine(
    symbol="AAPL", 
    period_months=6, 
    initial_capital=50000.0  # Start with $50k
)
```

## ⚠️ Important Limitations

### 1. Historical Bias

- **Survivorship bias**: Only tests stocks that still exist
- **Look-ahead bias**: Prevented (signals use only past data)
- **Overfitting**: Don't optimize excessively on one dataset

### 2. Execution Assumptions

- **No slippage**: Assumes trades execute at exact closing prices
- **No commissions**: Real trading has fees and commissions
- **Perfect execution**: Assumes all orders fill at desired prices
- **No market impact**: Assumes trades don't affect prices

### 3. Real-World Factors Not Modeled

- **Emotional discipline**: Backtests execute perfectly; humans don't
- **Market gaps**: Overnight gaps and halts not accounted for
- **Dividend adjustments**: Yahoo Finance data is adjusted, but may differ from reality
- **Changing volatility**: Historical volatility may differ from future

## 💡 Best Practices

### 1. Test Multiple Periods

Don't rely on a single backtest:

```bash
python main.py --backtest 3   # Q4 2025
python main.py --backtest 6   # H2 2025
python main.py --backtest 12  # All of 2025
```

### 2. Test Different Markets

Try various stocks with different characteristics:

```python
# Large cap tech
STOCK_SYMBOL = "AAPL"

# Volatile growth
STOCK_SYMBOL = "TSLA"

# Stable dividend
STOCK_SYMBOL = "KO"
```

### 3. Compare to Buy-and-Hold

Calculate simple buy-and-hold return for comparison. If your strategy underperforms buy-and-hold, it may not be worth the active trading.

### 4. Consider Risk-Adjusted Returns

A 20% return with 15% drawdown may be worse than 15% return with 5% drawdown.

### 5. Forward Testing

After backtesting, run the bot in "paper trading" mode (monitoring without executing) to validate real-time performance before risking capital.

## 🎯 Next Steps

After backtesting:

1. **Analyze Results**: Understand why certain trades won or lost
2. **Optimize Parameters**: Try different MA windows if results are poor
3. **Test Alert System**: Run `python main.py --test` to verify Discord alerts
4. **Paper Trade**: Run the bot in monitor-only mode to validate real-time signals
5. **Start Small**: If moving to live trading, start with a small position size

## 📚 Additional Resources

- See [signals.md](signals.md) for detailed explanation of MA crossover strategy
- See [troubleshooting.md](troubleshooting.md) if backtest fails
- See [faq.md](faq.md) for common questions about backtesting

---

**Remember**: Past performance does not guarantee future results. Backtesting is a tool for evaluation, not a crystal ball for future returns.
