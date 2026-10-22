# Backtest sanity check

Trade file: `trades_buggy.csv` | Price file: `sp500_prices.csv`
Period: 2016-11-07 to 2026-10-13 | Trades: 208 | Unreadable rows: 0

## Summary of flags

- **RED**: 207 of 208 entry prices equal an EARLIER day's close than the entry date. Classic look-ahead: the signal uses today's data but the fill is at yesterday's price (e.g. a missing .shift(1)).
- **RED**: Win rate 99.52% with profit factor 10508: too good to be true for almost any real strategy. Assume a bug (look-ahead, wrong prices) until proven otherwise.
- **AMBER**: t-stat 14.5 is unusually high for a trading strategy. Re-check for look-ahead or data errors before celebrating.

*Automatic checks only. They cannot see survivorship bias, adjusted vs unadjusted prices, or look-ahead inside indicators: use the manual checklist.*

## 1. Data hygiene
- Exit before entry: 0 | Duplicate trades: 0 | Trades opened before the previous one closed: 0

## 2. Are the fills possible? (checked against the price file)
- Fill dates missing from price data (holidays, wrong calendar, or bad dates): 0 of 416
- Entry prices match: close -1 day(s): 207, same-day close: 1
- Exit prices match: same-day close: 208
- Buy-and-hold over the same dates: 266.19% | Strategy time in market: 56.55%

## 3. Headline numbers (from the trade log, before any costs you add)
| Metric | Value |
|---|---|
| Total return (compounded, 1 position at a time) | 25280.93% |
| Annualised (CAGR) | 74.64% |
| Win rate | 99.52% |
| Average trade | 273.2 bps |
| Average win / average loss | 274.5 / -5.4 bps |
| Profit factor | 10507.88 |
| Max drawdown (trade-by-trade) | -0.05% |
| Average holding period | 10.0 calendar days |
| t-stat of average trade | 14.50 |

## 4. Cost sensitivity (round-trip cost per trade)
| Cost per round trip | Total return | Annualised |
|---|---|---|
| 0 bps | 25280.93% | 74.64% |
| 5 bps | 22835.19% | 72.87% |
| 10 bps | 20624.10% | 71.11% |
| 20 bps | 16818.35% | 67.65% |
| 50 bps | 9093.64% | 57.66% |
- Break-even cost: about **273.2 bps per round trip** (the average trade). Above that, the strategy loses money.

## 5. Is the profit fragile?
- Total return without the best 5 trades: 13276.53% (with them: 25280.93%)
| Year | Trades | Return | Win rate |
|---|---|---|---|
| 2016 | 3 | 9.35% | 100.00% |
| 2017 | 25 | 32.03% | 100.00% |
| 2018 | 16 | 49.71% | 100.00% |
| 2019 | 15 | 61.80% | 100.00% |
| 2020 | 18 | 143.80% | 100.00% |
| 2021 | 23 | 63.30% | 95.65% |
| 2022 | 23 | 107.84% | 100.00% |
| 2023 | 23 | 79.39% | 100.00% |
| 2024 | 24 | 77.38% | 100.00% |
| 2025 | 23 | 88.32% | 100.00% |
| 2026 | 15 | 46.35% | 100.00% |
- First half of trades: 1435.62% | Second half: 1552.81%

## 6. Overfitting risk
- Trades per tuned parameter: 208
- You tried 10 variants. A rough multiple-testing bar (Bonferroni, 5%) for the t-stat is 2.81; this result is 14.50.
