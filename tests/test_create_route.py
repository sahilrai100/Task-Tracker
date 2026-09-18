import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Task


class CreateRouteValidationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_invalid_submission_is_rejected_without_saving(self):
        with app.app_context():
            before = Task.query.count()

        response = self.client.post('/create', data={
            'title': '',
            'description': 'kept description',
            'priority': 'Urgent',
            'due_date': 'not-a-date',
            'status': 'Done',
        })

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(Task.query.count(), before)

        body = response.get_data(as_text=True)
        self.assertIn('Title is required.', body)
        self.assertIn('Priority must be Low, Medium, or High.', body)
        self.assertIn('kept description', body)

    def test_valid_submission_still_creates_a_task(self):
        with app.app_context():
            before = Task.query.count()

        response = self.client.post('/create', data={
            'title': 'Test task from route test',
            'description': '',
            'priority': 'Medium',
            'due_date': '',
            'status': 'Pending',
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        with app.app_context():
            self.assertEqual(Task.query.count(), before + 1)
            task = Task.query.filter_by(title='Test task from route test').first()
            self.assertIsNotNone(task)
            db.session.delete(task)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
