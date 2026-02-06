# Signal Logic

This document explains how BUY and SELL signals are generated.

## Moving Average Crossover

Two simple moving averages are used:

- Short MA (default: 5 periods)
- Long MA (default: 20 periods)

## Signal Rules

- BUY when short MA crosses above long MA.
- SELL when short MA crosses below long MA.
- No signal if there is no crossover.

## Key Details

- A crossover is only detected when the relationship changes between two
  consecutive points.
- The bot does not emit a signal just because short MA is above long MA.
- This avoids duplicate alerts and false positives.
