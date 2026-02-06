"""
Backtesting module for the Trading Monitor Bot.

This module allows users to test the MA crossover strategy on historical data
and evaluate its performance through various metrics.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from data_fetcher import fetch_stock_data
from indicators import calculate_moving_average, detect_ma_crossover
from config import STOCK_SYMBOL, SHORT_MA_PERIOD, LONG_MA_PERIOD


class BacktestEngine:
    """Backtesting engine for evaluating trading strategies."""
    
    def __init__(self, symbol: str, period_months: int = 6, initial_capital: float = 10000.0):
        """
        Initialize the backtest engine.
        
        Args:
            symbol: Stock ticker symbol to backtest
            period_months: Number of months of historical data to use
            initial_capital: Starting capital for simulation
        """
        self.symbol = symbol
        self.period_months = period_months
        self.initial_capital = initial_capital
        self.trades: List[Dict] = []
        self.portfolio_value: List[float] = []
        
    def run_backtest(self) -> Dict:
        """
        Execute the backtest simulation.
        
        Returns:
            Dictionary containing backtest results and performance metrics
        """
        print(f"\n{'='*60}")
        print(f"Starting Backtest for {self.symbol}")
        print(f"Period: {self.period_months} months | Initial Capital: ${self.initial_capital:,.2f}")
        print(f"{'='*60}\n")
        
        # Fetch historical data
        print(f"Fetching {self.period_months} months of historical data...")
        df = fetch_stock_data(self.symbol, period=f"{self.period_months}mo", interval="1d")
        
        if df is None or df.empty:
            return {"error": "Failed to fetch historical data"}
        
        print(f"Loaded {len(df)} trading days of data\n")
        
        # Calculate indicators
        df['Short_MA'] = calculate_moving_average(df, SHORT_MA_PERIOD)
        df['Long_MA'] = calculate_moving_average(df, LONG_MA_PERIOD)
        
        # Drop NaN values from MA calculations
        df = df.dropna()
        
        # Simulate trading
        position = None  # None, 'LONG', or 'SHORT'
        entry_price = 0.0
        entry_date = None
        shares = 0.0
        cash = self.initial_capital
        
        for i in range(1, len(df)):
            current_row = df.iloc[i]
            previous_row = df.iloc[i-1]
            
            # Detect crossover
            signal = detect_ma_crossover(
                previous_row['Short_MA'], 
                previous_row['Long_MA'],
                current_row['Short_MA'], 
                current_row['Long_MA']
            )
            
            current_price = current_row['Close']
            current_date = current_row.name
            
            # Execute trades based on signals
            if signal == "BUY" and position is None:
                # Enter long position
                shares = cash / current_price
                entry_price = current_price
                entry_date = current_date
                position = "LONG"
                cash = 0.0
                
                print(f"📈 BUY  | {current_date.strftime('%Y-%m-%d')} | Price: ${current_price:.2f} | Shares: {shares:.2f}")
                
            elif signal == "SELL" and position == "LONG":
                # Exit long position
                exit_price = current_price
                profit = (exit_price - entry_price) * shares
                profit_pct = ((exit_price - entry_price) / entry_price) * 100
                
                cash = shares * exit_price
                
                self.trades.append({
                    'entry_date': entry_date,
                    'exit_date': current_date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'shares': shares,
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'position': position
                })
                
                position = None
                shares = 0.0
                
                emoji = "✅" if profit > 0 else "❌"
                print(f"{emoji} SELL | {current_date.strftime('%Y-%m-%d')} | Price: ${exit_price:.2f} | P/L: ${profit:,.2f} ({profit_pct:+.2f}%)")
            
            # Track portfolio value
            if position == "LONG":
                portfolio_val = shares * current_price
            else:
                portfolio_val = cash
            
            self.portfolio_value.append(portfolio_val)
        
        # Close any open position at the end
        if position == "LONG":
            final_price = df.iloc[-1]['Close']
            final_date = df.iloc[-1].name
            profit = (final_price - entry_price) * shares
            profit_pct = ((final_price - entry_price) / entry_price) * 100
            
            cash = shares * final_price
            
            self.trades.append({
                'entry_date': entry_date,
                'exit_date': final_date,
                'entry_price': entry_price,
                'exit_price': final_price,
                'shares': shares,
                'profit': profit,
                'profit_pct': profit_pct,
                'position': position
            })
            
            emoji = "✅" if profit > 0 else "❌"
            print(f"{emoji} SELL | {final_date.strftime('%Y-%m-%d')} | Price: ${final_price:.2f} | P/L: ${profit:,.2f} ({profit_pct:+.2f}%) [CLOSE]")
            
            position = None
        
        # Calculate performance metrics
        results = self._calculate_metrics(cash)
        
        # Display results
        self._display_results(results)
        
        return results
    
    def _calculate_metrics(self, final_cash: float) -> Dict:
        """Calculate performance metrics from trade history."""
        
        if not self.trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "total_return": 0.0,
                "total_return_pct": 0.0,
                "avg_profit_per_trade": 0.0,
                "max_profit": 0.0,
                "max_loss": 0.0,
                "final_capital": final_cash
            }
        
        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t['profit'] > 0)
        losing_trades = sum(1 for t in self.trades if t['profit'] <= 0)
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        
        total_profit = sum(t['profit'] for t in self.trades)
        total_return_pct = ((final_cash - self.initial_capital) / self.initial_capital) * 100
        
        avg_profit = total_profit / total_trades if total_trades > 0 else 0.0
        
        max_profit = max(t['profit'] for t in self.trades)
        max_loss = min(t['profit'] for t in self.trades)
        
        # Calculate max drawdown
        max_drawdown = self._calculate_max_drawdown()
        
        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "total_return": total_profit,
            "total_return_pct": total_return_pct,
            "avg_profit_per_trade": avg_profit,
            "max_profit": max_profit,
            "max_loss": max_loss,
            "max_drawdown": max_drawdown,
            "final_capital": final_cash
        }
    
    def _calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown from portfolio value history."""
        if not self.portfolio_value:
            return 0.0
        
        peak = self.portfolio_value[0]
        max_dd = 0.0
        
        for value in self.portfolio_value:
            if value > peak:
                peak = value
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_dd:
                max_dd = drawdown
        
        return max_dd
    
    def _display_results(self, results: Dict):
        """Display formatted backtest results."""
        
        print(f"\n{'='*60}")
        print(f"BACKTEST RESULTS")
        print(f"{'='*60}\n")
        
        print(f"📊 Trading Performance:")
        print(f"   Total Trades:        {results['total_trades']}")
        print(f"   Winning Trades:      {results['winning_trades']} ✅")
        print(f"   Losing Trades:       {results['losing_trades']} ❌")
        print(f"   Win Rate:            {results['win_rate']:.2f}%\n")
        
        print(f"💰 Financial Performance:")
        print(f"   Initial Capital:     ${self.initial_capital:,.2f}")
        print(f"   Final Capital:       ${results['final_capital']:,.2f}")
        print(f"   Total Return:        ${results['total_return']:,.2f}")
        print(f"   Return %:            {results['total_return_pct']:+.2f}%\n")
        
        print(f"📈 Trade Statistics:")
        print(f"   Avg Profit/Trade:    ${results['avg_profit_per_trade']:,.2f}")
        print(f"   Best Trade:          ${results['max_profit']:,.2f}")
        print(f"   Worst Trade:         ${results['max_loss']:,.2f}")
        print(f"   Max Drawdown:        {results['max_drawdown']:.2f}%\n")
        
        # Performance verdict
        if results['total_return_pct'] > 10:
            verdict = "🎉 Excellent Performance!"
        elif results['total_return_pct'] > 0:
            verdict = "✅ Profitable Strategy"
        elif results['total_return_pct'] == 0:
            verdict = "➖ Break Even"
        else:
            verdict = "⚠️  Strategy Needs Improvement"
        
        print(f"Verdict: {verdict}")
        print(f"{'='*60}\n")


def run_backtest_cli(symbol: str = None, months: int = 6):
    """
    Run backtest from command line.
    
    Args:
        symbol: Stock symbol to backtest (default: from config)
        months: Number of months of historical data
    """
    if symbol is None:
        symbol = STOCK_SYMBOL
    
    engine = BacktestEngine(symbol=symbol, period_months=months)
    results = engine.run_backtest()
    
    return results


if __name__ == "__main__":
    # Run backtest if executed directly
    run_backtest_cli()
