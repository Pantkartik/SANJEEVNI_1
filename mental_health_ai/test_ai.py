import requests

# Backend URL
BASE_URL = "http://127.0.0.1:8000"

# 1️⃣ Start a session
name = input("Enter your name: ")
age = int(input("Enter your age: "))

start_payload = {"name": name, "age": age}
start_response = requests.post(f"{BASE_URL}/start", json=start_payload).json()

session_id = start_response.get("session_id")
print(f"\nSession created! ID: {session_id}\n")

# 2️⃣ Get questions from backend
questions_response = requests.get(f"{BASE_URL}/questions/{session_id}")
questions = questions_response.json()

print("Answer the questions with numbers 0-3:")
print("0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day\n")

answers = []
for q in questions:
    while True:
        try:
            answer = int(input(f"{q['text']}\nYour answer: "))
            if answer in [0, 1, 2, 3]:
                answers.append(answer)
                break
            else:
                print("Invalid input! Please enter 0, 1, 2, or 3.")
        except ValueError:
            print("Invalid input! Enter a number between 0 and 3.")

# 3️⃣ Submit answers
submit_url = f"{BASE_URL}/submit"
submit_payload = {"session_id": session_id, "answers": answers}
result = requests.post(submit_url, json=submit_payload).json()

# 4️⃣ Print results
print("\n=== Evaluation Result ===")
print(f"Name: {result['user_name']}")
print(f"Age: {result['age']}")
print(f"Depression Score: {result['depression_score']} ({result['depression_level']})")
print(f"Anxiety Score: {result['anxiety_score']} ({result['anxiety_level']})")
print(f"Overall: {result['overall']}")
print(f"Recommendation: {result['recommendation']}")
