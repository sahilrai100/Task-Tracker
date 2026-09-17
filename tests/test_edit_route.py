import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Task


class EditRouteValidationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            task = Task(title='Original title', description='', priority='Medium',
                        due_date=None, status='Pending')
            db.session.add(task)
            db.session.commit()
            self.task_id = task.id

    def tearDown(self):
        with app.app_context():
            task = db.session.get(Task, self.task_id)
            if task:
                db.session.delete(task)
                db.session.commit()

    def test_invalid_submission_is_rejected_without_saving(self):
        response = self.client.post(f'/edit/{self.task_id}', data={
            'title': '',
            'description': 'desc',
            'priority': 'Urgent',
            'due_date': 'not-a-date',
            'status': 'Done',
        })

        self.assertEqual(response.status_code, 200)
        with app.app_context():
            task = db.session.get(Task, self.task_id)
            self.assertEqual(task.title, 'Original title')

    def test_valid_submission_still_updates_the_task(self):
        response = self.client.post(f'/edit/{self.task_id}', data={
            'title': 'Updated title',
            'description': 'updated desc',
            'priority': 'High',
            'due_date': '',
            'status': 'Completed',
        }, follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        with app.app_context():
            task = db.session.get(Task, self.task_id)
            self.assertEqual(task.title, 'Updated title')
            self.assertEqual(task.status, 'Completed')


if __name__ == '__main__':
    unittest.main()
