from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

def save_application(data, filename='applications.csv'):
    fieldnames = ['name', 'email', 'phone', 'apartment']
    try:
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        print(f"Error saving application: {e}")

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
    app.run(host='0.0.0.0', port=5000)
