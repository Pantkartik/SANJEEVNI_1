import json
import os
import uuid
from typing import Dict, List, Tuple, Union
from models.user import UserInit
from models.response import QuestionOut
from utils.helpers import score_option_index, generate_feedback

QUESTIONS_DIR = os.path.join(os.path.dirname(__file__), "questions")

def _load_json(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class ChatbotEngine:
    def __init__(self):
        # Load question banks once
        self.q_general = _load_json(os.path.join(QUESTIONS_DIR, "general.json"))
        self.q_students = _load_json(os.path.join(QUESTIONS_DIR, "students.json"))
        self.q_working = _load_json(os.path.join(QUESTIONS_DIR, "working.json"))
        self.q_others  = _load_json(os.path.join(QUESTIONS_DIR, "others.json"))
        # Simple in-memory session store
        self.sessions: Dict[str, dict] = {}

    def _choose_bank(self, user: UserInit) -> List[dict]:
        prof = user.profession.lower().strip()
        if prof in ["student", "school", "college", "university"]:
            base = self.q_students
        elif prof in ["working", "professional", "employee", "it", "doctor", "teacher"]:
            base = self.q_working
        else:
            base = self.q_others

        # Always prepend a few general questions
        combined = self.q_general + base
        # Cap between 15-20 questions (keep first 16 for consistency)
        return combined[:16]

    def start_session(self, user: UserInit) -> Tuple[str, QuestionOut]:
        if user.age < 12 or user.age > 100:
            raise ValueError("Age must be between 12 and 100.")
        q_bank = self._choose_bank(user)
        if not q_bank:
            raise ValueError("No questions available for the selected profile.")

        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user": user.dict(),
            "questions": q_bank,
            "index": 0,
            "answers": [],  # list of (question_id, option_index, score)
            "done": False
        }
        q = q_bank[0]
        return session_id, QuestionOut(
            id=q["id"],
            text=q["question"],
            options=q["options"],
            number=1,
            total=len(q_bank)
        )

    def get_current_question(self, session_id: str) -> QuestionOut:
        s = self.sessions[session_id]
        if s["done"]:
            raise ValueError("Session already completed.")
        i = s["index"]
        q = s["questions"][i]
        return QuestionOut(
            id=q["id"],
            text=q["question"],
            options=q["options"],
            number=i+1,
            total=len(s["questions"])
        )

    def submit_answer(self, session_id: str, question_id: int, option_index: int) -> Union[QuestionOut, dict]:
        s = self.sessions[session_id]
        if s["done"]:
            raise ValueError("Session already completed.")

        i = s["index"]
        q = s["questions"][i]
        if q["id"] != question_id:
            raise ValueError("Question ID does not match the expected current question.")
        if option_index < 0 or option_index >= len(q["options"]):
            raise ValueError("Invalid option index.")

        # Score this answer
        sc = score_option_index(option_index, q.get("polarity", "neg"))
        s["answers"].append((question_id, option_index, sc))
        s["index"] += 1

        if s["index"] >= len(s["questions"]):
            s["done"] = True
            total = sum(a[2] for a in s["answers"])
            max_score = len(s["answers"]) * 3  # since option index maps 0..3
            feedback, level = generate_feedback(total, max_score)
            return {
                "score": total,
                "max_score": max_score,
                "level": level,
                "feedback": feedback
            }

        # Next question
        nxt = s["questions"][s["index"]]
        return QuestionOut(
            id=nxt["id"],
            text=nxt["question"],
            options=nxt["options"],
            number=s["index"]+1,
            total=len(s["questions"])
        )
