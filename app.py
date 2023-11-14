from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# generic error message, ideas from CS50 Finance
def error(message):
    return render_template("error.html", message=message)

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///eventtracker.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# credits to CS50 Finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    # return index page
    return render_template("index.html")
    # index page right buttons will display either logout or register/login depending on whether logged in

@app.route("/login", methods=["GET", "POST"])
# credits to CS50 finance
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("invalid input")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("invalid input")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("incorrect password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    # user submitted form:
    if request.method == "POST":

        # make sure all fields filled out
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return error("invalid input")

        # check pw matches
        if request.form.get("password") != request.form.get("confirmation"):
            return error("password does not match")

        # check if username in database
        usernames = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if len(usernames) == 0:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
            return render_template("login.html")

        else:
            return error("username in use")

    # if no form submitted
    return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
def add():

    # check if user logged in
    if not session.get("user_id"):
        return render_template("login.html")

    eventtype =[
        'health',
        'finance',
        'productivity',
        'celebrations',
        'hobbies',
        'misc'
    ]

    # request method always post, check all fields filled
    if not request.form.get("datetime") or not request.form.get("details") or not request.form.get("eventtype") or request.form.get("eventtype") not in eventtype:
        return error("invalid input")

    # insert event into events table
    db.execute("INSERT INTO events (user_id, event_time, activity, event_type) VALUES (?,?,?,?)", session.get("user_id"), request.form.get("datetime"), request.form.get("details"), request.form.get("eventtype"))
    return redirect("/")

@app.route("/upcoming")
def upcoming():

    # check if user logged in
    if not session.get("user_id"):
        return render_template("login.html")

    # give table of upcoming events (columns = date, type, details)
    events = db.execute("SELECT event_time, activity, event_type FROM events WHERE user_id = ? AND event_time >= CURRENT_TIMESTAMP AND event_time <= DATE('NOW', '+7 DAY') ORDER BY event_time ASC", session.get("user_id"))
    return render_template("upcoming.html", events=events)

@app.route("/track")
def track():

    # check if user logged in
    if not session.get("user_id"):
        return render_template("login.html")

    return render_template("track.html")

@app.route("/trackbytype", methods=["GET", "POST"])
def trackbytype():

    health = db.execute("SELECT * FROM events WHERE user_id = ? AND event_type = 'health' ORDER BY event_time ASC", session.get("user_id"))
    finance = db.execute("SELECT * FROM events WHERE user_id = ? AND event_type = 'finance' ORDER BY event_time ASC", session.get("user_id"))
    productivity = db.execute("SELECT * FROM events WHERE user_id = ? AND event_type = 'productivity' ORDER BY event_time ASC", session.get("user_id"))
    celebrations = db.execute("SELECT * FROM events WHERE user_id = ? AND event_type = 'celebrations' ORDER BY event_time ASC", session.get("user_id"))
    hobbies = db.execute("SELECT * FROM events WHERE user_id = ? AND event_type = 'hobbies' ORDER BY event_time ASC", session.get("user_id"))
    misc = db.execute("SELECT * FROM events WHERE user_id = ? AND event_type = 'misc' ORDER BY event_time ASC", session.get("user_id"))

    return render_template("trackbytype.html", health=health, finance=finance, productivity=productivity, celebrations=celebrations, hobbies=hobbies, misc=misc)

@app.route("/trackbydate", methods=["GET", "POST"])
def trackbydate():

    if request.method == "POST":
        #check valid date
        if not request.form.get("date"):
            return error("invalid input")

        events = db.execute("SELECT * FROM events WHERE user_id = ? AND DATE(event_time) = ? ORDER BY event_time ASC", session.get("user_id"), request.form.get("date"))
        return render_template("trackedbydate.html", events=events)

    return render_template("trackbydate.html")


