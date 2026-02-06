# Troubleshooting

## Import errors (yfinance, pandas, requests)

Install dependencies:

```
pip install -r requirements.txt
```

## No data returned

- Confirm the stock symbol is valid.
- Ensure your internet connection is active.

## Discord alerts not sending

- Verify DISCORD_WEBHOOK_URL in config.py.
- Make sure the webhook is not expired or revoked.
- Try the alert test: python main.py --test

## Bot seems stuck

The bot sleeps for 5 minutes between cycles. This is expected behavior.
