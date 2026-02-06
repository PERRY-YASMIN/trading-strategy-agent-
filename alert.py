"""
Alert Module

Manages alert generation and notification delivery via Discord webhooks.
Sends formatted trading signals to Discord channels when buy/sell conditions are met.
"""

import requests
from datetime import datetime
import config


def _get_signal_format(signal_type):
    """
    Get emoji and color for a signal type.
    
    Args:
        signal_type: "BUY", "SELL", or other
    
    Returns:
        Tuple of (emoji, color, title)
    """
    if signal_type == "BUY":
        return "🟢", 3066993, "BUY SIGNAL DETECTED"  # Green
    elif signal_type == "SELL":
        return "🔴", 15158332, "SELL SIGNAL DETECTED"  # Red
    else:
        return "⚪", 9807270, "TRADING ALERT"  # Gray


def send_discord_alert(symbol, signal_type, current_price, ma_values=None):
    """
    Send a trading alert to Discord using a webhook.
    
    Formats and sends a message when a BUY or SELL signal is detected.
    The message includes the stock symbol, signal type, current price,
    and optional moving average values.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
        signal_type: "BUY" or "SELL"
        current_price: Current stock price
        ma_values: Optional dict with 'short_ma' and 'long_ma' values
    
    Returns:
        Boolean indicating if alert was sent successfully
    """
    # Get webhook URL from config (not hardcoded)
    webhook_url = config.DISCORD_WEBHOOK_URL
    
    # Validate webhook URL
    if not webhook_url or "YOUR_WEBHOOK" in webhook_url:
        print("Warning: Discord webhook URL not configured in config.py")
        return False
    
    # Get signal formatting (emoji, color, title)
    emoji, color, title = _get_signal_format(signal_type)
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create Discord webhook payload
    # Using Discord's embed format for better formatting
    payload = {
        "embeds": [{
            "title": f"{emoji} {title}",
            "description": f"**{symbol}** trading signal detected",
            "color": color,
            "fields": [
                {
                    "name": "Signal Type",
                    "value": signal_type,
                    "inline": True
                },
                {
                    "name": "Current Price",
                    "value": f"${current_price:.2f}",
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Trading Monitor Bot • {timestamp}"
            }
        }]
    }
    
    # Add MA values to embed if provided
    if ma_values:
        payload["embeds"][0]["fields"].extend([
            {
                "name": "Short MA",
                "value": f"${ma_values.get('short_ma', 'N/A')}",
                "inline": True
            },
            {
                "name": "Long MA",
                "value": f"${ma_values.get('long_ma', 'N/A')}",
                "inline": True
            }
        ])
    
    # Send the webhook request
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=30  # 30 second timeout
        )
        
        # Check if request was successful
        if response.status_code == 204:
            print(f"✓ Discord alert sent successfully for {symbol} {signal_type} signal")
            return True
        else:
            print(f"✗ Discord webhook failed with status code: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("✗ Discord webhook request timed out")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to send Discord alert: {str(e)}")
        return False
    
    except Exception as e:
        print(f"✗ Unexpected error sending Discord alert: {str(e)}")
        return False


def format_alert_message(symbol, signal_type, current_price):
    """
    Format a simple text alert message.
    
    Args:
        symbol: Stock ticker symbol
        signal_type: "BUY" or "SELL"
        current_price: Current stock price
    
    Returns:
        Formatted string message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emoji, _, _ = _get_signal_format(signal_type)

    # Add trend arrows for BUY/SELL
    if signal_type == "BUY":
        emoji = f"{emoji} 📈"
    elif signal_type == "SELL":
        emoji = f"{emoji} 📉"

    message = f"{emoji} {signal_type} SIGNAL\n"
    message += f"Symbol: {symbol}\n"
    message += f"Price: ${current_price:.2f}\n"
    message += f"Time: {timestamp}"

    return message


def log_alert(symbol, signal_type, current_price, filename="alerts.log"):
    """
    Log alert to a file for record-keeping.
    
    Args:
        symbol: Stock ticker symbol
        signal_type: "BUY" or "SELL"
        current_price: Current stock price
        filename: Log file name
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {symbol} - {signal_type} signal at ${current_price:.2f}\n"

    try:
        with open(filename, "a") as log_file:
            log_file.write(log_entry)
        print(f"Alert logged to {filename}")
    except Exception as e:
        print(f"Failed to log alert: {str(e)}")
