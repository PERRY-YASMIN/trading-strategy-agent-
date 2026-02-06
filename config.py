"""
Configuration Module
Stores configuration settings for the trading bot.
Includes API keys, trading parameters, alert settings, etc.
"""


# ============================================================================
# TRADING CONFIGURATION
# ============================================================================

# Stock symbol to monitor
# Default is Apple Inc. (AAPL)
STOCK_SYMBOL = "AAPL"

# Data fetch interval in minutes
# Bot will fetch new data every 5 minutes
FETCH_INTERVAL_MINUTES = 5

# Historical data lookback period in days
# Used for calculating technical indicators
LOOKBACK_PERIOD_DAYS = 30


# ============================================================================
# TECHNICAL INDICATOR CONFIGURATION
# ============================================================================

# Short-term Moving Average window (in periods)
# Used for quick trend detection
SHORT_MA_WINDOW = 5

# Long-term Moving Average window (in periods)
# Used for overall trend analysis
LONG_MA_WINDOW = 20


# ============================================================================
# ALERT CONFIGURATION
# ============================================================================

# Discord webhook URL for sending alerts
# Get your webhook URL from Discord Server Settings > Integrations > Webhooks
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1469363655643627640/_ZnU0uybiy-gjAFUm7pO2BjA4q_1ZtrSLpvdZUHY34aT0Nkt3opasAJvFr-9bOPL7EkS"


# ============================================================================
# DERIVED SETTINGS (DO NOT MODIFY)
# ============================================================================

# Convert fetch interval to seconds for internal use
FETCH_INTERVAL_SECONDS = FETCH_INTERVAL_MINUTES * 60


# ============================================================================
# CONFIGURATION VALIDATION FUNCTIONS
# ============================================================================

def is_webhook_configured():
    """
    Check if Discord webhook URL is properly configured.
    
    Returns:
        Boolean indicating if webhook is configured
    """
    return DISCORD_WEBHOOK_URL and "YOUR_WEBHOOK" not in DISCORD_WEBHOOK_URL


def validate_config():
    """
    Validate configuration settings.
    
    Returns:
        Boolean indicating if configuration is valid
    """
    # Check required settings are positive numbers
    if FETCH_INTERVAL_MINUTES <= 0:
        print("Error: FETCH_INTERVAL_MINUTES must be positive")
        return False
    
    if LOOKBACK_PERIOD_DAYS <= 0:
        print("Error: LOOKBACK_PERIOD_DAYS must be positive")
        return False
    
    if SHORT_MA_WINDOW <= 0 or LONG_MA_WINDOW <= 0:
        print("Error: MA windows must be positive")
        return False
    
    if SHORT_MA_WINDOW >= LONG_MA_WINDOW:
        print("Error: SHORT_MA_WINDOW must be less than LONG_MA_WINDOW")
        return False
    
    return True
