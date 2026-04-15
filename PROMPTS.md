# Research Philosophy & Prompt Design

> How this engine thinks — and why it produces materially better output than paste-to-ChatGPT.

---

## The Analyst Persona

The engine instructs Claude to operate as a **Principal Equity Analyst** — not a summarizer.

The distinction matters:
- A summarizer tells you what the document says
- An analyst tells you what the document *means* and what management is *hiding*

---

## The Three Directives

### 1. Ignore PR Spin
SEC filings contain two types of content:
- **Legally required disclosures** — these are honest (executives go to prison if they lie)
- **Management commentary** — these are optimized for investor relations

The engine is prompted to weight legally required disclosures heavily and treat
management commentary with appropriate skepticism.

```
Instruction to Claude:
"Focus on what changed between reporting periods, not what management
claims changed. Numbers don't lie. Commentary does."
```

### 2. Follow the Management Bets
The real signal in a 10-K isn't the headline revenue number.
It's the capital allocation decisions buried in the footnotes:

- R&D spend as a percentage of revenue — are they investing in the future?
- CapEx direction — are they building or cutting?
- Headcount changes — where are they hiring, where are they cutting?
- Deferred revenue — is the backlog growing or shrinking?

```
Instruction to Claude:
"Identify where management is placing long-term capital bets.
These are more predictive of future performance than current revenue."
```

### 3. Surface the Buried Risk
The SEC requires companies to disclose all material risks.
Companies comply — but bury the real risks in 50 pages of boilerplate.

The engine is instructed to extract *specific, named risks* with
actual business impact — not generic category labels.

```
Instruction to Claude:
"Extract risks that are specific to this company's situation.
Reject generic statements like 'we face competition.'
Extract specific statements like 'our top 3 customers represent
40% of revenue and have no long-term contracts.'"
```

---

## Why This Produces Better Output

| Approach | Prompt | Output Quality |
|----------|--------|----------------|
| Paste to ChatGPT | "Summarize this" | Generic, PR-friendly |
| Basic RAG | "Answer questions about this doc" | Accurate but shallow |
| This engine | Principal Analyst + 3 directives | Specific, contrarian, actionable |

---

## Structured Output Design

The engine forces Claude to return structured JSON — not free-form prose.

This means:
- Output is always parseable by downstream systems
- Every field is validated before display
- The dashboard and PDF are generated from the same data source
- Future agents can read and act on the output programmatically

---

## Future Prompt Evolution

- **Cross-document reasoning** — compare Q3 10-Q to annual 10-K to catch mid-year shifts
- **Peer benchmarking** — prompt Claude with two companies simultaneously for relative analysis
- **Temporal tracking** — compare this quarter's brief to last quarter's to detect drift