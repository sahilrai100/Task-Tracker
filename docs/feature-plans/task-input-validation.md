# Feature: Task input validation with clear error messages
Status: in-progress
Repo: Task-Tracker
Started: 2026-09-15

## Why
The README lists "Validation is melty (needs better checks for fields)" as a
known issue. Right now the create/edit forms only rely on the browser's
`required` attribute on the title field, which is easy to bypass (disabled
JS, a raw POST, or an empty-after-whitespace title). An empty or garbage
task then lands silently in the list with no way to tell the user what went
wrong. Server-side validation with a clear, specific error message lets
users fix their input instead of getting a confusing blank/broken row.

## Design
- New pure module `validation.py`: `validate_task_data(form)` takes the raw
  form dict and returns a list of human-readable error strings (empty list
  = valid). No Flask/DB imports, so it is unit-testable in isolation.
- Rules: title required (non-empty after strip, <=120 chars to match the DB
  column), priority must be one of Low/Medium/High, status must be one of
  Pending/In Progress/Completed, due_date (if provided) must parse as
  YYYY-MM-DD.
- `/create` and `/edit/<id>` call `validate_task_data` before touching the
  DB. On errors, re-render the same form with the error list and the
  values the user typed (so nothing is lost), instead of saving or
  crashing. On success, behavior is unchanged.
- Templates gain a small reusable error block (list of `alert-danger`
  items) at the top of the form.
- Edge cases covered: empty/whitespace-only title, title over 120 chars,
  unexpected priority/status values (e.g. tampered `<select>` on the
  client), malformed due_date.

## Steps
- [x] 1. Add `validation.py` with `validate_task_data()` plus unit tests in `tests/test_validation.py` (stdlib `unittest`, no new dependency). (done 2026-09-15)
- [x] 2. Wire validation into the `/create` route: reject invalid submissions, re-render `create.html` with errors and the submitted values. (done 2026-09-16)
- [ ] 3. Wire validation into the `/edit/<id>` route the same way, re-rendering `edit.html` on error.
- [ ] 4. Update `create.html` and `edit.html` to display the error list and preserve submitted values on a failed submission.
- [ ] 5. Update the README: remove "Validation is melty" from Known issues and add a short Validation section describing the rules.

## Notes
