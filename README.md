# Task Tracker

This is a small, simple task tracking web app built with Flask and SQLite. I started this project to keep track of daily tasks and to learn more about Flask and SQLAlchemy. It's kinda minimal but works for basic stuff.

---

## What it does

- Create, edit and delete tasks
- Set priority (Low / Medium / High)
- Add due dates and change status (Pending / In Progress / Completed)
- Shows a tiny "insight" message on the overview (like how many high priority and upcoming tasks)

## Tech stack

- Python 3.10+ (should work with other 3.x too)
- Flask (simple web framework)
- Flask-SQLAlchemy for DB
- SQLite for local dev DB
- Bootstrap 5 for basic styling

## Project structure (important files)

- `task_tracker/app.py` - main Flask app and models
- `task_tracker/templates/` - html templates (base, index, create, edit)
- `instance/` - (optional) place for tasks.db or other runtime files
- `readme.md` - this file

## Quick start (dev)

1. Create virtual env and activate it (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install deps

```powershell
pip install flask flask_sqlalchemy
```

3. Run the app

```powershell

python app.py

python -m task_tracker.app
```

4. Open http://127.0.0.1:5000 in your browser

Note: The app will create `tasks.db` in the app folder automatically on first run.

## Routes (what each page does)

- `/` - list tasks, filter by status and sort by due date/title/priority
- `/create` - create a new task
- `/edit/<id>` - edit task
- `/delete/<id>` (POST) - delete task

## Data model

Task has: id, title, description, priority, due_date, status, created_at.

## Known issues / TODOs

- No user auth, it's single-user right now
- Validation is melty (needs better checks for fields)
- The UI is basic, could be improved
- Tests are not added yet

## How I tested it (quick)

- Ran the app locally and added few tasks
- Confirmed create/edit/delete works and the insight message shows

## If you want to contrib

Just fork, make changes and open a PR. If you need help running the app lmk.

---

This README was written quick by a new dev, so might have typos and stuff. If you want a cleaned, formal README I can make one.
