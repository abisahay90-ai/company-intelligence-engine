"""
SEC EDGAR Collector
====================
What this file does:
  - You give it a company ticker symbol (like AAPL for Apple)
  - It finds that company in the SEC database
  - It downloads their latest financial filings (10-K and 10-Q)
  - It saves everything as a JSON file for our AI engine to read later

A 10-K = a company's full yearly financial report (required by law)
A 10-Q = a company's quarterly update (every 3 months)
Both are public documents — free for anyone to read on SEC EDGAR
"""

import json        # Built into Python — saves data as JSON files
import time        # Built into Python — lets us pause between requests
import argparse    # Built into Python — lets us pass options from command line
import requests    # We installed this — lets Python talk to websites
from pathlib import Path      # Built into Python — handles file/folder paths
from datetime import datetime # Built into Python — gets current date/time
import re                     # Built into Python — cleans up text

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────

USER_AGENT = "CompanyIntelligenceEngine abhishek@youremail.com"
OUTPUT_DIR = Path("data/sec_filings")

# ─────────────────────────────────────────────────────────────
# STEP 1 — Convert ticker symbol to SEC's internal ID (CIK)
# ─────────────────────────────────────────────────────────────

def ticker_to_cik(ticker):
    """
    Look up a company's CIK number using their stock ticker.
    CIK = Central Index Key — SEC's unique ID for every public company.
    Example: Apple's ticker is AAPL but their SEC ID is 0000320193
    """
    print(f"\n  [1/4] Looking up CIK number for: {ticker.upper()}")

    url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

    companies = response.json()

    for _, company in companies.items():
        if company["ticker"].upper() == ticker.upper():
            cik = str(company["cik_str"]).zfill(10)
            print(f"  Found: {company['title']} | CIK: {cik}")
            return cik, company["title"]

    raise ValueError(f"Ticker '{ticker}' not found. Must be a US public company.")


# ─────────────────────────────────────────────────────────────
# STEP 2 — Pull the company's full filing history from SEC
# ─────────────────────────────────────────────────────────────

def get_filing_history(cik):
    """
    Pull every filing this company has ever made with the SEC.
    Think of this like requesting someone's complete document history.
    """
    print(f"  [2/4] Pulling filing history from SEC EDGAR...")

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

    data = response.json()
    total = len(data.get("filings", {}).get("recent", {}).get("form", []))
    print(f"  Found {total} total filings on record")

    return data


# ─────────────────────────────────────────────────────────────
# STEP 3 — Filter for only the filing types we want
# ─────────────────────────────────────────────────────────────

def filter_filings(filing_history, filing_types, max_count):
    """
    From hundreds of SEC filings, pull out only 10-K and 10-Q forms.
    
    The SEC stores this data like a spreadsheet with parallel columns:
    forms[0] and dates[0] and accessions[0] = same filing
    forms[1] and dates[1] and accessions[1] = next filing
    """
    print(f"  [3/4] Filtering for: {', '.join(filing_types)}")

    recent      = filing_history.get("filings", {}).get("recent", {})
    forms       = recent.get("form", [])
    dates       = recent.get("filingDate", [])
    accessions  = recent.get("accessionNumber", [])
    primary_doc = recent.get("primaryDocument", [])

    results = []

    for i, form in enumerate(forms):
        if form in filing_types and len(results) < max_count:
            results.append({
                "form":        form,
                "date":        dates[i],
                "accession":   accessions[i],
                "primary_doc": primary_doc[i],
            })
            print(f"    Found: {form} filed on {dates[i]}")

    print(f"  Keeping {len(results)} filings")
    return results


# ─────────────────────────────────────────────────────────────
# STEP 4 — Download and clean the actual filing text
# ─────────────────────────────────────────────────────────────

