from fastapi import APIRouter
from models import User, Answers, Result, QuestionOut
from questions import get_questions_for_age
from scoring import calculate_score

router = APIRouter()

@router.post("/onboarding")
def onboarding(user: User):
    return {"message": f"Welcome {user.name}!", "age": user.age}

@router.get("/questions/{age}", response_model=list[QuestionOut])
def fetch_questions(age: int):
    return get_questions_for_age(age)

@router.post("/submit")
def submit_answers(data: Answers):
    score, assessment = calculate_score(data.answers)
    result = Result(user_id=data.user_id, score=score, assessment=assessment)
    return result
