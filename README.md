# Company Intelligence & Interview Synthesis Engine

> Pull any public company's financial data, run it through AI, get a boardroom-ready brief — automatically.

**Built by Abhishek Sahay** | Open Source | No SaaS subscription required

---

## What This Does

You type a company ticker. You get a complete intelligence brief:

- Financial health from SEC 10-K and 10-Q filings
- Risk flags extracted by Claude AI
- Strategic signals from earnings calls
- News pulse from last 30 days
- Talking points ready for interviews or sales meetings

---

## Build Progress

- [x] Phase 1 — SEC EDGAR collector ✅
- [x] Phase 2 — Claude AI synthesis engine ✅
- [ ] Phase 3 — PDF brief generator
- [ ] Phase 4 — Web dashboard
- [ ] Phase 5 — Automated daily scheduler

---

## Quick Start
```bash
# Company Intelligence & Interview Synthesis Engine

> Pull any public company's financial data, run it through AI, get a boardroom-ready brief — automatically.

Built by Abhishek Sahay | Open Source | No SaaS subscription required

---

## What This Does

You type a company ticker. You get a complete intelligence brief:

- Financial health from SEC 10-K and 10-Q filings
- Strategic signals from earnings call transcripts  
- News pulse from last 30 days of press coverage
- Risk flags extracted by Claude AI
- Talking points ready for interviews or sales meetings

---

## Build Progress

- [x] Phase 1 — SEC EDGAR collector (pulls real 10-K and 10-Q filings)
- [ ] Phase 2 — Claude AI synthesis engine (in progress)
- [ ] Phase 3 — PDF brief generator
- [ ] Phase 4 — Web dashboard
- [ ] Phase 5 — Automated daily scheduler

---

## Phase 1 — Quick Start

### Install
```bash
pip install requests
```

### Run
```bash
python collectors/sec_collector.py --ticker MSFT
```

### Output
```
Company  : MICROSOFT CORP
Filings  : 4 downloaded
Text     : 200,052 characters collected
File     : data/sec_filings/MSFT_sec_filings.json
```

---

## Data Sources (All Free)

| Source | What We Pull | API Key Needed? |
|--------|-------------|-----------------|
| SEC EDGAR | 10-K and 10-Q filings | No |
| Google News RSS | Recent news | No |
| NewsAPI | Richer news coverage | Free tier |

---

## Why This Exists

Enterprise intelligence tools charge $20-100 per seat per month.
This replaces them with fractional-cent API calls and code you fully own.

---

## Tech Stack

- Python 3.x
- SEC EDGAR API (free, no key needed)
- Claude AI via Anthropic API (Phase 2+)
- Streamlit for dashboard (Phase 4)
```

Now push it to GitHub:
```
git add .
```
```
git commit -m "Add README with project overview and build progress"
```
```
git push
```

---

## How to access your repo anytime
Bookmark this URL:
```
https://github.com/abisahay90-ai/company-intelligence-engine

Bookmark this URL:
```
https://github.com/abisahay90-ai/company-intelligence-engine
