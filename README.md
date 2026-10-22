# TapeSkills: free AI agent skills for traders

**Ready-made skills that do a trader's homework in Claude, ChatGPT, Cursor and Codex. Facts and checks, never tips.**

Skills follow the open [Agent Skills](https://agentskills.io/specification) format (a folder with a `SKILL.md`), so the same folder works across agents that support it. Both skills below pass the reference validator (`skills-ref validate`).

| Skill | What it does | Try asking |
|---|---|---|
| [**Backtest Sanity Checker**](skills/backtest-sanity-checker) | Finds the bugs that make backtests look too good: look-ahead, impossible fills, missing costs, too few trades, outlier-driven profit, overfitting | "Is this backtest realistic?" + your trade log CSV |
| [**SEC Filing Finder**](skills/sec-filing-finder) | Lists a company's 10-K, 10-Q, 8-K, Form 4 and 13D/G filings with direct sec.gov links and explains 8-K item numbers in plain English | "Show NVDA's latest SEC filings" |

### Real example: one missing line, +126% becomes +25,281%
We ran the Backtest Sanity Checker on a simple S&P 500 moving-average rule using 10 years of FRED data. A classic missing `.shift(1)` inflated the result from **+125.67% to +25,280.93%**. The checker flagged it as **RED** from the trade log alone: 207 of 208 entries were filled at the *previous* day's close. [See the worked example →](skills/backtest-sanity-checker/examples)

## Install

**Claude Code / Cursor / Codex:** copy the skill folders into your skills directory.
```bash
git clone https://github.com/tapeskills/trader-skills.git
cp -r trader-skills/skills/* ~/.claude/skills/     # Claude Code
cp -r trader-skills/skills/* ~/.cursor/skills/     # Cursor
cp -r trader-skills/skills/* ~/.agents/skills/     # Codex
```
**Claude.ai:** zip a skill folder (the folder itself at the root of the zip), then Customize → Skills → + → Create skill → Upload a skill. Code execution must be on (Settings → Capabilities).

**ChatGPT or any chatbot:** open the skill's `SKILL.md`, paste it into a new chat, then paste your data.

**SEC access:** the SEC asks every tool to identify itself. Set this once:
```bash
export SEC_USER_AGENT="Your Name you@example.com"
```
Scripts use only the Python standard library (3.8+). No API keys, no paid data.

## Want more?
- **Earnings Prep Pack ($19):** a one-page brief before earnings and a facts-only summary after, built from SEC filings, every number sourced. Tested on real Q3 2026 reports. → [tapeskills.pages.dev/earnings-prep](https://tapeskills.pages.dev/earnings-prep/) (launching soon)
- **Free weekly newsletter, "AI Agent Stack for Traders":** new skills, agent workflows and what's working. → [tapeskills.pages.dev/newsletter](https://tapeskills.pages.dev/newsletter/) (launching soon)

⭐ Star the repo to get new free skills as they ship.

## Principles
- **Facts, not advice.** Skills refuse buy/sell calls, price targets and position sizing.
- **Sources or it didn't happen.** Every number links back to where it came from.
- **Free data first.** SEC EDGAR, FRED and what you paste in.

## Licence and disclaimer
Free skills in this repo: [MIT](LICENSE). Paid packs are sold separately under their own licence.
Nothing here is investment advice. Backtests and summaries can be wrong; check sources and test before relying on anything. Past and simulated results do not predict future returns.

<!-- keywords: claude skills, agent skills, claude code skills, chatgpt skills, cursor skills, codex skills, trading, backtesting, backtest, look-ahead bias, overfitting, sec edgar, sec filings, 10-k, 8-k, form 4, earnings, retail traders, quant, algorithmic trading -->
