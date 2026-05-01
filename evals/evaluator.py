import json
import re
from pathlib import Path

SEC_URL_PATTERN = r"https:\/\/www\.sec\.gov\/edgar\/browse\/\?CIK=\d+"

def load_dataset():
    path = Path(__file__).parent / "golden_dataset.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# TRACEABILITY CHECK (NEW)
# ----------------------------
def has_valid_sec_url(text: str) -> bool:
    if not text:
        return False
    return re.search(SEC_URL_PATTERN, text) is not None

# ----------------------------
# MOCK MODEL (replace later with real LLM)
# ----------------------------
def generate_answer(question):
    if "Tesla" in question:
        return "Electric vehicles and clean energy products https://www.sec.gov/edgar/browse/?CIK=1318605"
    return "I don't know but guessing AI chips spending is $5B"

# ----------------------------
# SCORING LOGIC (STRICT JUDGE)
# ----------------------------
def score(item, prediction):
    expected = item["expected_answer"]

    # RULE 1: traceability requirement
    if not has_valid_sec_url(prediction):
        return 0, "NO_SEC_URL"

    # RULE 2: trick question handling
    if expected == "NOT_IN_SOURCE":
        if "I don't know" in prediction or "guess" in prediction.lower():
            return 1, "SAFE_ABSTAIN"
        return 0, "HALLUCINATION_ON_TRICK"

    # RULE 3: normal accuracy check
    if expected.lower() in prediction.lower():
        return 1, "MATCH"

    return 0, "MISMATCH"

# ----------------------------
# OPTIONAL: SLACK + HUMAN ROUTING
# ----------------------------
def send_to_slack(payload):
    print(f"📨 Sending to Slack: {payload}")

def log_for_human_review(payload):
    print(f"🧑 Human Review Needed: {payload}")

# ----------------------------
# MAIN
# ----------------------------
def main():
    dataset = load_dataset()

    print("✅ Evaluator running")
    print("✅ Found golden dataset")

    correct = 0

    for item in dataset:
        prediction = generate_answer(item["question"])
        score_val, reason = score(item, prediction)

        correct += score_val

        print("\n---")
        print("Q:", item["question"])
        print("Prediction:", prediction)
        print("Source:", item["source"])
        print("Score:", score_val, "| Reason:", reason)

        # ----------------------------
        # AGENTIC HANDSHAKE (NEW)
        # ----------------------------
        if score_val >= 0.9:
            send_to_slack({
                "ticker": item["ticker"],
                "status": "PASS",
                "reason": reason
            })
        else:
            log_for_human_review({
                "ticker": item["ticker"],
                "status": "FAIL",
                "reason": reason
            })

    print("\n📊 Final Accuracy:", correct / len(dataset))

if __name__ == "__main__":
    main()