"""
AI Synthesis Engine — Phase 2
===============================
What this file does:
  - Reads the SEC filing JSON files collected in Phase 1
  - Sends the financial data to Claude AI
  - Gets back a structured intelligence brief
  - Saves the brief as a clean JSON file

Think of this as the "brain" of the engine.
Phase 1 collected the raw ingredients.
Phase 2 turns them into a meal.

Run it:
  python engine/synthesizer.py --ticker MSFT
  python engine/synthesizer.py --ticker TSLA
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timezone


import anthropic

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

ENV            = load_env()
API_KEY        = ENV.get("ANTHROPIC_API_KEY", "")
INPUT_DIR      = Path("data/sec_filings")
OUTPUT_DIR     = Path("data/briefs")
MODEL          = "claude-opus-4-6"


# ── Step 1: Load SEC filing data ──────────────────────────────────────────────

def load_filing_data(ticker):
    """
    Load the JSON file we created in Phase 1.
    This is the raw SEC data we're going to feed to Claude.
    """
    filepath = INPUT_DIR / f"{ticker.upper()}_sec_filings.json"

    if not filepath.exists():
        raise FileNotFoundError(
            f"No data found for {ticker.upper()}. "
            f"Run Phase 1 first: python collectors/sec_collector.py --ticker {ticker}"
        )

    print(f"  Loading: {filepath}")
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    print(f"  Found {data['filing_count']} filings for {data['company_name']}")
    return data


# ── Step 2: Prepare the prompt ────────────────────────────────────────────────

def build_prompt(filing_data):
    """
    Build the prompt we send to Claude.

    This is the most important part of Phase 2.
    The quality of the prompt directly determines the quality of the output.

    We're telling Claude:
    - Who it is (a senior financial analyst)
    - What data it has (SEC filings)
    - Exactly what to output (structured sections)
    - What format to use (JSON so we can parse it)
    """
    company   = filing_data["company_name"]
    ticker    = filing_data["ticker"]

    # Combine all filing content into one block of text
    # We take the first 40,000 characters to stay within Claude's context window
    all_content = ""
    for filing in filing_data["filings"]:
        all_content += f"\n\n--- {filing['form']} filed {filing['date']} ---\n"
        all_content += filing["content"][:10000]  # 10k chars per filing

    all_content = all_content[:40000]  # Hard cap for safety

    prompt = f"""You are a senior financial analyst and enterprise intelligence expert.

You have been given SEC filings for {company} (ticker: {ticker}).
Your job is to analyze this data and produce a structured intelligence brief
that a busy executive or job candidate could read in 2 minutes.

Here is the SEC filing data:

{all_content}

Based on this data, produce a JSON response with EXACTLY this structure.
Return ONLY the JSON — no extra text, no markdown, no explanation:

{{
  "company_name": "{company}",
  "ticker": "{ticker}",
  "analysis_date": "today's date",
  "financial_health": {{
    "summary": "2-3 sentence summary of overall financial health",
    "revenue_trend": "one sentence on revenue direction",
    "profitability": "one sentence on margins and profit",
    "cash_position": "one sentence on cash and debt situation",
    "score": "Strong / Moderate / Weak"
  }},
  "risk_flags": [
    "Risk 1 — specific risk extracted from the filing",
    "Risk 2 — specific risk extracted from the filing",
    "Risk 3 — specific risk extracted from the filing",
    "Risk 4 — specific risk extracted from the filing",
    "Risk 5 — specific risk extracted from the filing"
  ],
  "strategic_moves": [
    "Strategic initiative 1 management is focused on",
    "Strategic initiative 2 management is focused on",
    "Strategic initiative 3 management is focused on"
  ],
  "talking_points": [
    "Ready-to-use talking point 1 for an interview or sales meeting",
    "Ready-to-use talking point 2 for an interview or sales meeting",
    "Ready-to-use talking point 3 for an interview or sales meeting"
  ],
  "one_line_summary": "One sentence that captures the company's current situation"
}}"""

    return prompt


# ── Step 3: Call Claude AI ────────────────────────────────────────────────────

def call_claude(prompt):
    """
    Send the prompt to Claude and get back the intelligence brief.

    anthropic.Anthropic() = creates a connection to Claude API
    client.messages.create() = sends one message and gets one response
    max_tokens = maximum length of Claude's response (1000 is plenty for JSON)
    """
    if not API_KEY:
        raise ValueError(
            "No Anthropic API key found. "
            "Add ANTHROPIC_API_KEY=your-key to your .env file."
        )

    print(f"  Connecting to Claude AI...")
    client = anthropic.Anthropic(api_key=API_KEY)

    print(f"  Sending {len(prompt):,} characters to Claude...")
    print(f"  Waiting for response...")

    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = message.content[0].text
        print(f"  Response received — {len(response_text):,} characters")
        return response_text

    except anthropic.AuthenticationError:
        raise ValueError("Invalid API key. Check your ANTHROPIC_API_KEY in .env")
    except anthropic.RateLimitError:
        raise RuntimeError("Rate limit hit. Wait 60 seconds and try again.")
    except anthropic.APIConnectionError:
        raise RuntimeError("Could not connect to Claude API. Check your internet.")


# ── Step 4: Parse Claude's response ──────────────────────────────────────────

def parse_response(response_text):
    """
    Claude should return clean JSON.
    But sometimes it adds extra text around it — this handles that.
    """
    # Try to parse directly first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # If that fails, try to find JSON block inside the response
    import re
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # If all else fails, return the raw text wrapped in a dict
    print("  Warning: Could not parse JSON — saving raw response")
    return {"raw_response": response_text}


# ── Step 5: Save the brief ────────────────────────────────────────────────────

def save_brief(ticker, brief_data):
    """
    Save the intelligence brief to a JSON file.
    Phase 3 will read this to generate the PDF report.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_used":   MODEL,
        "brief":        brief_data
    }

    filepath = OUTPUT_DIR / f"{ticker.upper()}_brief.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Saved to: {filepath}")
    return filepath


