from __future__ import annotations


DIAGNOSIS_RULES: list[dict[str, object]] = [
    {
        "keywords": ["yellow", "yellowing", "yellow leaves"],
        "disease": "Chlorosis (Yellowing)",
        "cause": "Nutrient deficiency (usually iron or nitrogen) or overwatering.",
        "treatment": (
            "Check soil pH (ideal 6.0–7.0). Apply balanced fertilizer or iron chelate. "
            "Reduce watering frequency and ensure proper drainage."
        ),
        "confidence": "high",
    },
    {
        "keywords": ["brown", "brown spots", "brown edges", "brown tips"],
        "disease": "Leaf Scorch / Tip Burn",
        "cause": "Underwatering, low humidity, excess fertilizer salts, or direct harsh sunlight.",
        "treatment": (
            "Increase watering. Mist leaves or place near a humidity source. "
            "Flush soil to remove fertilizer buildup. Move away from direct afternoon sun."
        ),
        "confidence": "high",
    },
    {
        "keywords": ["wilting", "drooping", "limp", "droopy"],
        "disease": "Wilting / Root Stress",
        "cause": "Overwatering causing root rot OR underwatering causing dehydration.",
        "treatment": (
            "Check soil moisture. If soggy — let dry out, inspect roots for rot, repot if needed. "
            "If dry — water deeply and consistently."
        ),
        "confidence": "medium",
    },
    {
        "keywords": ["white powder", "white coating", "powdery", "mold"],
        "disease": "Powdery Mildew",
        "cause": "Fungal infection caused by poor air circulation and high humidity.",
        "treatment": (
            "Remove infected leaves. Improve airflow. Avoid overhead watering. "
            "Apply neem oil or a fungicide as directed."
        ),
        "confidence": "high",
    },
    {
        "keywords": ["black spots", "dark spots", "spotting", "leaf spots"],
        "disease": "Leaf Spot Disease",
        "cause": "Fungal or bacterial infection, often due to wet leaves and poor airflow.",
        "treatment": (
            "Remove affected leaves. Keep foliage dry. Improve ventilation. "
            "Use copper-based spray if the problem spreads."
        ),
        "confidence": "medium",
    },
    {
        "keywords": ["soft", "mushy", "rot", "smell", "root rot"],
        "disease": "Root Rot",
        "cause": "Overwatering and poor drainage causing roots to decay.",
        "treatment": (
            "Remove plant from pot, trim rotten roots, and repot in fresh well-draining soil. "
            "Water only when the top soil dries."
        ),
        "confidence": "high",
    },
    {
        "keywords": ["tiny insects", "aphids", "bugs", "sticky", "honeydew"],
        "disease": "Aphid / Pest Infestation",
        "cause": "Sap-sucking pests weakening the plant and spreading disease.",
        "treatment": (
            "Rinse leaves with water. Apply insecticidal soap or neem oil. "
            "Isolate infected plants to prevent spread."
        ),
        "confidence": "medium",
    },
    {
        "keywords": ["holes", "chewed", "bite marks", "snails", "slugs"],
        "disease": "Chewing Pest Damage",
        "cause": "Snails, slugs, caterpillars, or other chewing insects.",
        "treatment": (
            "Inspect at night, remove pests manually, and use safe bait/traps. "
            "Apply suitable organic pest control if needed."
        ),
        "confidence": "medium",
    },
]


DEFAULT_RESPONSE = {
    "disease": "Unknown Condition",
    "cause": "Symptoms are not specific enough for a confident rule-based diagnosis.",
    "treatment": (
        "Provide more detail (leaf color, spots, pests, watering schedule, sunlight). "
        "Check for pests under leaves and review watering/drainage."
    ),
    "confidence": "low",
}


def _score(symptoms: str, keywords: list[str]) -> int:
    s = symptoms.lower()
    return sum(1 for k in keywords if k.lower() in s)


def diagnose_plant(symptoms: str) -> dict:
    text = (symptoms or "").strip()
    if not text:
        return {
            "possible_disease": DEFAULT_RESPONSE["disease"],
            "cause": DEFAULT_RESPONSE["cause"],
            "treatment": DEFAULT_RESPONSE["treatment"],
            "confidence": DEFAULT_RESPONSE["confidence"],
            "disclaimer": (
                "This is an automated rule-based diagnosis for informational purposes only. "
                "For serious plant health issues, consult a professional horticulturist."
            ),
        }

    best_match: dict[str, object] | None = None
    best_score = 0
    for rule in DIAGNOSIS_RULES:
        keywords = rule["keywords"]
        if not isinstance(keywords, list):
            continue
        score = _score(text, keywords)
        if score > best_score:
            best_score = score
            best_match = rule

    result = best_match if best_match and best_score > 0 else DEFAULT_RESPONSE
    return {
        "possible_disease": result["disease"],
        "cause": result["cause"],
        "treatment": result["treatment"],
        "confidence": result["confidence"],
        "disclaimer": (
            "This is an automated rule-based diagnosis for informational purposes only. "
            "For serious plant health issues, consult a professional horticulturist."
        ),
    }

