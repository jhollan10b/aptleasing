from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
