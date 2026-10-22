# Backtest sanity check

Trade file: `trades_fixed.csv` | Price file: `sp500_prices.csv`
Period: 2016-11-07 to 2026-10-14 | Trades: 208 | Unreadable rows: 0

## Summary of flags

- **AMBER**: Most entries fill at the same day's close. That is only realistic if the signal is known BEFORE the close (e.g. market-on-close order using data up to a few minutes earlier). If the signal uses that close, shift fills to the next bar.
- **AMBER**: After trying 10 variants, a t-stat of 2.55 is below the ~2.81 bar. The best variant may be luck.

*Automatic checks only. They cannot see survivorship bias, adjusted vs unadjusted prices, or look-ahead inside indicators: use the manual checklist.*

## 1. Data hygiene
- Exit before entry: 0 | Duplicate trades: 0 | Trades opened before the previous one closed: 0

## 2. Are the fills possible? (checked against the price file)
- Fill dates missing from price data (holidays, wrong calendar, or bad dates): 0 of 416
- Entry prices match: same-day close: 208
- Exit prices match: same-day close: 208
- Buy-and-hold over the same dates: 262.13% | Strategy time in market: 64.86%

## 3. Headline numbers (from the trade log, before any costs you add)
| Metric | Value |
|---|---|
| Total return (compounded, 1 position at a time) | 125.67% |
| Annualised (CAGR) | 8.54% |
| Win rate | 43.27% |
| Average trade | 41.9 bps |
| Average win / average loss | 237.1 / -106.9 bps |
| Profit factor | 1.69 |
| Max drawdown (trade-by-trade) | -19.79% |
| Average holding period | 11.3 calendar days |
| t-stat of average trade | 2.55 |

## 4. Cost sensitivity (round-trip cost per trade)
| Cost per round trip | Total return | Annualised |
|---|---|---|
| 0 bps | 125.67% | 8.54% |
| 5 bps | 103.45% | 7.41% |
| 10 bps | 83.41% | 6.30% |
| 20 bps | 49.03% | 4.10% |
| 50 bps | -20.14% | -2.24% |
- Break-even cost: about **41.9 bps per round trip** (the average trade). Above that, the strategy loses money.

## 5. Is the profit fragile?
- Total return without the best 5 trades: 45.05% (with them: 125.67%)
| Year | Trades | Return | Win rate |
|---|---|---|---|
| 2016 | 3 | 4.77% | 66.67% |
| 2017 | 25 | 4.32% | 32.00% |
| 2018 | 16 | 8.81% | 62.50% |
| 2019 | 15 | 17.55% | 53.33% |
| 2020 | 17 | 27.03% | 52.94% |
| 2021 | 24 | 3.66% | 41.67% |
| 2022 | 22 | -14.76% | 27.27% |
| 2023 | 23 | 7.95% | 39.13% |
| 2024 | 25 | 19.34% | 52.00% |
| 2025 | 23 | 3.78% | 43.48% |
| 2026 | 15 | 7.57% | 33.33% |
- First half of trades: 78.11% | Second half: 26.70%

## 6. Overfitting risk
- Trades per tuned parameter: 208
- You tried 10 variants. A rough multiple-testing bar (Bonferroni, 5%) for the t-stat is 2.81; this result is 2.55.
- Note: buy-and-hold returned 262.13% over the same dates vs 125.67% for the strategy (strategy was in the market less of the time).
