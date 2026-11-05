import re


WEAPON_TERMS = [
    "gun", "rifle", "pistol", "shotgun", "firearm",
    "knife", "blade", "bomb", "explosive", "grenade",
    "weapon", "shoot", "shooting", "stab",
]

TARGET_LOCATION_TERMS = [
    "school", "classroom", "campus", "everyone", "everybody",
    "all of them", "my class", "students", "teacher", "teachers",
    "mall", "church", "concert", "workplace", "office",
]

SELF_HARM_METHOD_TERMS = [
    "overdose", "pills", "hanging", "jump off", "cut myself",
    "slit", "bleed out", "suffocate", "drown myself", "starve myself",
]

TEMPORAL_MARKERS = [
    "tonight", "tomorrow", "today", "right now", "going to", "i will",
    "i'm going to", "im going to", "already", "last time",
    "after school", "when i get home", "before anyone",
]

FAREWELL_TERMS = [
    "goodbye", "forever", "never coming back", "won't be here", "wont be here",
    "last message", "no point anymore", "nobody will miss me", "no one will miss me",
    "take care of my", "this is my last", "won't need this anymore", "wont need this anymore",
    "i'm done", "im done", "it's over", "its over", "end it all",
]

ACQUISITION_TERMS = [
    "i have a gun", "i have a knife", "i have a bomb",
    "i bought a gun", "i found a gun", "i got a gun", "i own a gun",
    "i bought a knife", "i found a knife",
]


def _matches_any(text: str, terms: list[str]) -> list[str]:
    matched = []
    for term in terms:
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, text):
            matched.append(term)
    return matched


def check_threat_escalation(text: str, probs: dict[str, float]) -> dict:
    t = text.lower()

    weapons = _matches_any(t, WEAPON_TERMS)
    targets = _matches_any(t, TARGET_LOCATION_TERMS)
    methods = _matches_any(t, SELF_HARM_METHOD_TERMS)
    temporal = _matches_any(t, TEMPORAL_MARKERS)
    farewells = _matches_any(t, FAREWELL_TERMS)
    acquisition = _matches_any(t, ACQUISITION_TERMS)

    triggered_rules: list[str] = []

    if weapons and targets:
        triggered_rules.append("Credible external threat (weapon + target location)")
    if methods and temporal:
        triggered_rules.append("Imminent self-harm risk (method + timing)")
    if farewells and probs.get("Depression", 0.0) >= 0.85:
        triggered_rules.append("Acute suicide risk (farewell language + high depression score)")
    if acquisition:
        triggered_rules.append("Threat preparation (explicit weapon possession)")

    matched_terms = {
        k: v
        for k, v in {
            "weapons": weapons,
            "targets": targets,
            "methods": methods,
            "temporal": temporal,
            "farewells": farewells,
            "acquisition": acquisition,
        }.items()
        if v
    }

    return {
        "escalated": len(triggered_rules) > 0,
        "triggered_rules": triggered_rules,
        "matched_terms": matched_terms,
        "reason": "; ".join(triggered_rules),
    }
