def score_option_index(option_index: int, polarity: str = "neg") -> int:
    """
    Maps option index (0..3) to a score 0..3.
    polarity='neg' means higher index is worse (Never..Always).
    polarity='pos' means higher index is better (Always..Never).
    """
    if polarity == "neg":
        return option_index  # 0 good, 3 bad
    else:
        # flip scoring for positive questions (where higher index means healthier)
        return 3 - option_index

def generate_feedback(score: int, max_score: int) -> tuple[str, str]:
    """
    Lower score = healthier. We map to levels.
    """
    pct = (score / max_score) if max_score else 0
    if pct < 0.25:
        return ("Your responses indicate generally good mental well-being. "
                "Maintain sleep hygiene, social connection, and balanced routines.", "Low")
    elif pct < 0.55:
        return ("Mild stress signals detected. Consider mindful breathing, short walks, "
                "journaling, and reducing screen time before bed.", "Mild")
    elif pct < 0.8:
        return ("Moderate stress/anxiety indicators present. Build a daily routine: "
                "7–8 hrs sleep, 10–15 min mindfulness, talk to a trusted person. "
                "If symptoms persist, consult a professional.", "Moderate")
    else:
        return ("High stress/anxiety risk. Please reach out to a counselor/therapist or "
                "doctor. If you experience thoughts of self-harm, contact a helpline "
                "or a trusted person immediately.", "High")
