# Testing and Verification

This document explains how to validate the bot.

## Indicator Tests

Run the quick indicator tests:

```
python test_indicators.py
```

What it verifies:

- Moving average calculations are correct.
- Crossover detection logic behaves as expected.
- Insufficient data is handled safely.

## Alert Test

Run the alert test mode:

```
python main.py --test
```

What it verifies:

- Discord webhook is configured.
- Alerts are formatted and sent correctly.

## Live Run

Start the bot and let it run for at least 15 minutes:

```
python main.py
```

Verify that it:

- Fetches data without errors.
- Prints clear logs each cycle.
- Does not crash or spam alerts.
