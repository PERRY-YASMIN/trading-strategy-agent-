# Changelog

## v1.1 (February 2026)

### 🎉 NEW FEATURE: Backtesting Engine

- Added comprehensive backtesting module (`backtest.py`)
- Test the MA crossover strategy on historical data
- Performance metrics: win rate, total return, max drawdown
- Configurable backtest period (default: 6 months)
- Command: `python main.py --backtest [months]`
- Detailed backtest documentation added
- Visual trade history with profit/loss for each trade

### Improvements

- Enhanced command-line interface with `--backtest` flag
- Updated documentation with backtesting guide
- Added performance verdict system (Excellent/Profitable/Needs Improvement)

## v1.0 (February 2026)

- Initial release
- Yahoo Finance data fetch
- Moving average crossover signals
- Delta compression (ScaleDown)
- Discord webhook alerts
- Basic tests and documentation
