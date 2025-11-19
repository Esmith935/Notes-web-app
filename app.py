from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.secret_key = 'Password1' # -- Cybersecurity is my passion
DATABASE = 'database.db'

# -- Init db

def init_db():
    pass

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

@app.route('/notes')
def notes():
    
    return render_template("notes.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)