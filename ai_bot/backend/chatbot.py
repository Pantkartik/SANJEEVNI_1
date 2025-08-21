import json
from models.response import generate_response  # correct import

# Load all question datasets
question_files = [
    "ai_bot/questions/general.json",
    "ai_bot/questions/others.json",
    "ai_bot/questions/students.json",
    "ai_bot/questions/working.json"
]

data = {}
for file in question_files:
    with open(file, 'r') as f:
        data.update(json.load(f))

def get_response(user_id: str, question: str) -> str:
    """
    Get AI bot response for a question
    """
    # Simple exact match
    response = data.get(question.lower())
    if response:
        return response
    # Fallback
    return generate_response(question)
