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

Enterprise teams spend 3–5 hours manually researching a single public company before earnings calls, investment decisions, or board meetings.

Existing SaaS tools:
- Aggregate secondary data
- Provide generic summaries
- Still require manual synthesis and validation

This system removes manual synthesis by directly converting SEC filings into structured, decision-ready intelligence briefs.

---

## 🧠 System Architecture: The "Sovereign" Approach

Unlike generic RAG tools that summarize whatever text you paste in, this engine runs a
**Multi-Stage Synthesis Pipeline** designed to eliminate hallucinations and ensure
every claim is traceable to a primary government source.

```
┌──────────────────────────────────────────────────────────────┐
│              SOVEREIGN INTELLIGENCE ENGINE    (Updated)      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [1] SEC DIRECT INGESTION                                    │
│      └─ Pulls filings directly from SEC EDGAR               │
│      └─ No third-party financial data providers             │
│                                                              │
│  [2] STRUCTURED PARSING LAYER                                │
│      └─ Extracts MD&A, Risk Factors, Business sections      │
│      └─ Converts filings into structured semantic blocks    │
│                                                              │
│  [3] AI SYNTHESIS ENGINE                                     │
│      └─ LLM acts as Equity Research Analyst                 │
│      └─ Cross-period comparison (10-Q vs 10-K)             │
│      └─ Focus: operational signals, not PR language         │
│                                                              │
│  [4] INTELLIGENCE OUTPUT LAYER                               │
│      └─ Structured JSON briefs                              │
│      └─ PDF reports (investment-grade format)              │
│      └─ Dashboard + scheduled delivery (Phase 5)            │
│                                                              │
└──────────────────────────────────────────────────────────────┘


Design Principle: Deterministic Over Generative

This system prioritizes:
- Structured extraction over free-form summarization
- Source-linked claims over probabilistic generation
- Repeatable outputs over conversational variation

```

---

## 📈 Unit Economics vs. Traditional SaaS

Metric                         Traditional SaaS        This System
-----------------------------------------------------------------------
Cost per user/month           $20–$100               $0 (self-hosted)
Cost per analysis brief       Included in license    ~$0.01–$0.05 (LLM cost)
Data source                   Aggregated vendors     SEC EDGAR (free)
Latency                       Minutes–hours          ~60 seconds end-to-end
Auditability                  Black box              Fully traceable to filings
This is compute-based estimation, not SaaS pricing equivalence.

> **The ROI case:** A 10-person enterprise team replacing a $50/seat tool saves **$6,000/year**.
> At 500 companies monitored daily, traditional tools cost **$600,000/year**. This engine: **$60/year**.

---

## 🔬 Research Philosophy: First Principles Prompting

Most AI tools summarize financial filings.

This system instead structures them into analytical units and instructs the model to behave as an institutional equity analyst.

Core principles:
- Focus on changes across reporting periods, not static summaries
- Extract operational signals (capex, hiring, margins, risk evolution)
- Prioritize mandatory SEC disclosures over management narrative
- Maintain traceability back to source filing sections

---

## ✅ Build Progress

- [x] Phase 1 — SEC EDGAR collector ✅
- [x] Phase 2 — Claude AI synthesis engine ✅
- [x] Phase 3 — PDF brief generator ✅
- [x] Phase 4 — Web dashboard ✅
- [x] Phase 5 — Autonomous scheduler + Slack delivery ✅

---

## 📊 Results So Far

Company        Status
------------------------------------
MSFT           10-K / 10-Q processed
TSLA           10-K / 10-Q processed
NVDA           10-K / 10-Q processed

Outputs generated:
- Structured JSON intelligence briefs
- Section-level extraction (MD&A, Risk Factors)
- PDF reports (Phase 3)

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

Phase 1 — SEC Ingestion Layer ✅
Phase 2 — LLM Synthesis Engine ✅
Phase 3 — PDF Report Generator ✅
Phase 4 — Web Dashboard (Streamlit) ✅
Phase 5 — Scheduling + Alerts System (In progress)

Next Iterations:
- Vector database integration (RAG over filings)
- Embedding-based semantic search across companies
- Risk trend detection across quarters
- Multi-company comparative analysis engine
- Slack / email alerting for financial anomalies

### Future Vision — Agentic Orchestration
Moving from **Read-Only** to **Actionable Intelligence:**

- Trigger Zendesk / ServiceNow tickets when financial risk thresholds are breached
- Auto-flag partner portfolio companies showing deteriorating health scores
- Cross-company pattern detection — identify sector-wide risk signals before they hit the news
- Integration with CRM (Salesforce) to enrich account records with live financial intelligence

> *"The next frontier isn't better summarization — it's AI that takes action on what it reads."*

---

## 🛡️ Data Sources

SEC EDGAR → Primary filings (10-K, 10-Q)
Anthropic / OpenAI → AI synthesis layer
Google News RSS → Optional contextual enrichment (future phase)

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
