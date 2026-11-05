from config import COMBO_BONUSES, ESCALATION_GATE_THRESHOLD, LABEL_COLS, LABEL_WEIGHTS, ORANGE_THRESHOLD, RED_THRESHOLD, THRESHOLDS
from model import load_trained_model
from threat_rules import check_threat_escalation


def run_inference(text: str) -> dict[str, float]:
    """Return {label: probability} for all labels."""
    classifier = load_trained_model()
    raw = classifier(text)[0]  # list of {'label': ..., 'score': ...}
    return {item["label"]: item["score"] for item in raw}


def compute_alert(probs: dict[str, float]) -> dict:
    """Map per-label probabilities to a RED / ORANGE / GREEN alert dict."""
    EPSILON = 1e-4
    flagged = {lbl for lbl, p in probs.items() if p >= THRESHOLDS[lbl] - EPSILON}

    base_score = sum(probs[lbl] * LABEL_WEIGHTS[lbl] for lbl in flagged)

    bonus_total = 0.0
    triggered_combos = []
    for labels_needed, bonus, description in COMBO_BONUSES:
        if all(lbl in flagged for lbl in labels_needed):
            bonus_total += bonus
            triggered_combos.append(description)

    weighted_score = base_score + bonus_total

    if weighted_score >= RED_THRESHOLD:
        tier, emoji = "RED", "🔴"
        message = "Immediate concern – high-risk content detected."
    elif weighted_score >= ORANGE_THRESHOLD:
        tier, emoji = "ORANGE", "🟡"
        message = "Elevated concern – potentially harmful content detected."
    else:
        tier, emoji = "GREEN", "🟢"
        message = "No significant flags detected."

    return {
        "tier": tier,
        "emoji": emoji,
        "message": message,
        "weighted_score": round(weighted_score, 4),
        "base_score": round(base_score, 4),
        "combo_bonus": round(bonus_total, 4),
        "flagged_labels": sorted(flagged),
        "triggered_combos": triggered_combos,
        "label_probabilities": {lbl: round(p, 4) for lbl, p in probs.items()},
    }


def analyze_text(post_text: str) -> dict:
    probs = run_inference(post_text)
    result = compute_alert(probs)

    depression_gate = probs.get("Depression", 0.0) >= 0.85
    general_gate = any(p >= ESCALATION_GATE_THRESHOLD for p in probs.values())
    if depression_gate or general_gate:
        escalation = check_threat_escalation(post_text, probs)
        if escalation["escalated"]:
            result["tier"] = "RED"
            result["emoji"] = "🔴"
            result["message"] = "Immediate concern – high-risk content detected."
        result["escalation"] = escalation
    else:
        result["escalation"] = None

    return result
