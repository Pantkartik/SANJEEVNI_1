from fastapi import FastAPI
from .chatbot import get_response  # <-- changed

from pydantic import BaseModel

app = FastAPI(title="SANJEEVNI AI Bot")

class Query(BaseModel):
    user_id: str
    question: str

@app.post("/ask")
async def ask_bot(query: Query):
    response_text = get_response(query.user_id, query.question)
    return {"response": response_text}

@app.get("/")
async def root():
    return {"message": "SANJEEVNI AI Bot is running!"}
