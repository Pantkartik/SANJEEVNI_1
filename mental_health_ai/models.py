from pydantic import BaseModel, Field
from typing import List

class StartRequest(BaseModel):
    name: str = Field(..., example="Aarav")
    age: int = Field(..., ge=5, le=120, example=20)

class StartResponse(BaseModel):
    session_id: str
    message: str

class QuestionOut(BaseModel):
    id: int
    text: str
    options: List[str]

class SubmitRequest(BaseModel):
    session_id: str
    answers: List[int]  # 15 integers 0..3

class SubmitResponse(BaseModel):
    user_name: str
    age: int
    depression_score: int
    depression_level: str
    anxiety_score: int
    anxiety_level: str
    overall: str
    recommendation: str
