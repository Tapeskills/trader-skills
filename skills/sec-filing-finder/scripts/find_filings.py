#!/usr/bin/env python3
"""TapeSkills SEC Filing Finder (MIT licence). Standard library only, Python 3.8+.

Lists a company's recent SEC filings with direct links, and decodes 8-K item numbers
into plain English. Uses the free SEC EDGAR APIs (data.sec.gov).

The SEC requires a User-Agent with your contact details:
  export SEC_USER_AGENT="Your Name you@example.com"

Examples:
  python3 find_filings.py NVDA                      # last 15 filings of the main types
  python3 find_filings.py AAPL --forms 10-K,10-Q    # annual + quarterly reports
  python3 find_filings.py TSLA --forms 4 --limit 20 # insider transactions
  python3 find_filings.py MSFT --forms 8-K --since 2026-07-01
  python3 find_filings.py JNJ --earnings            # only 8-Ks with Item 2.02 (earnings releases)
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

ITEMS = {
    "1.01": "Entered a material agreement", "1.02": "Ended a material agreement", "1.03": "Bankruptcy or receivership",
    "1.05": "Material cybersecurity incident", "2.01": "Completed an acquisition or sale of assets",
    "2.02": "Earnings release (results of operations)", "2.03": "New debt or off-balance-sheet obligation",
    "2.04": "Event that accelerates a debt obligation", "2.05": "Exit or restructuring costs", "2.06": "Material impairment",
    "3.01": "Delisting notice or listing rule failure", "3.02": "Unregistered sale of shares", "3.03": "Change to shareholder rights",
    "4.01": "Auditor change", "4.02": "Past financial statements should no longer be relied on",
    "5.01": "Change in control", "5.02": "Director or officer change / compensation", "5.03": "Bylaw or fiscal-year change",
    "5.05": "Code of ethics change or waiver", "5.07": "Shareholder vote results", "5.08": "Shareholder director nominations",
    "7.01": "Regulation FD disclosure (often presentations or guidance)", "8.01": "Other events", "9.01": "Financial statements and exhibits",
}
DEFAULT_FORMS = ["10-K", "10-Q", "8-K", "DEF 14A", "S-1", "20-F", "6-K", "10-K/A", "10-Q/A", "8-K/A", "SC 13D", "SC 13G", "SCHEDULE 13D", "SCHEDULE 13G"]

def ua():
    u = os.environ.get("SEC_USER_AGENT", "").strip()
    if "@" not in u:
        sys.exit('Set SEC_USER_AGENT first (SEC rule), e.g.: export SEC_USER_AGENT="Your Name you@example.com"')
    return u

def get(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua(), "Accept-Encoding": "identity"})
            with urllib.request.urlopen(req, timeout=30) as r:
                time.sleep(0.15)  # stay well under the SEC's 10 requests/second limit
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404: sys.exit(f"Not found: {url}")
            time.sleep(1 + attempt)
        except urllib.error.URLError:
            time.sleep(1 + attempt)
    sys.exit(f"Could not reach {url} after 3 tries")

def cik_for(ticker):
    t = ticker.upper().replace(".", "-")
    if t.isdigit(): return int(t), t
    for row in get("https://www.sec.gov/files/company_tickers.json").values():
        if row["ticker"].upper() == t: return int(row["cik_str"]), row["title"]
    sys.exit(f"Ticker {ticker} not found in SEC's ticker list (foreign or delisted companies may need their CIK number).")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker", help="ticker or CIK number")
    ap.add_argument("--forms", help="comma-separated form types, e.g. 10-K,10-Q,8-K,4")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--since", help="YYYY-MM-DD")
    ap.add_argument("--earnings", action="store_true", help="only 8-Ks that contain an earnings release (Item 2.02)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    cik, name = cik_for(a.ticker)
    sub = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    rec = sub["filings"]["recent"]
    forms = [f.strip().upper() for f in a.forms.split(",")] if a.forms else DEFAULT_FORMS
    if a.earnings: forms = ["8-K"]
    out = []
    for i in range(len(rec["form"])):
        f, d = rec["form"][i], rec["filingDate"][i]
        if f.upper() not in forms: continue
        if a.since and d < a.since: continue
        items = [x for x in (rec.get("items", [""] * (i + 1))[i] or "").split(",") if x]
        if a.earnings and "2.02" not in items: continue
        acc = rec["accessionNumber"][i]; nodash = acc.replace("-", "")
        base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{nodash}"
        out.append({"form": f, "filed": d, "period": rec.get("reportDate", [""] * (i + 1))[i],
                    "items": [f"{x} {ITEMS.get(x, '')}".strip() for x in items],
                    "description": rec.get("primaryDocDescription", [""] * (i + 1))[i],
                    "document": f"{base}/{rec['primaryDocument'][i]}" if rec["primaryDocument"][i] else "",
                    "index": f"{base}/{acc}-index.html"})
        if len(out) >= a.limit: break
    if a.json:
        print(json.dumps({"company": sub.get("name", name), "cik": cik, "filings": out}, indent=2)); return
    print(f"# {sub.get('name', name)} (CIK {cik}): {len(out)} filing(s)\n")
    print("| Filed | Form | Period | What it is | Links |\n|---|---|---|---|---|")
    for o in out:
        what = "; ".join(o["items"]) if o["items"] else (o["description"] or "")
        print(f"| {o['filed']} | {o['form']} | {o['period'] or ''} | {what} | [document]({o['document']}) · [all files]({o['index']}) |")
    if not out: print("| | | | none found with these filters | |")
    print(f"\nSource: SEC EDGAR, https://data.sec.gov/submissions/CIK{cik:010d}.json")

if __name__ == "__main__":
    main()
