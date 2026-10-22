---
name: sec-filing-finder
description: Finds a US-listed company's SEC filings (10-K annual report, 10-Q quarterly report, 8-K events and earnings releases, Form 4 insider trades, proxy, 13D/13G stakes) with direct sec.gov links, and explains in plain English what each filing and 8-K item number means. Use when the user asks for a company's latest filings, annual or quarterly report, earnings release, insider buying/selling filings, or "what did X file with the SEC". Facts only, never investment advice.
license: MIT. See LICENSE in the repository root.
compatibility: Needs Python 3.8+ (standard library) and internet access to sec.gov. The user sets SEC_USER_AGENT to their name and email (an SEC requirement). Without a shell, guide the user through the EDGAR website instead.
metadata:
  author: TapeSkills
  version: "1.0"
---

# SEC Filing Finder (TapeSkills, free)

## Rules
- Only report what the filings list shows. Link every filing. Never guess filing dates or contents.
- Explain forms and item numbers using [references/form-guide.md](references/form-guide.md).
- No buy/sell calls, price targets or opinions about what a filing means for the stock. If asked, say: "I can't give buy/sell calls or price targets. Here is what was filed."
- End with: *Facts from SEC EDGAR only, not financial advice.*

## Steps
1. Make sure `SEC_USER_AGENT` is set (`export SEC_USER_AGENT="Your Name you@example.com"`). If not, ask the user for a name and email to use, or have them set it.
2. Pick the command:
   - Latest filings overall: `python3 scripts/find_filings.py TICKER`
   - Annual / quarterly reports: `--forms 10-K,10-Q`
   - Earnings releases: `--earnings` (8-Ks with Item 2.02; the release itself is usually Exhibit 99.1, found under "all files")
   - Insider trades: `--forms 4 --limit 20`
   - Since a date: `--since YYYY-MM-DD`
   - Machine-readable: `--json`
3. Present the table, then add 1-2 plain-English lines on what the main filing types are (from the form guide). If the user asks what is *in* a filing, open the document link and summarise only what it says, quoting key lines.
4. No shell? Tell the user: go to https://www.sec.gov/edgar/search/, type the ticker, then filter by form type.

## Limits
- Covers the most recent ~1,000 filings in SEC's "recent" list, which is years of history for most companies.
- Foreign companies file 20-F/6-K instead of 10-K/8-K. Very new tickers may be missing from SEC's ticker list; use the CIK number.
