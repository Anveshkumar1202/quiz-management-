# Quiz Management App

A simple terminal quiz. Questions are loaded from the local SQLite database, and each score is appended to `file.txt`.

## Run

Requires Python 3.8 or newer. No packages need to be installed.

```powershell
python main.py
```

Enter a player name, choose a category, and answer each question with its option number. Results are saved in the project folder as `file.txt`.

## Add Sample Questions

```powershell
python -m scripts.seed_questions
```

This adds the sample questions to `data/quiz.db`. It can be run again to add another copy of each question.

## Project Guide

See [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for the file-by-file explanation, technologies, and program flow.

## Files

- `main.py` runs the quiz in the terminal and records scores.
- `backend/database.py` creates the SQLite database and loads quiz questions.
- `scripts/seed_questions.py` adds sample questions.
- `data/quiz.db` stores quiz questions.
- `file.txt` is created after the first completed quiz; each result is appended with the date, player, category, and score.
