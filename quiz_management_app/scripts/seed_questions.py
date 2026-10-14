from backend import database

SAMPLE_QUESTIONS = [
    ("General Knowledge", "Easy", "What is the capital of France?",
     ["Paris", "Rome", "Berlin", "Madrid"], 0),
    ("General Knowledge", "Easy", "How many continents are there?",
     ["5", "6", "7", "8"], 2),
    ("General Knowledge", "Medium", "Which planet is known as the Red Planet?",
     ["Venus", "Mars", "Jupiter", "Saturn"], 1),
    ("Python", "Easy", "Which keyword is used to define a function in Python?",
     ["func", "def", "function", "lambda"], 1),
    ("Python", "Medium", "What data type does `{1, 2, 3}` represent in Python?",
     ["List", "Tuple", "Set", "Dictionary"], 2),
    ("Python", "Hard", "What does the acronym 'PEP' stand for in the Python world?",
     ["Python Enhancement Proposal", "Python Execution Plan",
      "Public Extension Package", "Program Evaluation Process"], 0),
    ("Math", "Easy", "What is 12 x 8?",
     ["96", "88", "104", "80"], 0),
    ("Math", "Medium", "What is the square root of 144?",
     ["10", "11", "12", "13"], 2),
]

if __name__ == "__main__":
    database.init_db()
    added = 0
    for category, difficulty, text, options, correct in SAMPLE_QUESTIONS:
        database.add_question(category, difficulty, text, options, correct)
        added += 1
    print(f"Seeded {added} sample questions across "
          f"{len(set(q[0] for q in SAMPLE_QUESTIONS))} categories.")
