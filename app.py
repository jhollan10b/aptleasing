from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

DB_NAME = 'applications.db'


def init_db():
    """Ensure the applications table exists."""
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                apartment TEXT NOT NULL,
                date_submitted TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_application(data):
    """Save an application record to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    try:
        conn.execute(
            """
            INSERT INTO applications (name, email, phone, apartment, date_submitted)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data['name'],
                data['email'],
                data['phone'],
                data['apartment'],
                datetime.utcnow().isoformat(timespec='seconds'),
            ),
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving application: {e}")
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'apartment': request.form.get('apartment'),
        }
        save_application(data)
        return render_template('thanks.html', name=data['name'])
    return render_template('apply.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
    """Handle the step-by-step leasing process."""
    step = int(request.args.get('step', 1))
    if 'process_data' not in session:
        session['process_data'] = {}
    data = session['process_data']

    if request.method == 'POST':
        if step == 1:
            data['email'] = request.form.get('email')
        elif step == 2:
            data['num_people'] = request.form.get('num_people')
            data['move_in'] = request.form.get('move_in')
            data['pets'] = request.form.get('pets')
            data['job'] = request.form.get('job')
            data['budget'] = request.form.get('budget')
        elif step == 3:
            data['appointment'] = request.form.get('appointment')
        elif step == 4:
            data['name'] = request.form.get('name')
            data['phone'] = request.form.get('phone')
            data['apartment'] = request.form.get('apartment')
            save_application(
                {
                    'name': data['name'],
                    'email': data.get('email', ''),
                    'phone': data['phone'],
                    'apartment': data['apartment'],
                }
            )
        session['process_data'] = data
        next_step = step + 1
        return redirect(url_for('process', step=next_step))

    if step > 10:
        step = 10
    return render_template('process.html', step=step, data=data)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
