"""
Autonomous Daily Scheduler — Phase 5
======================================
What this file does:
  - Reads your watchlist.txt (list of tickers to monitor)
  - Runs the full pipeline for each company:
      Phase 1: Pulls SEC filings
      Phase 2: Generates AI brief
      Phase 3: Creates PDF report
  - Sends a formatted intelligence digest to Slack
  - Runs automatically every morning via GitHub Actions

Run manually:
  python scheduler/run_pipeline.py

Or let GitHub Actions run it automatically at 9am EST Mon-Fri.
"""

import json
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# Add project root to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from collectors.sec_collector import collect as collect_sec
from engine.synthesizer import synthesize
from outputs.pdf_generator import generate_pdf


# ── Configuration ─────────────────────────────────────────────────────────────

def load_env(filepath=".env"):
    """Read key=value pairs from .env file."""
    env = {}
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    env[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return env

ENV               = load_env()
SLACK_WEBHOOK_URL = ENV.get("SLACK_WEBHOOK_URL", "")
WATCHLIST_FILE    = Path("watchlist.txt")
BRIEFS_DIR        = Path("data/briefs")


# ── Step 1: Load watchlist ────────────────────────────────────────────────────

def load_watchlist():
    """
    Read the list of tickers to monitor from watchlist.txt.
    One ticker per line. Lines starting with # are comments.
    """
    if not WATCHLIST_FILE.exists():
        print("  No watchlist.txt found. Creating a default one...")
        WATCHLIST_FILE.write_text("MSFT\nTSLA\nNVDA\nAAPL\nAMZN\n")

    tickers = []
    for line in WATCHLIST_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            tickers.append(line.upper())

    print(f"  Watchlist: {', '.join(tickers)}")
    return tickers


# ── Step 2: Run full pipeline for one ticker ──────────────────────────────────

def run_pipeline(ticker):
    """
    Run all 3 phases for one company.
    Returns the brief data if successful, None if failed.
    """
    print(f"\n  Processing: {ticker}")
    print(f"  {'─'*40}")

    try:
        # Phase 1: Collect SEC data
        print(f"  [1/3] Collecting SEC filings...")
        collect_sec(ticker)

        # Small pause between API calls — be a good citizen
        time.sleep(2)

        # Phase 2: AI synthesis
        print(f"  [2/3] Running AI synthesis...")
        synthesize(ticker)

        # Phase 3: Generate PDF
        print(f"  [3/3] Generating PDF...")
        generate_pdf(ticker)

        # Load the generated brief
        brief_path = BRIEFS_DIR / f"{ticker}_brief.json"
        if brief_path.exists():
            with open(brief_path, encoding="utf-8") as f:
                data = json.load(f)
            return data.get("brief", data)

    except Exception as e:
        print(f"  Error processing {ticker}: {e}")
        return None


# ── Step 3: Format Slack message ──────────────────────────────────────────────

def format_slack_message(results):
    """
    Format all briefs into one clean Slack message.

    Slack uses Block Kit for rich formatting.
    Think of blocks like HTML divs — each block is a section of the message.
    """
    today = datetime.now().strftime("%A, %B %d %Y")
    successful = [(t, b) for t, b in results if b is not None]
    failed     = [t for t, b in results if b is None]

    # ── Header block ──────────────────────────────────────────────────────────
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🏛️ Sovereign Intelligence Digest — {today}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*{len(successful)} companies analyzed* | "
                    f"Source: SEC EDGAR + Claude AI | "
                    f"Cost: ~${len(successful) * 0.01:.2f}"
                )
            }
        },
        {"type": "divider"}
    ]

    # ── One block per company ─────────────────────────────────────────────────
    for ticker, brief in successful:
        company  = brief.get("company_name", ticker)
        summary  = brief.get("one_line_summary", "No summary available")
        fh       = brief.get("financial_health", {})
        score    = fh.get("score", "N/A")
        risks    = brief.get("risk_flags", [])
        points   = brief.get("talking_points", [])

        # Score emoji
        score_emoji = (
            "🟢" if "STRONG" in score.upper() else
            "🟡" if "MODERATE" in score.upper() else
            "🔴"
        )

        # Top 2 risks
        top_risks = "\n".join(
            f"  ⚠️ {r[:100]}..." if len(r) > 100 else f"  ⚠️ {r}"
            for r in risks[:2]
        )

        # Top talking point
        top_point = points[0][:150] + "..." if points and len(points[0]) > 150 else (points[0] if points else "")

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*{company}* (`{ticker}`) {score_emoji} *{score}*\n"
                    f"_{summary}_\n\n"
                    f"*Top Risks:*\n{top_risks}\n\n"
                    f"*Key Talking Point:*\n  💬 {top_point}"
                )
            }
        })
        blocks.append({"type": "divider"})

    # ── Failed tickers ────────────────────────────────────────────────────────
    if failed:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"⚠️ *Failed to process:* {', '.join(failed)}"
            }
        })

    # ── Footer ────────────────────────────────────────────────────────────────
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "_Sovereign Intelligence Engine | "
                "Built by Abhishek Sahay | "
                "github.com/abisahay90-ai/company-intelligence-engine_"
            )
        }
    })

    return {"blocks": blocks}


# ── Step 4: Send to Slack ─────────────────────────────────────────────────────

def send_to_slack(message):
    """
    POST the formatted message to your Slack channel via webhook.
    Slack webhooks are dead simple — just a POST request with JSON.
    """
    if not SLACK_WEBHOOK_URL:
        print("\n  No SLACK_WEBHOOK_URL found in .env — skipping Slack")
        print("  Add SLACK_WEBHOOK_URL to your .env file to enable Slack delivery")
        return False

    print(f"\n  Sending to Slack...")

    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 200:
            print(f"  ✅ Slack message sent successfully")
            return True
        else:
            print(f"  ❌ Slack returned status {response.status_code}: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("  ❌ Slack request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("  ❌ Could not connect to Slack. Check your internet.")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    """
    Run the full autonomous pipeline.
    Called by GitHub Actions every morning at 9am EST.
    Can also be run manually: python scheduler/run_pipeline.py
    """
    print(f"\n{'='*55}")
    print(f"  Sovereign Intelligence Engine — Phase 5")
    print(f"  Autonomous Daily Scheduler")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}\n")

    # Step 1: Load watchlist
    print("[1/4] Loading watchlist...")
    tickers = load_watchlist()

    # Step 2: Run pipeline for each ticker
    print(f"\n[2/4] Running pipeline for {len(tickers)} companies...")
    results = []

    for ticker in tickers:
        brief = run_pipeline(ticker)
        results.append((ticker, brief))
        # Pause between companies to respect API rate limits
        time.sleep(3)

    # Step 3: Format Slack message
    print(f"\n[3/4] Formatting Slack digest...")
    message = format_slack_message(results)

    # Step 4: Send to Slack
    print(f"\n[4/4] Sending to Slack...")
    send_to_slack(message)

    # Summary
    successful = sum(1 for _, b in results if b is not None)
    print(f"\n{'='*55}")
    print(f"  Done!")
    print(f"  Companies processed : {successful}/{len(tickers)}")
    print(f"  Estimated cost      : ~${successful * 0.01:.2f}")
    print(f"  Delivered to        : Slack #market-intelligence")
    print(f"{'='*55}")


if __name__ == "__main__":
    run()