# Data Compression (ScaleDown)

This bot uses delta compression to reduce the size of time-series price data.

## Why Compression Helps

Stock prices change slowly between 5-minute intervals. Instead of storing full
prices each time, we store one base price and the differences (deltas) between
consecutive prices. This reduces storage and speeds up processing.

## How It Works

Example prices:

```
[100.50, 100.52, 100.48, 100.51]
```

Compressed format:

- Base price: 100.50
- Deltas: [+0.02, -0.04, +0.03]

## Decompression

To reconstruct the original series:

- Start with the base price.
- Add each delta in order.

This reproduces the original data exactly.
