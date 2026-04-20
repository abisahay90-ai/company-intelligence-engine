# 🏛️ Sovereign Intelligence Engine

> **An Open-Source Agentic Framework for High-Fidelity Financial Analysis.**
> Moving from 'Generative Fluff' to 'Deterministic Ground Truth' — for $0.01 per brief.

**Built by [Abhishek Sahay](https://www.linkedin.com/in/abhisheksahay/)** | Open Source (MIT) | No SaaS subscription required

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data Source](https://img.shields.io/badge/Data-SEC%20EDGAR-orange)](https://edgar.sec.gov)
[![AI](https://img.shields.io/badge/AI-Claude%20Sonnet-purple)](https://anthropic.com)

---

## 📺 Live Demo

> Type any US public company ticker → get a boardroom-ready intelligence brief in 60 seconds.

![Dashboard Preview](https://via.placeholder.com/800x400/0A1628/2E86C1?text=Company+Intelligence+Engine+Dashboard)


---

## 🎯 The Problem This Solves

Enterprise teams spend **3-5 hours per company** on manual research before high-stakes meetings.
Existing SaaS tools charge **$20-100/seat/month** and still require humans to synthesize the output.

This engine eliminates both problems entirely.

---

## 🧠 System Architecture: The "Sovereign" Approach

Unlike generic RAG tools that summarize whatever text you paste in, this engine runs a
**Multi-Stage Synthesis Pipeline** designed to eliminate hallucinations and ensure
every claim is traceable to a primary government source.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOVEREIGN INTELLIGENCE ENGINE                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [1] DIRECT SEC INGESTION                                        │
│      └─ Bypasses third-party aggregators                         │
│      └─ Pulls raw XBRL/JSON directly from SEC EDGAR             │
│      └─ Zero data vendor dependency                              │
│                          ↓                                       │
│  [2] CONTEXT-AWARE CHUNKING                                      │
│      └─ Maps 200k+ characters into thematic nodes               │
│      └─ Risk Section → Risk Analysis node                        │
│      └─ MD&A Section → Strategy Analysis node                    │
│      └─ Financials → Health Score node                           │
│                          ↓                                       │
│  [3] CLAUDE AI ORCHESTRATION                                     │
│      └─ Prompted as Principal Equity Analyst                     │
│      └─ Cross-document reasoning (10-Q vs 10-K)                 │
│      └─ Ignores PR spin, focuses on Management Bets             │
│      └─ Structured JSON output — no free-form hallucination     │
│                          ↓                                       │
│  [4] DETERMINISTIC OUTPUT LAYER                                  │
│      └─ PDF consulting-grade artifact                            │
│      └─ Web dashboard (Streamlit)                                │
│      └─ Slack / email digest (Phase 5)                          │
│      └─ Every claim linked to primary source filing             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 Unit Economics vs. Traditional SaaS

| Metric | Traditional Enterprise SaaS | Sovereign Intelligence Engine |
|--------|----------------------------|-------------------------------|
| Monthly Cost | $20 – $100 / user | $0 (Open Source) |
| Cost Per Brief | Included in subscription | ~$0.01 (inference cost only) |
| Data Privacy | Vendor-stored | Local / Private Cloud |
| Data Source | Aggregator (lagged) | SEC EDGAR (primary, real-time) |
| Auditability | Black box | Primary source linked |
| Customization | Limited | Full — you own the code |
| Scale (500 companies) | $10,000–$50,000/month | ~$5/month |

> **The ROI case:** A 10-person enterprise team replacing a $50/seat tool saves **$6,000/year**.
> At 500 companies monitored daily, traditional tools cost **$600,000/year**. This engine: **$60/year**.

---

## 🔬 Research Philosophy: First Principles Prompting

Most AI tools tell Claude to "summarize this document." This engine operates differently.

**The engine prompts Claude to act as a Principal Equity Analyst with three directives:**

1. **Ignore PR Spin** — Management Discussion sections are written by lawyers. The engine
   is instructed to focus on *what changed* between periods, not what management *claims* changed.

2. **Follow the Management Bets** — R&D spend vs. revenue realization. CapEx direction.
   Headcount changes. These are the signals that predict strategic pivots 2-3 quarters ahead.

3. **Surface the Buried Risk** — SEC 10-K risk sections contain legally-required disclosures
   that management buries in boilerplate. The engine is instructed to extract *specific,
   named risks* — not generic category labels.

This approach produces briefs that are **materially different** from what you get by
pasting a filing into ChatGPT.

---

## ✅ Build Progress

- [x] Phase 1 — SEC EDGAR collector ✅
- [x] Phase 2 — Claude AI synthesis engine ✅
- [x] Phase 3 — PDF brief generator ✅
- [x] Phase 4 — Web dashboard ✅
- [x] Phase 5 — Autonomous scheduler + Slack delivery ✅

---

## 📊 Results So Far

| Company | Filings Collected | AI Brief | PDF Report |
|---------|------------------|----------|------------|
| Microsoft (MSFT) | ✅ 4 filings | ✅ Generated | ✅ Created |
| Tesla (TSLA) | ✅ 4 filings | ✅ Generated | ✅ Created |
| NVIDIA (NVDA) | ✅ 4 filings | ✅ Generated | ✅ Created |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/abisahay90-ai/company-intelligence-engine.git
cd company-intelligence-engine
```

### 2. Install dependencies
```bash
pip install requests anthropic reportlab streamlit
```

### 3. Configure environment (security best practice)
Create a `.env` file — this file is gitignored and never committed:
```
SEC_USER_AGENT=CompanyIntelligenceEngine your@email.com
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Get your free Anthropic API key at: https://console.anthropic.com

### 4. Run the full pipeline
```bash
# Phase 1 — Collect SEC filings (free, no key needed)
python collectors/sec_collector.py --ticker TSLA

# Phase 2 — Generate AI intelligence brief (~$0.01)
python engine/synthesizer.py --ticker TSLA

# Phase 3 — Create PDF report
python outputs/pdf_generator.py --ticker TSLA

# Phase 4 — Launch web dashboard
python -m streamlit run outputs/dashboard.py
```

---

## 📁 Project Structure

```
company-intelligence-engine/
├── collectors/
│   └── sec_collector.py       ← Phase 1: Direct SEC EDGAR ingestion
├── engine/
│   └── synthesizer.py         ← Phase 2: Claude AI orchestration
├── outputs/
│   ├── pdf_generator.py       ← Phase 3: Consulting-grade PDF artifacts
│   └── dashboard.py           ← Phase 4: Streamlit web dashboard
├── .env                       ← API keys (gitignored — never committed)
├── .gitignore                 ← Security: excludes secrets and raw data
└── README.md
```

---

## 🗺️ Roadmap

### Phase 5 — Autonomous Daily Scheduler (In Progress)
- Cron job runs pipeline every morning at 6am
- Pushes briefs to Slack channel or WhatsApp
- GitHub Actions for zero-infrastructure automation

### Future Vision — Agentic Orchestration
Moving from **Read-Only** to **Actionable Intelligence:**

- Trigger Zendesk / ServiceNow tickets when financial risk thresholds are breached
- Auto-flag partner portfolio companies showing deteriorating health scores
- Cross-company pattern detection — identify sector-wide risk signals before they hit the news
- Integration with CRM (Salesforce) to enrich account records with live financial intelligence

> *"The next frontier isn't better summarization — it's AI that takes action on what it reads."*

---

## 🛡️ Data Sources

| Source | What We Pull | API Key? | Latency |
|--------|-------------|----------|---------|
| SEC EDGAR | 10-K and 10-Q filings | No — completely free | Same-day filing |
| Google News RSS | Recent press coverage | No — completely free | Real-time |
| Anthropic Claude | AI analysis and synthesis | Yes — ~$0.01/brief | 15-30 seconds |

---

## 📜 License

MIT — use it, fork it, build on it. Attribution appreciated.

---

## 👤 Author

**Abhishek Sahay** — Senior Product Leader | AI/ML & LLM Copilots

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/abhisheksahay/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/abisahay90-ai)

> *"The most competitive companies won't be the ones with the most AI licenses —
> they'll be the ones with the best internal agent infrastructure."*