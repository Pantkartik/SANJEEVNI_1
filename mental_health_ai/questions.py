from typing import List, Dict

# Standard options for scoring 0..3
OPTIONS = ["Not at all", "Several days", "More than half the days", "Nearly every day"]

# We compose a 15-question set:
# - First 9 are depression-like (PHQ-style)
# - Next 6 are anxiety-like (abbreviated GAD-style)
# For teens we keep wording youth-friendly.

ADULT_QUESTIONS: List[Dict] = [
    {"id": 1001, "question": "Little interest or pleasure in doing things?", "options": OPTIONS},
    {"id": 1002, "question": "Feeling down, depressed, or hopeless?", "options": OPTIONS},
    {"id": 1003, "question": "Trouble falling or staying asleep, or sleeping too much?", "options": OPTIONS},
    {"id": 1004, "question": "Feeling tired or having little energy?", "options": OPTIONS},
    {"id": 1005, "question": "Poor appetite or overeating?", "options": OPTIONS},
    {"id": 1006, "question": "Feeling bad about yourself — or that you are a failure?", "options": OPTIONS},
    {"id": 1007, "question": "Trouble concentrating on things (like reading or watching)?", "options": OPTIONS},
    {"id": 1008, "question": "Moving or speaking slowly, or being fidgety/restless?", "options": OPTIONS},
    {"id": 1009, "question": "Thoughts that you would be better off dead, or hurting yourself?", "options": OPTIONS},
    # anxiety-like (6)
    {"id": 1010, "question": "Feeling nervous, anxious, or on edge?", "options": OPTIONS},
    {"id": 1011, "question": "Not being able to stop or control worrying?", "options": OPTIONS},
    {"id": 1012, "question": "Worrying too much about different things?", "options": OPTIONS},
    {"id": 1013, "question": "Trouble relaxing?", "options": OPTIONS},
    {"id": 1014, "question": "Being so restless that it's hard to sit still?", "options": OPTIONS},
    {"id": 1015, "question": "Becoming easily annoyed or irritable?", "options": OPTIONS},
]

TEEN_QUESTIONS: List[Dict] = [
    {"id": 2001, "question": "Little interest or pleasure in usual activities?", "options": OPTIONS},
    {"id": 2002, "question": "Feeling down, sad, or hopeless?", "options": OPTIONS},
    {"id": 2003, "question": "Trouble sleeping or sleeping too much?", "options": OPTIONS},
    {"id": 2004, "question": "Feeling tired or low on energy?", "options": OPTIONS},
    {"id": 2005, "question": "Eating much more or much less than usual?", "options": OPTIONS},
    {"id": 2006, "question": "Feeling bad about yourself or you let yourself down?", "options": OPTIONS},
    {"id": 2007, "question": "Finding it hard to concentrate in school or while studying?", "options": OPTIONS},
    {"id": 2008, "question": "Feeling restless or moving/speaking more than usual?", "options": OPTIONS},
    {"id": 2009, "question": "Having thoughts you don't want or that scare you?", "options": OPTIONS},
    # anxiety-like (6)
    {"id": 2010, "question": "Feeling nervous or on edge much of the time?", "options": OPTIONS},
    {"id": 2011, "question": "Not able to control your worries?", "options": OPTIONS},
    {"id": 2012, "question": "Worry interfering with school or friendships?", "options": OPTIONS},
    {"id": 2013, "question": "Difficulty relaxing or calming down?", "options": OPTIONS},
    {"id": 2014, "question": "Feeling restless or keyed up?", "options": OPTIONS},
    {"id": 2015, "question": "Getting easily annoyed or angry?", "options": OPTIONS},
]

def get_questions_for_age(age: int) -> List[Dict]:
    """
    Returns list of 15 questions appropriate for the given age.
    """
    if age < 13:
        # for younger kids we'll still return teen set (can be refined later)
        bank = TEEN_QUESTIONS
    elif 13 <= age <= 17:
        bank = TEEN_QUESTIONS
    else:
        bank = ADULT_QUESTIONS

    # always return the first 15 (we already have 15)
    selected = bank[:15]
    # transform keys to match QuestionOut model (id, text, options)
    out = []
    for q in selected:
        out.append({
            "id": q["id"],
            "text": q["question"],
            "options": q["options"]
        })
    return out
