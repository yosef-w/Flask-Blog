from app import app
from flask import render_template
from fake_data import posts

@app.route('/')
def index():
    return render_template('index.html', posts=posts, logged_in=False)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')