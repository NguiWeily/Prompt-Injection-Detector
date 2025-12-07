import re

RULES = {
    r"(ignore (all|previous) instructions)": 0.6,
    r"(forget previous directives)": 0.6,
    r"(disregard.*rules)": 0.7,
    r"(override.*system)": 0.8,
    r"(reveal.*(system|developer) prompt)": 0.9,
    r"(you are no longer an ai)": 0.7,
    r"(perform dangerous|illegal|bypass safety)": 1.0,
    r"(act as jailbreak|act as dan|act as chaosgpt)": 1.0,
    r"(simulate unrestricted mode|no limitations)": 0.8,
    r"(bypass content filter|disable safety)": 1.0,
}

def detect_injection(text):
    triggered = []
    score = 0.0

    for pattern, weight in RULES.items():
        if re.search(pattern, text, re.IGNORECASE):
            triggered.append(pattern)
            score += weight

    # --- improved scoring classification ---
    if score >= 1.5:
        verdict = "high"
    elif score >= 0.6:
        verdict = "medium"
    else:
        verdict = "low"

    # Cap at 1.0
    final_score = min(score, 1.0)

    return {
        "input": text,
        "triggered_rules": triggered,
        "final_score": final_score,
        "verdict": verdict,
        "suggested_actions": (
            ["block request"] if verdict == "high" else
            ["review manually"] if verdict == "medium" else
            []
        ),
    }
