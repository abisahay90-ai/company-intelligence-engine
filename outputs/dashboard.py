"""
Web Dashboard — Phase 4
========================
What this file does:
  - Gives you a beautiful web interface for the engine
  - Type any ticker → runs all 3 phases automatically
  - Shows the intelligence brief on screen
  - Lets you download the PDF report
  - No command line needed — anyone on your team can use it

Run it:
  streamlit run outputs/dashboard.py
"""

import json
import sys
import time
from pathlib import Path

import streamlit as st

# Add project root to path so we can import our own modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from collectors.sec_collector import collect as collect_sec
from engine.synthesizer import synthesize
from outputs.pdf_generator import generate_pdf

# ── Page Configuration ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Company Intelligence Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0A1628;
        color: #E8EDF2;
    }

    /* Hide Streamlit default menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Title styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .main-subtitle {
        font-size: 1.1rem;
        color: #8899AA;
        margin-top: 8px;
        margin-bottom: 32px;
    }

    /* Search box */
    .stTextInput input {
        background-color: #132238;
        border: 1.5px solid #1B4F8A;
        border-radius: 8px;
        color: #FFFFFF;
        font-size: 1.1rem;
        padding: 12px 16px;
    }
    .stTextInput input:focus {
        border-color: #2E86C1;
        box-shadow: 0 0 0 2px rgba(46,134,193,0.2);
    }

    /* Buttons */
    .stButton button {
        background-color: #1B4F8A;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton button:hover {
        background-color: #2E86C1;
    }

    /* Metric cards */
    .metric-card {
        background: #132238;
        border: 1px solid #1B4F8A;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #2E86C1;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 1rem;
        color: #E8EDF2;
        line-height: 1.5;
    }

    /* Score badge */
    .score-strong {
        background: #1E4D2B;
        color: #2ECC71;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .score-moderate {
        background: #4D3B1A;
        color: #F39C12;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .score-weak {
        background: #4D1A1A;
        color: #E74C3C;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    /* Section headers */
    .section-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #2E86C1;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        margin-top: 24px;
        padding-bottom: 8px;
        border-bottom: 1px solid #1B4F8A;
    }

    /* Risk items */
    .risk-item {
        background: #1A1A2E;
        border-left: 3px solid #E67E22;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 8px;
        color: #E8EDF2;
        font-size: 0.9rem;
    }

    /* Strategy items */
    .strategy-item {
        background: #132238;
        border-left: 3px solid #2E86C1;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 8px;
        color: #E8EDF2;
        font-size: 0.9rem;
    }

    /* Talking points */
    .talking-item {
        background: #1A2A1A;
        border-left: 3px solid #27AE60;
        padding: 12px 14px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 10px;
        color: #E8EDF2;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Progress steps */
    .step-active {
        color: #2E86C1;
        font-weight: 600;
    }
    .step-done {
        color: #27AE60;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border-color: #1B4F8A;
        opacity: 0.4;
    }
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ──────────────────────────────────────────────────────────

def load_existing_brief(ticker):
    """Check if we already have a brief for this ticker."""
    filepath = Path("data/briefs") / f"{ticker.upper()}_brief.json"
    if filepath.exists():
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("brief", data)
    return None


def get_score_html(score):
    """Return colored HTML badge for financial health score."""
    score_upper = score.upper() if score else ""
    if "STRONG" in score_upper:
        return f'<span class="score-strong">● {score}</span>'
    elif "MODERATE" in score_upper:
        return f'<span class="score-moderate">● {score}</span>'
    else:
        return f'<span class="score-weak">● {score}</span>'


def display_brief(brief):
    """Render the full intelligence brief on screen."""

    # ── One Line Summary ──────────────────────────────────────────────────────
    summary = brief.get("one_line_summary", "")
    if summary:
        st.markdown(f"""
        <div class="metric-card" style="border-color: #2E86C1; margin-top: 24px;">
            <div class="metric-label">Executive Summary</div>
            <div class="metric-value" style="font-style: italic; font-size: 1.05rem;">
                "{summary}"
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Financial Health ──────────────────────────────────────────────────────
    fh    = brief.get("financial_health", {})
    score = fh.get("score", "N/A")

    st.markdown('<div class="section-header">📊 Financial Health</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Score</div>
            <div>{get_score_html(score)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Revenue Trend</div>
            <div class="metric-value">{fh.get('revenue_trend', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Cash Position</div>
            <div class="metric-value">{fh.get('cash_position', 'N/A')[:120]}...</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Financial Summary</div>
        <div class="metric-value">{fh.get('summary', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two Column Layout ─────────────────────────────────────────────────────
    left_col, right_col = st.columns(2)

    with left_col:
        # Risk Flags
        st.markdown('<div class="section-header">⚠️ Risk Flags</div>',
                    unsafe_allow_html=True)
        for i, risk in enumerate(brief.get("risk_flags", []), 1):
            st.markdown(
                f'<div class="risk-item"><b>{i}.</b> {risk}</div>',
                unsafe_allow_html=True
            )

    with right_col:
        # Strategic Moves
        st.markdown('<div class="section-header">🎯 Strategic Moves</div>',
                    unsafe_allow_html=True)
        for i, move in enumerate(brief.get("strategic_moves", []), 1):
            st.markdown(
                f'<div class="strategy-item"><b>{i}.</b> {move}</div>',
                unsafe_allow_html=True
            )

    # ── Talking Points ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">💬 Talking Points</div>',
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#8899AA; font-size:0.85rem; margin-bottom:12px;'>"
        "Use these in your next interview, sales call, or board meeting</p>",
        unsafe_allow_html=True
    )
    for i, point in enumerate(brief.get("talking_points", []), 1):
        st.markdown(
            f'<div class="talking-item"><b>{i}.</b> {point}</div>',
            unsafe_allow_html=True
        )


# ── Main App ──────────────────────────────────────────────────────────────────

def main():

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 32px 0 16px 0;">
        <div class="main-title">Company Intelligence Engine</div>
        <div class="main-subtitle">
            Type any US public company ticker → get a boardroom-ready brief in 60 seconds
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Search Bar ────────────────────────────────────────────────────────────
    col_input, col_button = st.columns([3, 1])

    with col_input:
        ticker = st.text_input(
            label="Company Ticker",
            placeholder="e.g. AAPL, MSFT, NVDA, TSLA, AMZN",
            label_visibility="collapsed"
        ).strip().upper()

    with col_button:
        run_button = st.button("🔍 Generate Brief")

    # ── Examples ──────────────────────────────────────────────────────────────
    st.markdown(
        "<p style='color:#8899AA; font-size:0.8rem;'>"
        "Try: AAPL &nbsp;·&nbsp; MSFT &nbsp;·&nbsp; NVDA &nbsp;·&nbsp; "
        "TSLA &nbsp;·&nbsp; AMZN &nbsp;·&nbsp; GOOGL &nbsp;·&nbsp; META</p>",
        unsafe_allow_html=True
    )

    # ── Run Pipeline ──────────────────────────────────────────────────────────
    if run_button and ticker:

        st.markdown("---")

        # Check if we already have a cached brief
        existing = load_existing_brief(ticker)

        if existing:
            st.success(f"✅ Loaded cached brief for **{ticker}**")
            company_name = existing.get("company_name", ticker)
            st.markdown(f"""
            <div style="margin-bottom: 8px;">
                <span style="font-size:1.8rem; font-weight:800;
                color:#FFFFFF;">{company_name}</span>
                <span style="font-size:1rem; color:#2E86C1;
                margin-left:12px;">{ticker}</span>
            </div>
            """, unsafe_allow_html=True)
            display_brief(existing)

        else:
            # Run full pipeline
            progress = st.empty()
            status   = st.empty()

            # Step 1: Collect SEC data
            progress.markdown(
                '<p class="step-active">⏳ Step 1/3 — Collecting SEC filings...</p>',
                unsafe_allow_html=True
            )
            status.info("Connecting to SEC EDGAR. This takes 20-30 seconds...")

            try:
                collect_sec(ticker)
                progress.markdown(
                    '<p class="step-done">✅ Step 1/3 — SEC filings collected</p>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Could not collect SEC data: {e}")
                st.stop()

            # Step 2: AI Synthesis
            progress.markdown(
                '<p class="step-active">⏳ Step 2/3 — Running AI analysis...</p>',
                unsafe_allow_html=True
            )
            status.info("Claude AI is reading the filings and generating your brief...")

            try:
                synthesize(ticker)
                progress.markdown(
                    '<p class="step-done">✅ Step 2/3 — AI brief generated</p>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"AI synthesis failed: {e}")
                st.stop()

            # Step 3: Generate PDF
            progress.markdown(
                '<p class="step-active">⏳ Step 3/3 — Generating PDF report...</p>',
                unsafe_allow_html=True
            )
            status.info("Building your PDF report...")

            try:
                generate_pdf(ticker)
                progress.markdown(
                    '<p class="step-done">✅ Step 3/3 — PDF report created</p>',
                    unsafe_allow_html=True
                )
                status.empty()
            except Exception as e:
                st.warning(f"PDF generation had an issue: {e}")

            # Load and display the brief
            brief = load_existing_brief(ticker)
            if brief:
                st.success(f"✅ Intelligence brief ready for **{ticker}**")
                company_name = brief.get("company_name", ticker)
                st.markdown(f"""
                <div style="margin-bottom: 8px;">
                    <span style="font-size:1.8rem; font-weight:800;
                    color:#FFFFFF;">{company_name}</span>
                    <span style="font-size:1rem; color:#2E86C1;
                    margin-left:12px;">{ticker}</span>
                </div>
                """, unsafe_allow_html=True)
                display_brief(brief)
            else:
                st.error("Brief was generated but could not be loaded.")

        # ── PDF Download Button ───────────────────────────────────────────────
        pdf_path = Path("outputs/pdfs") / f"{ticker}_Intelligence_Brief.pdf"
        if pdf_path.exists():
            st.markdown("---")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=f,
                    file_name=f"{ticker}_Intelligence_Brief.pdf",
                    mime="application/pdf"
                )

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#8899AA; font-size:0.75rem; padding:16px 0;">
        Company Intelligence Engine &nbsp;·&nbsp;
        Built by Abhishek Sahay &nbsp;·&nbsp;
        Source: SEC EDGAR + Claude AI &nbsp;·&nbsp;
        For informational purposes only
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
