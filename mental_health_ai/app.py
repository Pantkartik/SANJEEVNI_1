from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Mental Health AI backend is running"}

@app.get("/questions")
def get_questions():
    return {
        "questions": [
            "How are you feeling today?",
            "Have you been sleeping well?",
            "Do you feel stressed or anxious recently?"
        ]
    }
