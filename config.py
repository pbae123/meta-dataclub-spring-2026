LABEL_COLS = ["Self-Harm", "Depression", "Aggression", "Anxiety", "Sexually suggestive"]

# A label is flagged when its probability >= 0.5
THRESHOLDS = {lbl: 0.5 for lbl in LABEL_COLS}

# How dangerous a true-positive is in isolation (1.0 low → 3.0 critical)
LABEL_WEIGHTS = {
    "Self-Harm":           3.0,
    "Depression":          1.5,
    "Aggression":          2.5,
    "Anxiety":             1.2,
    "Sexually suggestive": 1.8,
}

# Bonus score added when dangerous label combos co-occur
COMBO_BONUSES = [
    (["Self-Harm", "Depression"],               2.0, "Self-harm + Depression (suicide risk)"),
    (["Self-Harm", "Aggression"],               2.5, "Self-harm + Aggression (violent ideation)"),
    (["Self-Harm", "Depression", "Aggression"], 1.5, "Triple flag: SH + Dep + Agg"),
    (["Depression", "Anxiety"],                 0.5, "Depression + Anxiety (compounding)"),
    (["Aggression", "Anxiety"],                 0.8, "Aggression + Anxiety (volatile state)"),
    (["Self-Harm", "Sexually suggestive"],      1.2, "Self-harm + Sexual content (exploitation risk)"),
]

RED_THRESHOLD    = 3.0   # weighted_score >= this → RED
ORANGE_THRESHOLD = 1.4   # weighted_score >= this → ORANGE, else GREEN

ESCALATION_GATE_THRESHOLD = 0.90
