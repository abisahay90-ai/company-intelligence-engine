"""
SEC EDGAR Collector (LLM-Ready + Safe Mode)
===========================================
What this file does:
  - Takes a company ticker (e.g. AAPL)
  - Maps it to SEC CIK
  - Downloads latest 10-K / 10-Q filings
  - Extracts key sections (MD&A, Risk Factors, Business)
  - Cleans + chunks text for LLM ingestion
  - Saves structured JSON output

Why this version is better:
  - SEC-safe rate limiting
  - Retry + backoff handling
  - LLM-ready structured chunks
  - Section-aware extraction (not just raw text)
"""

import json
import time
import argparse
import requests
import re
from pathlib import Path
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ─────────────────────────────────────────────
# CONFIG (SEC SAFE MODE)
# ─────────────────────────────────────────────

USER_AGENT = "CompanyIntelligenceEngine/1.0 (your-email@example.com)"
BASE_DIR   = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "data/sec_filings"

RATE_LIMIT_SECONDS = 0.25   # SEC-safe pacing
MAX_RETRIES = 5

# ─────────────────────────────────────────────
# SESSION WITH RETRY + BACKOFF
# ─────────────────────────────────────────────

def get_session():
    session = requests.Session()

    retry = Retry(
        total=MAX_RETRIES,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": USER_AGENT})

    return session


session = get_session()

# ─────────────────────────────────────────────
# STEP 1 — Ticker → CIK
# ─────────────────────────────────────────────

def ticker_to_cik(ticker):
    print(f"\n[1/4] Looking up CIK for {ticker.upper()}")

    url = "https://www.sec.gov/files/company_tickers.json"
    r = session.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    for _, company in data.items():
        if company["ticker"].upper() == ticker.upper():
            cik = str(company["cik_str"]).zfill(10)
            print(f"Found {company['title']} | CIK {cik}")
            return cik, company["title"]

    raise ValueError("Ticker not found")


# ─────────────────────────────────────────────
# STEP 2 — Filing History
# ─────────────────────────────────────────────

def get_filing_history(cik):
    print(f"[2/4] Fetching filing history...")

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    r = session.get(url, timeout=10)
    r.raise_for_status()

    time.sleep(RATE_LIMIT_SECONDS)
    return r.json()


# ─────────────────────────────────────────────
# STEP 3 — Filter filings
# ─────────────────────────────────────────────

def filter_filings(history, types, max_count):
    print(f"[3/4] Filtering filings: {types}")

    recent = history.get("filings", {}).get("recent", {})

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accs  = recent.get("accessionNumber", [])
    docs  = recent.get("primaryDocument", [])

    results = []

    for i, form in enumerate(forms):
        if form in types and len(results) < max_count:
            results.append({
                "form": form,
                "date": dates[i],
                "accession": accs[i],
                "primary_doc": docs[i],
            })

    print(f"Selected {len(results)} filings")
    return results


# ─────────────────────────────────────────────
# STEP 4 — Download Filing (SAFE + RETRY)
# ─────────────────────────────────────────────

def download_filing(cik, filing):
    acc = filing["accession"].replace("-", "")
    cik_short = cik.lstrip("0")
    doc = filing["primary_doc"]

    url = f"https://www.sec.gov/Archives/edgar/data/{cik_short}/{acc}/{doc}"

    try:
        r = session.get(url, timeout=10)
        time.sleep(RATE_LIMIT_SECONDS)

        if r.status_code == 200:
            return r.text
    except Exception as e:
        print("Primary fetch failed:", e)

    return ""


# ─────────────────────────────────────────────
# STEP 5 — SECTION EXTRACTION (KEY U.S. FILING SECTIONS)
# ─────────────────────────────────────────────

def extract_sections(text):
    """
    Extract high-value SEC filing sections for LLMs
    """

    sections = {
        "MD&A": "",
        "RISK_FACTORS": "",
        "BUSINESS": ""
    }

    patterns = {
        "MD&A": r"item\s+7\.*\s*management.*?discussion.*?analysis(.*?)(item\s+8|item\s+7a)",
        "RISK_FACTORS": r"item\s+1a\.*\s*risk\s*factors(.*?)(item\s+1b|item\s+2)",
        "BUSINESS": r"item\s+1\.*\s*business(.*?)(item\s+1a|item\s+2)"
    }

    text_lower = text.lower()

    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower, re.DOTALL)
        if match:
            sections[key] = clean_text(match.group(1))

    return sections


# ─────────────────────────────────────────────
# STEP 6 — CLEAN TEXT
# ─────────────────────────────────────────────

def clean_text(raw):
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw


# ─────────────────────────────────────────────
# STEP 7 — LLM CHUNKING
# ─────────────────────────────────────────────

def chunk_text(text, chunk_size=2000):
    """
    Split into LLM-friendly chunks
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks


# ─────────────────────────────────────────────
# STEP 8 — SAVE OUTPUT
# ─────────────────────────────────────────────

def save(ticker, company, data):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path = OUTPUT_DIR / f"{ticker.upper()}_sec.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "ticker": ticker,
            "company": company,
            "collected_at": datetime.utcnow().isoformat(),
            "filings": data
        }, f, indent=2)

    print(f"\nSaved → {path}")
    return path


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

def collect(ticker, forms=["10-K", "10-Q"], max_count=3):

    print("\n==============================")
    print("SEC EDGAR Collector (LLM Ready)")
    print("==============================")

    cik, company = ticker_to_cik(ticker)
    history = get_filing_history(cik)
    filings = filter_filings(history, forms, max_count)

    results = []

    for filing in filings:
        raw = download_filing(cik, filing)
        if not raw:
            continue

        sections = extract_sections(raw)

        combined = {
            "meta": filing,
            "sections": sections,
            "chunks": {
                k: chunk_text(v)
                for k, v in sections.items()
                if v
            }
        }

        results.append(combined)

    save(ticker, company, results)

    print("\nDone. Ready for LLM ingestion 🚀")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--max", type=int, default=3)

    args = parser.parse_args()
    collect(args.ticker, max_count=args.max)