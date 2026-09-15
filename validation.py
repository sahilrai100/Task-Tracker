from datetime import datetime

TITLE_MAX_LENGTH = 120
ALLOWED_PRIORITIES = {"Low", "Medium", "High"}
ALLOWED_STATUSES = {"Pending", "In Progress", "Completed"}


def validate_task_data(form):
    """Validate a task form submission.

    `form` is a mapping with title, description, priority, due_date and
    status keys (as sent by the create/edit forms). Returns a list of
    human-readable error messages; an empty list means the data is valid.
    """
    errors = []

    title = (form.get("title") or "").strip()
    if not title:
        errors.append("Title is required.")
    elif len(title) > TITLE_MAX_LENGTH:
        errors.append(f"Title must be {TITLE_MAX_LENGTH} characters or fewer.")

    priority = form.get("priority")
    if priority not in ALLOWED_PRIORITIES:
        errors.append("Priority must be Low, Medium, or High.")

    status = form.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append("Status must be Pending, In Progress, or Completed.")

    due_date = form.get("due_date")
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Due date must be a valid date (YYYY-MM-DD).")

    return errors
