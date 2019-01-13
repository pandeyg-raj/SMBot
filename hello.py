import sqlite3
from helpers import apology, login_required
from werkzeug.exceptions import default_exceptions
from tempfile import mkdtemp
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
app = Flask(__name__)

# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def hello():
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    portDatas = db.execute("select * from employees")
    portData = portDatas.fetchall()
    print(portData)
    return "Hello jhsdgjWorld!"

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == 'GET':
        return render_template("admin.html")
    # Forget any user_id
    session.clear()
    USER = "admin"
    PASSWORD = "India@123"
    if(USER == request.form.get("Uname") and PASSWORD == request.form.get("Password")):
        # Remember which user has logged in
        session["user_id"] = request.form.get("Uname")
        session["user_name"] = request.form.get("Password")
        return render_template("dashboard.html")
    return apology("TODO",12)

@app.route("/manageTeams", methods=["GET", "POST"])
@login_required
def manageTeams():
    return render_template("manageTeams.html")

@app.route("/manageScrums", methods=["GET", "POST"])
@login_required
def manageScrums():
    return render_template("manageScrums.html")

@app.route("/manageNotifications", methods=["GET", "POST"])
def manageNotifications():
    return render_template("manageNotifications.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run()