# ── Step 6: Print the brief to screen ────────────────────────────────────────

def print_brief(brief_data):
    """
    Display the intelligence brief in a readable format in the terminal.
    This is the moment where raw SEC data becomes actionable intelligence.
    """
    b = brief_data if "company_name" in brief_data else brief_data.get("brief", brief_data)

    print("\n")
    print("=" * 60)
    print(f"  INTELLIGENCE BRIEF")
    print(f"  {b.get('company_name', 'Unknown')} ({b.get('ticker', '?')})")
    print("=" * 60)

    print(f"\n  ONE LINE SUMMARY")
    print(f"  {b.get('one_line_summary', 'N/A')}")

    fh = b.get("financial_health", {})
    print(f"\n  FINANCIAL HEALTH  [{fh.get('score', 'N/A')}]")
    print(f"  {fh.get('summary', 'N/A')}")
    print(f"  Revenue    : {fh.get('revenue_trend', 'N/A')}")
    print(f"  Margins    : {fh.get('profitability', 'N/A')}")
    print(f"  Cash       : {fh.get('cash_position', 'N/A')}")

    print(f"\n  RISK FLAGS")
    for i, risk in enumerate(b.get("risk_flags", []), 1):
        print(f"  {i}. {risk}")

    print(f"\n  STRATEGIC MOVES")
    for i, move in enumerate(b.get("strategic_moves", []), 1):
        print(f"  {i}. {move}")

    print(f"\n  TALKING POINTS  (use these in your next meeting)")
    for i, point in enumerate(b.get("talking_points", []), 1):
        print(f"  {i}. {point}")

    print("\n" + "=" * 60)


# ── Main ──────────────────────────────────────────────────────────────────────

def synthesize(ticker):
    """
    Run the full AI synthesis pipeline for one company.
    Reads Phase 1 output → sends to Claude → saves structured brief.
    """
    print(f"\n{'='*50}")
    print(f"  AI Synthesis Engine — Phase 2")
    print(f"  Ticker : {ticker.upper()}")
    print(f"  Model  : {MODEL}")
    print(f"{'='*50}\n")

    try:
        # Step 1: Load the SEC data from Phase 1
        print("[1/5] Loading SEC filing data...")
        filing_data = load_filing_data(ticker)

        # Step 2: Build the prompt
        print("\n[2/5] Building analysis prompt...")
        prompt = build_prompt(filing_data)
        print(f"  Prompt length: {len(prompt):,} characters")

        # Step 3: Call Claude
        print("\n[3/5] Calling Claude AI...")
        response_text = call_claude(prompt)

        # Step 4: Parse the response
        print("\n[4/5] Parsing response...")
        brief_data = parse_response(response_text)

        # Step 5: Save the brief
        print("\n[5/5] Saving intelligence brief...")
        output_path = save_brief(ticker, brief_data)

        # Print to screen
        print_brief(brief_data)

        print(f"\n  Brief saved to: {output_path}")
        print(f"  Ready for Phase 3 — PDF Generator")
        return output_path

    except FileNotFoundError as e:
        print(f"\n  Error: {e}")
    except (ValueError, RuntimeError) as e:
        print(f"\n  Error: {e}")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate AI intelligence brief from SEC filing data"
    )
    parser.add_argument(
        "--ticker",
        required=True,
        help="Stock ticker e.g. MSFT, TSLA, AAPL"
    )
    args = parser.parse_args()
    synthesize(args.ticker)