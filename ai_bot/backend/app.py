from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.user import UserInit
from models.response import AnswerIn, NextQResponse, StartResponse, QuestionOut, ResultOut
from chatbot import ChatbotEngine

app = FastAPI(title="ManasMitra Bot API", version="1.0.0")

# Allow your friend's frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ChatbotEngine()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/start", response_model=StartResponse)
def start(user: UserInit):
    try:
        session_id, first_q = engine.start_session(user)
        return StartResponse(session_id=session_id, question=first_q)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/answer", response_model=NextQResponse)
def answer(payload: AnswerIn):
    try:
        result_or_question = engine.submit_answer(
            payload.session_id,
            payload.question_id,
            payload.option_index
        )
        if isinstance(result_or_question, QuestionOut):
            return NextQResponse(done=False, question=result_or_question)
        else:
            # it's a result dict
            return NextQResponse(done=True, result=ResultOut(**result_or_question))
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/resume/{session_id}", response_model=QuestionOut)
def resume(session_id: str):
    try:
        return engine.get_current_question(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
