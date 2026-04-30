from __future__ import annotations


DIAGNOSIS_RULES: list[dict[str, object]] = [
    {
        "keywords": ["yellow", "yellowing", "yellow leaves", "صفراء", "اصفرار", "أصفر"],
        "disease": "Chlorosis (Yellowing)",
        "disease_ar": "اصفرار الأوراق (Chlorosis)",
        "cause": "Nutrient deficiency (usually iron or nitrogen) or overwatering.",
        "cause_ar": "نقص المغذيات (عادة الحديد أو النيتروجين) أو الري الزائد.",
        "treatment": (
            "Check soil pH (ideal 6.0–7.0). Apply balanced fertilizer or iron chelate. "
            "Reduce watering frequency and ensure proper drainage."
        ),
        "treatment_ar": "تحقق من حموضة التربة. أضف سماداً متوازناً. قلل من وتيرة الري وتأكد من تصريف المياه بشكل جيد.",
        "confidence": "high",
    },
    {
        "keywords": ["brown", "brown spots", "brown edges", "brown tips", "بنية", "بقع", "بني"],
        "disease": "Leaf Scorch / Tip Burn",
        "disease_ar": "احتراق أطراف الأوراق",
        "cause": "Underwatering, low humidity, excess fertilizer salts, or direct harsh sunlight.",
        "cause_ar": "نقص الري، انخفاض الرطوبة، زيادة الأملاح أو التعرض المباشر لأشعة الشمس القوية.",
        "treatment": (
            "Increase watering. Mist leaves or place near a humidity source. "
            "Flush soil to remove fertilizer buildup. Move away from direct afternoon sun."
        ),
        "treatment_ar": "زد من وتيرة الري. رش الأوراق برذاذ الماء أو ضع النبات في مكان رطب. اغسل التربة للتخلص من تراكم الأملاح.",
        "confidence": "high",
    },
    {
        "keywords": ["wilting", "drooping", "limp", "droopy", "ذبول", "ذابلة", "تميل"],
        "disease": "Wilting / Root Stress",
        "disease_ar": "ذبول / إجهاد الجذور",
        "cause": "Overwatering causing root rot OR underwatering causing dehydration.",
        "cause_ar": "الري الزائد المسبب لعفن الجذور أو نقص الري المسبب للجفاف.",
        "treatment": (
            "Check soil moisture. If soggy — let dry out, inspect roots for rot, repot if needed. "
            "If dry — water deeply and consistently."
        ),
        "treatment_ar": "تحقق من رطوبة التربة. إذا كانت مشبعة بالماء، اتركها لتجف وافحص الجذور. إذا كانت جافة، قم بالري بانتظام.",
        "confidence": "medium",
    },
    {
        "keywords": ["white powder", "white coating", "powdery", "mold", "بودرة", "أبيض", "طبقة بيضاء"],
        "disease": "Powdery Mildew",
        "disease_ar": "البياض الدقيقي",
        "cause": "Fungal infection caused by poor air circulation and high humidity.",
        "cause_ar": "عدوى فطرية ناتجة عن سوء تهوية المكان وارتفاع الرطوبة.",
        "treatment": (
            "Remove infected leaves. Improve airflow. Avoid overhead watering. "
            "Apply neem oil or a fungicide as directed."
        ),
        "treatment_ar": "تخلص من الأوراق المصابة. حسن تهوية المكان. تجنب ري الأوراق من الأعلى واستخدم زيت النيم.",
        "confidence": "high",
    },
    {
        "keywords": ["black spots", "dark spots", "spotting", "leaf spots", "سوداء", "بقع غامقة"],
        "disease": "Leaf Spot Disease",
        "disease_ar": "مرض تبقع الأوراق",
        "cause": "Fungal or bacterial infection, often due to wet leaves and poor airflow.",
        "cause_ar": "عدوى فطرية أو بكتيرية، غالباً بسبب رطوبة الأوراق الدائمة وضعف التهوية.",
        "treatment": (
            "Remove affected leaves. Keep foliage dry. Improve ventilation. "
            "Use copper-based spray if the problem spreads."
        ),
        "treatment_ar": "أزل الأوراق المصابة. حافظ على جفاف الأوراق وحسن التهوية. استخدم رذاذ النحاس إذا انتشر المرض.",
        "confidence": "medium",
    },
    {
        "keywords": ["soft", "mushy", "rot", "smell", "root rot", "عفن", "رائحة كريهة", "جذور"],
        "disease": "Root Rot",
        "disease_ar": "عفن الجذور",
        "cause": "Overwatering and poor drainage causing roots to decay.",
        "cause_ar": "الري الزائد وسوء تصريف المياه مما يؤدي لتحلل الجذور.",
        "treatment": (
            "Remove plant from pot, trim rotten roots, and repot in fresh well-draining soil. "
            "Water only when the top soil dries."
        ),
        "treatment_ar": "أخرج النبات من الأصيص، قص الجذور المتعفنة، وأعد زراعته في تربة جديدة جيدة التصريف.",
        "confidence": "high",
    },
    {
        "keywords": ["tiny insects", "aphids", "bugs", "sticky", "honeydew", "حشرات", "من", "لزج"],
        "disease": "Aphid / Pest Infestation",
        "disease_ar": "إصابة بالمن أو الآفات",
        "cause": "Sap-sucking pests weakening the plant and spreading disease.",
        "cause_ar": "حشرات تمتص عصارة النبات وتضعفه وتنقل الأمراض.",
        "treatment": (
            "Rinse leaves with water. Apply insecticidal soap or neem oil. "
            "Isolate infected plants to prevent spread."
        ),
        "treatment_ar": "اغسل الأوراق بالماء. استخدم الصابون المبيد للحشرات أو زيت النيم. اعزل النبات المصاب.",
        "confidence": "medium",
    },
    {
        "keywords": ["holes", "chewed", "bite marks", "snails", "slugs", "ثقوب", "قضم", "حلزون"],
        "disease": "Chewing Pest Damage",
        "disease_ar": "تلف بسبب الحشرات القارضة",
        "cause": "Snails, slugs, caterpillars, or other chewing insects.",
        "cause_ar": "القواقع، الحلزون، أو اليرقات التي تقضم الأوراق.",
        "treatment": (
            "Inspect at night, remove pests manually, and use safe bait/traps. "
            "Apply suitable organic pest control if needed."
        ),
        "treatment_ar": "افحص النبات ليلاً، أزل الحشرات يدوياً، واستخدم مصائد آمنة.",
        "confidence": "medium",
    },
]