def download_filing(cik, filing):
    """
    Download one filing's actual text content from SEC servers.
    SEC filings are stored as HTML pages — we grab the raw content.
    """
    accession_clean = filing["accession"].replace("-", "")
    cik_short = cik.lstrip("0")

    url = (
        f"https://www.sec.gov/Archives/edgar/data/"
        f"{cik_short}/{accession_clean}/{filing['primary_doc']}"
    )

    print(f"    Downloading {filing['form']} from {filing['date']}...")

    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    time.sleep(0.2)  # Be polite — don't hammer SEC servers

    if response.status_code != 200:
        print(f"    Could not download (error {response.status_code}) — skipping")
        return ""

    return response.text


def clean_text(raw_html, max_chars=50000):
    """
    Strip HTML tags so we get readable text.
    Also truncate — 10-K filings can be 500 pages, we only need ~50k chars.
    """
    clean = re.sub(r'<[^>]+>', ' ', raw_html)  # Remove HTML tags
    clean = re.sub(r'\s+', ' ', clean).strip() # Collapse whitespace

    if len(clean) > max_chars:
        clean = clean[:max_chars] + "\n\n[Truncated]"

    return clean


# ─────────────────────────────────────────────────────────────
# STEP 5 — Save everything to a JSON file
# ─────────────────────────────────────────────────────────────

def save_to_json(ticker, company_name, filings_data):
    """
    Save all collected data into one JSON file.
    JSON = structured text file both humans and computers can read.
    This is what we feed into the AI engine in Phase 2.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output = {
        "ticker":       ticker.upper(),
        "company_name": company_name,
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "source":       "SEC EDGAR (free public API)",
        "filing_count": len(filings_data),
        "filings":      filings_data
    }

    filepath = OUTPUT_DIR / f"{ticker.upper()}_sec_filings.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Saved to: {filepath}")
    return filepath


# ─────────────────────────────────────────────────────────────
# MAIN — ties all 5 steps together
# ─────────────────────────────────────────────────────────────

def collect(ticker, filing_types=None, max_count=4):
    if filing_types is None:
        filing_types = ["10-K", "10-Q"]

    print(f"\n{'='*50}")
    print(f"  SEC EDGAR Collector — Phase 1")
    print(f"  Ticker: {ticker.upper()} | Forms: {', '.join(filing_types)}")
    print(f"{'='*50}")

    cik, company_name = ticker_to_cik(ticker)
    history           = get_filing_history(cik)
    filings_meta      = filter_filings(history, filing_types, max_count)

    if not filings_meta:
        print("\n  No filings found. Try a different ticker.")
        return

    print(f"\n  [4/4] Downloading filing content...")
    filings_data = []

    for filing in filings_meta:
        raw_text = download_filing(cik, filing)
        clean    = clean_text(raw_text)
        filings_data.append({
            "form":       filing["form"],
            "date":       filing["date"],
            "accession":  filing["accession"],
            "characters": len(clean),
            "content":    clean
        })

    output_path  = save_to_json(ticker, company_name, filings_data)
    total_chars  = sum(f["characters"] for f in filings_data)

    print(f"\n  Done!")
    print(f"  Company : {company_name}")
    print(f"  Filings : {len(filings_data)} downloaded")
    print(f"  Text    : {total_chars:,} characters collected")
    print(f"  File    : {output_path}")
    print(f"\n  Ready for Phase 2 — AI Synthesis Engine")


# ─────────────────────────────────────────────────────────────
# Run when you type: python collectors/sec_collector.py --ticker AAPL
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pull SEC financial filings for any public US company"
    )
    parser.add_argument("--ticker", required=True,
        help="Stock ticker e.g. AAPL, MSFT, NVDA")
    parser.add_argument("--forms", nargs="+", default=["10-K", "10-Q"],
        help="Filing types (default: 10-K 10-Q)")
    parser.add_argument("--max", type=int, default=4,
        help="Max filings to download (default: 4)")

    args = parser.parse_args()
    collect(args.ticker, args.forms, args.max)