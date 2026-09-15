import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validation import validate_task_data


def base_form(**overrides):
    form = {
        "title": "Write report",
        "description": "",
        "priority": "Medium",
        "due_date": "",
        "status": "Pending",
    }
    form.update(overrides)
    return form


class ValidateTaskDataTests(unittest.TestCase):
    def test_valid_form_has_no_errors(self):
        self.assertEqual(validate_task_data(base_form()), [])

    def test_missing_title_is_rejected(self):
        errors = validate_task_data(base_form(title=""))
        self.assertIn("Title is required.", errors)

    def test_whitespace_only_title_is_rejected(self):
        errors = validate_task_data(base_form(title="   "))
        self.assertIn("Title is required.", errors)

    def test_title_over_max_length_is_rejected(self):
        errors = validate_task_data(base_form(title="x" * 121))
        self.assertIn("Title must be 120 characters or fewer.", errors)

    def test_title_at_max_length_is_accepted(self):
        errors = validate_task_data(base_form(title="x" * 120))
        self.assertEqual(errors, [])

    def test_invalid_priority_is_rejected(self):
        errors = validate_task_data(base_form(priority="Urgent"))
        self.assertIn("Priority must be Low, Medium, or High.", errors)

    def test_invalid_status_is_rejected(self):
        errors = validate_task_data(base_form(status="Done"))
        self.assertIn("Status must be Pending, In Progress, or Completed.", errors)

    def test_valid_due_date_is_accepted(self):
        errors = validate_task_data(base_form(due_date="2026-12-31"))
        self.assertEqual(errors, [])

    def test_empty_due_date_is_accepted(self):
        errors = validate_task_data(base_form(due_date=""))
        self.assertEqual(errors, [])

    def test_malformed_due_date_is_rejected(self):
        errors = validate_task_data(base_form(due_date="31-12-2026"))
        self.assertIn("Due date must be a valid date (YYYY-MM-DD).", errors)

    def test_multiple_errors_are_all_reported(self):
        errors = validate_task_data(
            base_form(title="", priority="Urgent", status="Done", due_date="not-a-date")
        )
        self.assertEqual(len(errors), 4)


if __name__ == "__main__":
    unittest.main()
