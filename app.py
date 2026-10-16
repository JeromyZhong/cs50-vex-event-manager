import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///events.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        name = request.form.get("name")
        date = request.form.get("date")
        place = request.form.get("place")

        print("name="+name + " place=")

        if not name and not date and not place:
           events = []
           return render_template("index.html", events=events)

        elif name and not date and not place:
            sqlstat = "SELECT * FROM events where name like '%" + name + "%'"
            events = db.execute(sqlstat)

        elif date and not name and not place:
            sqlstat = "SELECT * FROM events where date = '" + date + "'"
            events = db.execute(sqlstat)

        elif place and not name and not date:
            sqlstat = "SELECT * FROM events where place like '%" + place + "%'"
            events = db.execute(sqlstat)

        elif name and date and not place:
            sqlstat = "SELECT * FROM events where name like '%" + name + "%' and date = '" + date + "'"
            events = db.execute(sqlstat)

        elif name and place and not date:
            sqlstat = "SELECT * FROM events where name like '%" + name + "%' and place like '%" + place + "%'"
            events = db.execute(sqlstat)

        elif date and place and not name:
            sqlstat = "SELECT * FROM events where date = '" + date + "' and place like '%" + place + "%'"
            events = db.execute(sqlstat)

        else:
            sqlstat = "SELECT * FROM events where name like '%" + name + "%' and date = '" + date + "' and place like '%" + place + "%'"
            events = db.execute(sqlstat)

        return render_template("index.html", events=events)

    else:
        events = []
        return render_template("index.html", events=events)

@app.route("/manage_events", methods=["GET", "POST"])
def manage_events():
    if request.method == "POST":

        name = request.form.get("name")
        date = request.form.get("date")
        place = request.form.get("place")

        db.execute("INSERT INTO events (name, date, place) VALUES(?, ?, ?)", name, date, place)

        return redirect("/")

    else:
        return render_template("manage_events.html")

@app.route("/edit_events", methods=["GET", "POST"])
def edit_events():

    if request.method == "POST":

        name = request.form.get("input_name")

        events = db.execute("SELECT * FROM events where name like '%" + name + "%'")

        return render_template("manage_events.html", events=events)

    else:
        events = []
        return render_template("manage_events.html", events=events)

@app.route("/update_event", methods=["GET", "POST"])
def update_event():
    if request.method == "POST":

        name = request.form.get("name_change")
        date = request.form.get("date_change")
        place = request.form.get("place_change")

        db.execute("UPDATE events SET date = ? , place = ? where name = ?", date, place, name)

        return redirect("/")

    else:
        return render_template("manage_events.html")
