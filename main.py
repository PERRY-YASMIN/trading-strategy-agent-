"""
Main entry point for the Trading Monitor & Alert Bot.

This bot continuously monitors stock prices, calculates technical indicators,
and sends alerts when buy/sell signals are detected.

WORKFLOW:
1. Fetch latest stock price data (5-minute intervals)
2. Compress data for efficient storage
3. Calculate moving averages
4. Detect crossover signals
5. Send Discord alerts when new signals appear
6. Wait and repeat
"""

import time
from datetime import datetime
import config
import data_fetcher
import compressor
import indicators
import alert


def test_alert_system():
    """
    Quick test to verify Discord webhook and alert formatting work.
    This sends a single test alert without running the full bot.
    """
    print("=" * 60)
    print("  TESTING ALERT SYSTEM")
    print("=" * 60)
    
    print("\n🧪 Sending test BUY alert...")
    success = alert.send_discord_alert(
        symbol="AAPL",
        signal_type="BUY",
        current_price=123.45,
        ma_values={'short_ma': 124.00, 'long_ma': 122.50, 'current_price': 123.45}
    )
    
    if success:
        print("✓ BUY alert sent successfully!")
    else:
        print("✗ BUY alert failed!")
    
    print("\n🧪 Sending test SELL alert...")
    success = alert.send_discord_alert(
        symbol="AAPL",
        signal_type="SELL",
        current_price=123.45,
        ma_values={'short_ma': 122.00, 'long_ma': 124.50, 'current_price': 123.45}
    )
    
    if success:
        print("✓ SELL alert sent successfully!")
    else:
        print("✗ SELL alert failed!")
    
    print("\n✓ Alert system test complete!")


def main():
    """
    Main function to run the trading bot.
    Coordinates all components and manages the main execution loop.
    """
    print("=" * 60)
    print("  TRADING MONITOR & ALERT BOT")
    print("=" * 60)
    
    # Initialize and display configuration
    if not initialize_bot():
        return
    
    # Run the main monitoring loop
    run_monitoring_loop()


def initialize_bot():
    """
    Initialize bot configuration and display startup information.
    """
    print("\n🔧 INITIALIZING BOT...")
    print(f"   Stock Symbol: {config.STOCK_SYMBOL}")
    print(f"   Fetch Interval: {config.FETCH_INTERVAL_MINUTES} minutes")
    print(f"   Lookback Period: {config.LOOKBACK_PERIOD_DAYS} days")
    print(f"   Short MA Window: {config.SHORT_MA_WINDOW}")
    print(f"   Long MA Window: {config.LONG_MA_WINDOW}")
    print(f"   Discord Webhook: {'Configured ✓' if config.is_webhook_configured() else 'Not configured ✗'}")
    
    # Validate configuration
    if not config.validate_config():
        print("\n✗ Configuration validation failed!")
        return False
    
    print("\n✓ Bot initialized successfully!")
    print(f"\n⏰ Starting monitoring loop (checking every {config.FETCH_INTERVAL_MINUTES} minutes)...\n")
    return True


def run_monitoring_loop():
    """
    Execute the main monitoring loop.
    
    This loop runs indefinitely, checking for trading signals every 5 minutes.
    It tracks the previous signal to avoid sending duplicate alerts.
    """
    # Track the last signal to only alert on NEW signals
    previous_signal = None
    
    # Keep track of iteration count for logging
    iteration = 0
    
    # Main infinite loop
    while True:
        iteration += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("=" * 60)
        print(f"[{timestamp}] Iteration #{iteration}")
        print("=" * 60)
        
        try:
            # STEP 1: Fetch latest stock data
            print(f"\n📊 Fetching data for {config.STOCK_SYMBOL}...")
            price_data = data_fetcher.fetch_stock_data(
                symbol=config.STOCK_SYMBOL,
                period_days=config.LOOKBACK_PERIOD_DAYS
            )
            
            # Validate that data was fetched successfully
            if not data_fetcher.validate_data(price_data):
                print("✗ Failed to fetch valid data. Retrying in next cycle...")
                time.sleep(config.FETCH_INTERVAL_SECONDS)
                continue
            
            print(f"✓ Fetched {len(price_data)} price data points")
            print(f"   Latest Price: ${price_data.iloc[-1]:.2f}")
            
            # STEP 2: Compress data for efficient storage
            print(f"\n💾 Compressing data...")
            compressed_data = compressor.compress_market_data(price_data)
            
            if compressed_data:
                # Calculate and display compression efficiency
                compressor.calculate_compression_ratio(price_data, compressed_data)
            
            # STEP 3: Calculate moving averages and detect signals
            print(f"\n📈 Calculating indicators...")
            print(f"   Short MA ({config.SHORT_MA_WINDOW} periods)")
            print(f"   Long MA ({config.LONG_MA_WINDOW} periods)")
            
            # Detect crossover signal
            current_signal = indicators.detect_ma_crossover(
                price_data=price_data,
                short_window=config.SHORT_MA_WINDOW,
                long_window=config.LONG_MA_WINDOW
            )
            
            # Get current MA values for display and alerts
            ma_values = indicators.get_latest_ma_values(
                price_data=price_data,
                short_window=config.SHORT_MA_WINDOW,
                long_window=config.LONG_MA_WINDOW
            )
            
            if ma_values:
                print(f"   Current Price: ${ma_values['current_price']}")
                print(f"   Short MA: ${ma_values['short_ma']}")
                print(f"   Long MA: ${ma_values['long_ma']}")
            
            # STEP 4: Handle signal detection and alerts
            print(f"\n🔔 Signal Status: {current_signal if current_signal else 'No signal'}")
            
            # Only send alert if this is a NEW signal (different from previous)
            if current_signal and current_signal != previous_signal:
                print(f"   🚨 NEW {current_signal} SIGNAL DETECTED!")
                
                # Send Discord alert
                print(f"   📤 Sending Discord alert...")
                alert_sent = alert.send_discord_alert(
                    symbol=config.STOCK_SYMBOL,
                    signal_type=current_signal,
                    current_price=price_data.iloc[-1],
                    ma_values=ma_values
                )
                
                # Log the alert to file if sent successfully
                if alert_sent:
                    alert.log_alert(
                        symbol=config.STOCK_SYMBOL,
                        signal_type=current_signal,
                        current_price=price_data.iloc[-1]
                    )
                
                # Update tracking
                previous_signal = current_signal
            
            elif current_signal == previous_signal:
                print(f"   ℹ️  Signal unchanged (still {current_signal})")
            
            else:
                print(f"   ℹ️  No trading signal detected")
                previous_signal = None
            
            # STEP 5: Wait before next iteration
            print(f"\n⏳ Waiting {config.FETCH_INTERVAL_MINUTES} minutes until next check...")
            print(f"   Next check at: {datetime.fromtimestamp(time.time() + config.FETCH_INTERVAL_SECONDS).strftime('%Y-%m-%d %H:%M:%S')}")
            
            time.sleep(config.FETCH_INTERVAL_SECONDS)
        
        except KeyboardInterrupt:
            # User pressed Ctrl+C
            print("\n\n🛑 Bot stopped by user")
            print("Shutting down gracefully...")
            break
        
        except Exception as e:
            # Catch any unexpected errors
            print(f"\n✗ ERROR: {str(e)}")
            print(f"   Retrying in {config.FETCH_INTERVAL_MINUTES} minutes...")
            time.sleep(config.FETCH_INTERVAL_SECONDS)


if __name__ == "__main__":
    import sys
    
    # Run test mode if --test argument is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_alert_system()
    else:
        main()
