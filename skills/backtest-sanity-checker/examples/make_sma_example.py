#!/usr/bin/env python3
"""Builds a real worked example for the Backtest Sanity Checker (MIT licence).

Strategy: be long the S&P 500 index while it closes above its 10-day simple moving average.
Data: S&P 500 daily close from FRED (series SP500, https://fred.stlouisfed.org/series/SP500).
The data is downloaded at run time, not shipped (S&P Dow Jones Indices owns it).

Writes two trade logs:
  trades_buggy.csv : the common vectorised bug: position not shifted, so each day's
                     return is earned using a signal that already knew that day's close.
  trades_fixed.csv : signal at today's close, trade at today's close, earn from tomorrow.
"""
import csv, io, sys, urllib.request

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500"
# Optional: pass a CSV you downloaded yourself from the URL above (FRED can be slow).
if len(sys.argv) > 1:
    raw = open(sys.argv[1], encoding="utf-8-sig").read()
else:
    raw = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "curl/8.0"}), timeout=120).read().decode()
rows = [(r["observation_date"], float(r["SP500"])) for r in csv.DictReader(io.StringIO(raw)) if r["SP500"] not in (".", "")]
with open("sp500_prices.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["date", "close"]); w.writerows(rows)
dates = [d for d, _ in rows]; close = [c for _, c in rows]
N = 10
sig = [None] * len(close)
for i in range(N - 1, len(close)):
    sig[i] = close[i] > sum(close[i - N + 1:i + 1]) / N   # uses today's close (fine as a signal)

def runs(pos):
    out, start = [], None
    for i, p in enumerate(pos + [False]):
        if p and start is None: start = i
        if not p and start is not None: out.append((start, i - 1)); start = None
    return out

def write(name, trades):
    with open(name, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["entry_date", "exit_date", "side", "entry_price", "exit_price"])
        for ed, xd, ep, xp in trades: w.writerow([ed, xd, "long", f"{ep:.2f}", f"{xp:.2f}"])

# BUGGY: position[t] = sig[t]; earns return close[t-1] -> close[t]. Log: bought at close[t-1], dated t.
buggy_pos = [bool(s) for s in sig]
bt = [(dates[a], dates[b], close[a - 1], close[b]) for a, b in runs(buggy_pos) if a >= 1]
# FIXED: position[t] = sig[t-1]; i.e. buy at the close of the signal day, hold from the next day.
fixed_pos = [False] + [bool(s) for s in sig[:-1]]
ft = [(dates[a - 1], dates[b], close[a - 1], close[b]) for a, b in runs(fixed_pos) if a >= 1]
write("trades_buggy.csv", bt); write("trades_fixed.csv", ft)
print(f"prices: {len(rows)} days {dates[0]}..{dates[-1]} | buggy trades: {len(bt)} | fixed trades: {len(ft)}")
