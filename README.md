# Apartment Leasing Web App

This simple Flask application lets prospective tenants apply for an apartment online.

## Setup

1. Install dependencies (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser at `http://localhost:5000` to access the web app.

Submitted applications are stored in `applications.db` (a SQLite database) in the
project directory. Each entry records the applicant details along with the date
and time the application was submitted.
