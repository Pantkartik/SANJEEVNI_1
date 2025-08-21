class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.history = []

    def add_to_history(self, question: str, answer: str):
        self.history.append({"question": question, "answer": answer})
