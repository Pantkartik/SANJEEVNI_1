from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import StartRequest, StartResponse, QuestionOut, SubmitRequest, SubmitResponse
from questions import get_questions_for_age
from scoring import evaluate_answers
from uuid import uuid4
from typing import Dict
from datetime import datetime

app = FastAPI(title="Mental Health AI (Backend)")

# Allow local frontend to call this backend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# In-memory session store: session_id -> { name, age, started_at }
SESSIONS: Dict[str, Dict] = {}

@app.get("/", tags=["health"])
def root():
    return {"message": "Mental Health AI backend is running"}

@app.post("/start", response_model=StartResponse, tags=["session"])
def start_session(payload: StartRequest):
    """
    Start a new session by providing name + age. Returns a session_id.
    Frontend should call /questions/{session_id} after this.
    """
    sid = str(uuid4())
    SESSIONS[sid] = {
        "name": payload.name,
        "age": payload.age,
        "started_at": datetime.utcnow().isoformat()
    }
    return StartResponse(session_id=sid, message=f"Hello {payload.name}, session created.")

@app.get("/questions/{session_id}", response_model=list[QuestionOut], tags=["questions"])
def get_questions(session_id: str):
    """
    Returns 15 questions chosen according to the user's age saved in the session.
    """
    info = SESSIONS.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Invalid session_id")
    age = info["age"]
    questions = get_questions_for_age(age)   # returns list of dicts {id, text, options}
    return questions

@app.post("/submit", response_model=SubmitResponse, tags=["evaluate"])
def submit_answers(payload: SubmitRequest):
    """
    Accepts answers array (length 15) where each answer is an int 0..3
    (0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day)
    Returns scores and interpretation for depression & anxiety.
    """
    info = SESSIONS.get(payload.session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Invalid session_id")

    # basic validation
    if not isinstance(payload.answers, list) or len(payload.answers) != 15:
        raise HTTPException(status_code=400, detail="answers must be a list of 15 integers (0..3)")

    # compute evaluation
    result = evaluate_answers(payload.answers)

    # optionally delete session after submit (privacy)
    try:
        del SESSIONS[payload.session_id]
    except KeyError:
        pass

    return SubmitResponse(
        user_name=info["name"],
        age=info["age"],
        depression_score=result["depression_score"],
        depression_level=result["depression_level"],
        anxiety_score=result["anxiety_score"],
        anxiety_level=result["anxiety_level"],
        overall=result["overall"],
        recommendation=result["recommendation"]
    )
