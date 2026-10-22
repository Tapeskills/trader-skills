# Worked example: a one-line bug that turns +126% into +25,281%

**Rule tested:** hold the S&P 500 index while it closes above its 10-day simple moving average.
**Data:** S&P 500 daily close, FRED series SP500 (https://fred.stlouisfed.org/series/SP500), 2,512 trading days from 17 Oct 2016 to 14 Oct 2026. Price index only (no dividends). Downloaded at run time, not included here.

```bash
python3 make_sma_example.py            # downloads FRED data, writes trades_buggy.csv and trades_fixed.csv
python3 ../scripts/check_backtest.py trades_buggy.csv --prices sp500_prices.csv --cost-bps 5 --params 1 --variants-tried 10
python3 ../scripts/check_backtest.py trades_fixed.csv --prices sp500_prices.csv --cost-bps 5 --params 1 --variants-tried 10
```

| | Buggy (no shift) | Fixed (trade at signal close, earn from next day) |
|---|---|---|
| Trades | 208 | 208 |
| Total return | +25,280.93% | +125.67% |
| Win rate | 99.52% | 43.27% |
| Max drawdown (trade-by-trade) | -0.05% | -19.79% |
| t-stat of average trade | 14.50 | 2.55 |
| Break-even cost per round trip | 273.2 bps | 41.9 bps |
| Buy-and-hold, same dates | +266.19% | +262.13% |

Both totals were re-computed independently from daily returns and match to the cent.

**What the checker caught in the buggy version (from the trade log and prices alone):**
- RED: 207 of 208 entry prices equal the *previous* day's close, the signature of a missing `.shift(1)`.
- RED: 99.52% win rate with a profit factor of about 10,508: too good to be true.
- AMBER: t-stat 14.5.

**What it still flags in the fixed version (correctly):**
- AMBER: every entry fills at the same close the signal uses. That is only achievable with a market-on-close order placed just before the close.
- AMBER: after 10 variants, t-stat 2.55 is below the rough 2.81 multiple-testing bar.
- Costs: at 50 bps per round trip the result turns negative (-20.14%).

Full outputs: `report_buggy.md`, `report_fixed.md`.
