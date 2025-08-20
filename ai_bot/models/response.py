from pydantic import BaseModel
from typing import List, Optional

class QuestionOut(BaseModel):
    id: int
    text: str
    options: List[str]
    number: int
    total: int

class StartResponse(BaseModel):
    session_id: str
    question: QuestionOut

class ResultOut(BaseModel):
    score: int
    max_score: int
    level: str
    feedback: str

class AnswerIn(BaseModel):
    session_id: str
    question_id: int
    option_index: int  # 0..3

class NextQResponse(BaseModel):
    done: bool
    question: Optional[QuestionOut] = None
    result: Optional[ResultOut] = None
