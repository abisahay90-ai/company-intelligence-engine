# Company Intelligence & Interview Synthesis Engine

> Pull any public company's financial data, run it through AI, get a boardroom-ready brief — automatically.

**Built by Abhishek Sahay** | Open Source | No SaaS subscription required

---

## What This Does

You type a company ticker. You get a complete intelligence brief in under 60 seconds:

- Financial health from SEC 10-K and 10-Q filings
- Risk flags extracted by Claude AI from primary source documents
- Strategic signals from management filings
- Talking points ready for interviews or sales meetings
- PDF report generated automatically

No SaaS subscription. No manual research. No vendor lock-in.

---

## Build Progress

- [x] Phase 1 — SEC EDGAR collector ✅
- [x] Phase 2 — Claude AI synthesis engine ✅
- [x] Phase 3 — PDF brief generator ✅
- [ ] Phase 4 — Web dashboard (building now)
- [ ] Phase 5 — Automated daily scheduler (coming soon)

---

## Results So Far

| Company | Filings Collected | AI Brief | PDF Report |
|---------|------------------|----------|------------|
| Microsoft (MSFT) | ✅ 4 filings | ✅ Generated | ✅ Created |
| Tesla (TSLA) | ✅ 4 filings | ✅ Generated | ✅ Created |

---

## Quick Start

### 1. Install dependencies
```bash
pip install requests anthropic reportlab
```

### 2. Add your API key
Create a `.env` file in the project root:
```
SEC_USER_AGENT=CompanyIntelligenceEngine your@email.com
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Run the full pipeline
```bash
# Phase 1 — Collect SEC filings
python collectors/sec_collector.py --ticker TSLA

# Phase 2 — Generate AI intelligence brief
python engine/synthesizer.py --ticker TSLA

# Phase 3 — Create PDF report
python outputs/pdf_generator.py --ticker TSLA
```

---

## Sample Output
```
INTELLIGENCE BRIEF — Tesla, Inc. (TSLA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINANCIAL HEALTH [Strong]
Tesla reported full-year 2025 results showing a diversified revenue
base across automotive, energy generation and storage, and services.

RISK FLAGS
1. Restructuring charges signal ongoing operational realignment
2. Restatement of prior quarterly figures raises reporting questions
3. Regulatory credit revenue volatile and policy-dependent
4. Multiple active litigation matters across filings
5. Heavy CNY exposure from Chinese manufacturing operations

TALKING POINTS
1. Tesla's 10-K now tracks robotaxi deployments and bot deliveries
   as discrete operational metrics — material revenue, not R&D
2. Energy storage has matured into a full platform business with
   its own deferred revenue and dedicated leasing streams
3. Conservative treasury management signals financial discipline
   even while funding capital-intensive multi-segment growth
```

---

## Data Sources

| Source | What We Pull | API Key? |
|--------|-------------|----------|
| SEC EDGAR | 10-K and 10-Q filings | No — completely free |
| Google News RSS | Recent press coverage | No — completely free |
| Anthropic Claude | AI analysis and synthesis | Yes — ~$0.01 per brief |

---

## Why This Exists

Enterprise intelligence tools charge $20–100 per seat per month and
still require humans to do the heavy lifting.

This engine replaces that with:
- Fractional-cent API calls instead of SaaS subscriptions
- Primary source data direct from US government via SEC EDGAR
- Zero manual work — fully automated pipeline
- Code you own — no vendor lock-in, no black box

---

## Tech Stack

- Python 3.x
- SEC EDGAR API (free, no key needed)
- Claude AI via Anthropic API
- ReportLab for PDF generation
- Streamlit for web dashboard (Phase 4)

---

## Project Structure
```
company-intelligence-engine/
├── collectors/
│   └── sec_collector.py      ← Phase 1: pulls SEC filings
├── engine/
│   └── synthesizer.py        ← Phase 2: Claude AI analysis
├── outputs/
│   └── pdf_generator.py      ← Phase 3: PDF report generator
├── .env                      ← Your API keys (never committed)
├── .gitignore                ← Keeps secrets and data private
└── README.md
```

---

## License

MIT — use it, fork it, build on it.