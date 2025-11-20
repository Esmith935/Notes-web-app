from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Password1' # -- Cybersecurity is my passion
DATABASE = 'database.db'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -- Init db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        bodytext TEXT NOT NULL,
                        date DATETIME NOT NULL
                        )
                    ''')
        
        conn.commit()

# -------- Main -------- #

# -- Route: Home

@app.route('/')
def home():
    
    return render_template("home.html")

# -- Route: About

@app.route('/about')
def about():
    
    return render_template("about.html")

# -- Route: Notes

@app.route('/notes', methods=["GET", "POST"])
def notes():
    if request.method == "POST":
        title = request.form['title']
        bodytext = request.form['bodytext']
        currentDate = datetime.now()

        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO notes (title, bodytext, date) VALUES (?, ?, ?)', (title, bodytext, currentDate))
            conn.commit()

            return redirect(url_for('notes'))
        
    with sqlite3.connect(DATABASE) as conn:
        notes = conn.execute('SELECT * FROM notes').fetchall()
    
    return render_template("notes.html", notes=notes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)