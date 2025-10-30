from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20))  # Low, Medium, High
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20))  # Pending, In Progress, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.title}>"

# Flask 3.x-compatible table creation
with app.app_context():
    db.create_all()

# Smart Insight Generator
def generate_insight(tasks):
    if not tasks:
        return "No tasks yet. You have a clean slate! 🎉"

    total = len(tasks)
    high = sum(1 for t in tasks if t.priority == 'High')
    upcoming = sum(1 for t in tasks if t.due_date and t.due_date <= datetime.utcnow().date() + timedelta(days=7))
    completed = sum(1 for t in tasks if t.status == 'Completed')

    busy_msg = (
        "This week looks busy 📅 — " if upcoming > 3 else
        "You have a manageable week ahead 👍 — " if upcoming > 0 else
        "Relaxed week, no upcoming deadlines 😌 — "
    )
    focus = f"{high} out of {total} tasks are high priority. "
    progress = f"You’ve completed {completed}/{total} tasks so far."

    return busy_msg + focus + progress

# Routes
@app.route('/')
def index():
    sort_by = request.args.get('sort', 'due_date')
    filter_status = request.args.get('status', 'all')

    query = Task.query
    if filter_status != 'all':
        query = query.filter_by(status=filter_status)

    if sort_by == 'priority':
        query = query.order_by(Task.priority.desc())
    elif sort_by == 'title':
        query = query.order_by(Task.title)
    else:
        query = query.order_by(Task.due_date.asc().nulls_last())

    tasks = query.all()
    insight = generate_insight(tasks)
    return render_template('index.html', tasks=tasks, insight=insight, sort_by=sort_by, filter_status=filter_status)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None

        task = Task(title=title, description=desc, priority=priority, due_date=due_date_obj, status=status)
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        due_date = request.form['due_date']
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
        task.status = request.form['status']
        db.session.commit()
        flash('Task updated successfully!', 'info')
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
