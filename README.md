# 🏛️ Sovereign Intelligence Engine

> **An Open-Source Agentic Framework for High-Fidelity Financial Analysis.**
> Moving from 'Generative Fluff' to 'Deterministic Ground Truth' — for $0.01 per brief.


## 👤 Author

**Abhishek Sahay** — Senior Product Leader | AI/ML & LLM Copilots  
[LinkedIn](https://www.linkedin.com/in/abhisheksahay/) | [GitHub](https://github.com/abisahay90-ai)

> *"The next frontier isn't better summarization — it's AI that takes action on what it reads."Here is your updated `README.md`. I have integrated the **Intelligence Eval Engine (Phase 5.5)**, added the **"Audit-First"** philosophy, and included the new directory structure for the evaluator.

---

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data Source](https://img.shields.io/badge/Data-SEC%20EDGAR-orange)](https://edgar.sec.gov)
[![AI](https://img.shields.io/badge/AI-Claude%20Sonnet-purple)](https://anthropic.com)

---

## 🎯 The Problem This Solves

Enterprise teams spend 3–5 hours manually researching a single public company before earnings calls or investment decisions. Existing SaaS tools often provide generic summaries that still require manual validation.

This system removes manual synthesis by directly converting SEC filings into **structured, decision-ready intelligence briefs** with a built-in "Auditor" to prevent hallucinations.

---

## 🧠 System Architecture: The "Sovereign" Approach

Unlike generic RAG tools, this engine runs a **Multi-Stage Synthesis Pipeline** designed to ensure every claim is traceable to a primary government source.

┌──────────────────────────────────────────────────────────────┐
│              SOVEREIGN INTELLIGENCE ENGINE                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [1] SEC DIRECT INGESTION (sec_collector.py)                 │
│      └─ Pulls raw filings directly from SEC EDGAR            │
│                                                              │
│  [2] STRUCTURED PARSING LAYER                                │
│      └─ Extracts MD&A and Risk Factors into semantic blocks  │
│                                                              │
│  [3] AI SYNTHESIS & EVALUATION (evaluator.py)                │
│      └─ Creator: Claude generates the synthesis              │
│      └─ Judge: Cross-model audit for Hallucinations          │
│                                                              │
│  [4] AGENTIC HANDSHAKE                                       │
│      └─ Score > 0.9: Automated Slack Delivery                │
│      └─ Score < 0.9: Flagged for Human Review                │
│                                                              │
└──────────────────────────────────────────────────────────────┘

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

## 🛡️ The "Plumbing of Trust" (Intelligence Evals)

Before allowing the system to act (Phase 6), we implemented a deterministic verification layer.

*   **Hallucination Check:** Binary pass/fail against "Golden Datasets".
*   **Traceability Scoring:** Every claim must include a clickable SEC EDGAR URL; otherwise, it receives a score of 0.
*   **The Kill Switch:** If the trust score falls below 90%, the agent halts and requests human intervention.

---

## ✅ Build Progress

- [x] Phase 1 — SEC EDGAR collector ✅
- [x] Phase 2 — Claude AI synthesis engine ✅
- [x] Phase 3 — PDF brief generator ✅
- [x] Phase 4 — Web dashboard ✅
- [x] Phase 5 — Autonomous scheduler + Slack delivery ✅
- [x] **Phase 5.5 — Intelligence Eval Engine (The Auditor) ✅**



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
├── collectors/     ← Phase 1: SEC EDGAR ingestion
├── engine/         ← Phase 2: Claude AI orchestration
├── evals/          ← Phase 5.5: The Auditor (Golden Datasets & Evaluator)
├── outputs/        ← Phase 3 & 4: PDF artifacts & Streamlit Dashboard
├── .env            ← API keys (gitignored)
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
