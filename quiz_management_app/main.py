from datetime import datetime
from pathlib import Path

from backend import database


RESULTS_FILE = Path(__file__).resolve().parent / "file.txt"


def main():
    database.init_db()
    categories = database.get_categories()
    if not categories:
        print("No quiz questions found. Run: python -m scripts.seed_questions")
        return

    print("QUIZ MANAGEMENT APP")
    print("===================")
    username = input("Your name: ").strip() or "Player"

    print("\nChoose a category:")
    for number, category in enumerate(categories, start=1):
        print(f"{number}. {category}")

    while True:
        try:
            choice = int(input("Category number: ").strip())
            if 1 <= choice <= len(categories):
                break
        except ValueError:
            pass
        print(f"Enter a number from 1 to {len(categories)}.")

    category = categories[choice - 1]
    questions = database.load_questions(category)
    score = 0
    print(f"\n{category} quiz ({len(questions)} questions)\n")

    for question_number, question in enumerate(questions, start=1):
        print(f"{question_number}. {question['text']}")
        for option_number, option in enumerate(question["options"], start=1):
            print(f"   {option_number}. {option}")

        while True:
            try:
                answer = int(input("Your answer: ").strip())
                if 1 <= answer <= len(question["options"]):
                    break
            except ValueError:
                pass
            print(f"Enter a number from 1 to {len(question['options'])}.")

        if answer - 1 == question["correct_index"]:
            score += 1

    percentage = round(score / len(questions) * 100) if questions else 0
    timestamp = datetime.now().isoformat(timespec="seconds")
    record = f"{timestamp} | {username} | {category} | {score}/{len(questions)} ({percentage}%)\n"
    with RESULTS_FILE.open("a", encoding="utf-8") as results_file:
        results_file.write(record)

    print(f"\nScore: {score}/{len(questions)} ({percentage}%)")
    print(f"Result saved to {RESULTS_FILE.name}")


if __name__ == "__main__":
    main()