DEFAULT_RESPONSE = {
    "disease": "Unknown Condition",
    "disease_ar": "حالة غير معروفة",
    "cause": "Symptoms are not specific enough for a confident rule-based diagnosis.",
    "cause_ar": "الأعراض غير محددة بما يكفي لتشخيص دقيق.",
    "treatment": (
        "Provide more detail (leaf color, spots, pests, watering schedule, sunlight). "
        "Check for pests under leaves and review watering/drainage."
    ),
    "treatment_ar": "يرجى تقديم تفاصيل أكثر (لون الورق، وجود حشرات، جدول الري). افحص أسفل الأوراق للتأكد من عدم وجود آفات.",
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
            "possible_disease_ar": DEFAULT_RESPONSE["disease_ar"],
            "cause": DEFAULT_RESPONSE["cause"],
            "cause_ar": DEFAULT_RESPONSE["cause_ar"],
            "treatment": DEFAULT_RESPONSE["treatment"],
            "treatment_ar": DEFAULT_RESPONSE["treatment_ar"],
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
        "possible_disease_ar": result["disease_ar"],
        "cause": result["cause"],
        "cause_ar": result["cause_ar"],
        "treatment": result["treatment"],
        "treatment_ar": result["treatment_ar"],
        "confidence": result["confidence"],
        "disclaimer": (
            "This is an automated rule-based diagnosis for informational purposes only. "
            "For serious plant health issues, consult a professional horticulturist."
        ),
    }

