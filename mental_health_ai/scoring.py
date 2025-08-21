from typing import List, Dict

def evaluate_answers(answers: List[int]) -> Dict:
    """
    answers: list of 15 integers (0..3)
    Returns dictionary with depression & anxiety scores, interpretation,
    overall and recommendation.
    - First 9 answers map to depression (PHQ-style).
    - Next 6 answers map to anxiety (abbreviated).
    """

    # validation
    if len(answers) != 15:
        raise ValueError("answers must be a list of 15 integers (0..3)")

    # ensure each answer is 0..3
    for a in answers:
        if not isinstance(a, int) or a < 0 or a > 3:
            raise ValueError("each answer must be integer 0..3")

    # split
    depression_answers = answers[:9]   # 0..27
    anxiety_answers = answers[9:]      # 0..18 (6 items)

    depression_score = sum(depression_answers)
    anxiety_score = sum(anxiety_answers)

    # depression interpretation using PHQ-9 bands
    if depression_score <= 4:
        dep_level = "Minimal or None"
    elif 5 <= depression_score <= 9:
        dep_level = "Mild"
    elif 10 <= depression_score <= 14:
        dep_level = "Moderate"
    elif 15 <= depression_score <= 19:
        dep_level = "Moderately severe"
    else:
        dep_level = "Severe"

    # anxiety interpretation (6-item scale, thresholds scaled similarly)
    # max = 18. We'll use proportional thresholds similar to GAD-7 bands.
    if anxiety_score <= 4:
        anx_level = "Minimal or None"
    elif 5 <= anxiety_score <= 9:
        anx_level = "Mild"
    elif 10 <= anxiety_score <= 14:
        anx_level = "Moderate"
    else:
        anx_level = "Severe"

    # overall logic — conservative approach: choose higher concern area
    overall = "Healthy"
    high_dep = depression_score >= 10  # clinical threshold
    high_anx = anxiety_score >= 10

    if high_dep and high_anx:
        overall = "Significant symptoms of both depression and anxiety"
    elif high_dep:
        overall = "Significant symptoms of depression"
    elif high_anx:
        overall = "Significant symptoms of anxiety"
    elif dep_level == "Mild" or anx_level == "Mild":
        overall = "Mild symptoms — monitor and consider self-help strategies"
    else:
        overall = "No significant symptoms detected"

    # recommendation text
    recommendation = []
    if depression_score >= 10:
        recommendation.append("Your depression score suggests moderate to severe symptoms — consider seeing a mental health professional.")
    elif depression_score >= 5:
        recommendation.append("Mild depressive symptoms — try self-care, maintain sleep, routine, stay connected; re-check in a few weeks.")

    if anxiety_score >= 10:
        recommendation.append("Your anxiety score suggests moderate to severe symptoms — consider talking to a counselor or doctor.")
    elif anxiety_score >= 5:
        recommendation.append("Mild anxiety symptoms — try breathing exercises, short walks, and relaxation techniques.")

    if not recommendation:
        recommendation.append("No immediate action needed; continue healthy routines and reach out if things change.")

    return {
        "depression_score": depression_score,
        "depression_level": dep_level,
        "anxiety_score": anxiety_score,
        "anxiety_level": anx_level,
        "overall": overall,
        "recommendation": " ".join(recommendation)
    }
