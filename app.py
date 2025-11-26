from select import select
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Password1' # -- Cybersecurity is my passion
DATABASE = 'database.db'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -- Init db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        bodytext TEXT NOT NULL,
                        date DATETIME NOT NULL,
                        avatar TEXT
                        )
                    ''')
        
        conn.commit()

# -------- Main -------- #

# -- Route: Home

@app.route('/')
def home():
    # Fetch the most recent note to display on home page
    with sqlite3.connect(DATABASE) as conn:
        recent_note = conn.execute('SELECT * FROM notes ORDER BY date DESC LIMIT 1').fetchone()
    
    return render_template("home.html", recent_note=recent_note)

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
        avatar = request.files.get('avatar')
        avatar_filename = None
        currentDate = datetime.now()

        if avatar and allowed_file(avatar.filename):
            filename = secure_filename(avatar.filename)
            avatar_filename = f"{title}_{filename}"
            avatar.save(os.path.join(UPLOAD_FOLDER, avatar_filename))

        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO notes (title, bodytext, date, avatar) VALUES (?, ?, ?, ?)', (title, bodytext, currentDate, avatar_filename))
            conn.commit()

            return redirect(url_for('notes'))
        
    with sqlite3.connect(DATABASE) as conn:
        notes = conn.execute('SELECT * FROM notes').fetchall()
    
    return render_template("notes.html", notes=notes)

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    with sqlite3.connect(DATABASE) as conn:

        note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone
        conn.commit()

        if not note_id:
            return 'note not found', 404
        
        if request.method == 'POST':
            title = request.form['title']
            bodytext = request.form['bodytext']

            
            conn.execute('UPDATE notes SET title = ?, bodytext = ? WHERE id = ?', (title, bodytext, note_id))
            conn.commit()
            
            return redirect(url_for('notes'))
    
    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:note_id>', methods=['GET', 'POST'])
def delete_note(note_id):
    if request.method == "POST":
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
            conn.commit()
        return redirect(url_for('notes'))
    
    return render_template('delete_note.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)