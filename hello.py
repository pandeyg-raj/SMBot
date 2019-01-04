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

@app.route("/addmember", methods=["GET", "POST"])
#@login_required
def addmember():
    if request.method == 'GET':
        return render_template("addmember.html")
    conn = sqlite3.connect('database.db')
    db = conn.cursor()

    db.execute("INSERT INTO employees(sap_id,first_name,last_name,mail_id) VALUES (?,?,?,?) ",
                (request.form.get("sapId"),request.form.get("fName"),request.form.get("lName"),request.form.get("eMail")))
    conn.commit()
    conn.close()
    return apology("Sucess",200)

@app.route("/removemember", methods=["GET", "POST"])
#@login_required
def removemember():
    if request.method == 'GET':
        return render_template("removemember.html")
    conn = sqlite3.connect('database.db')
    db = conn.cursor()
    print("sapId")
    print(request.form.get("sapId"))
    SAPID = (request.form.get("sapId"),)
    db.execute("SELECT sap_id FROM employees where sap_id = ?",SAPID)
    data=db.fetchone()
    if data is None:
        print('There is no component named %s'%SAPID)
        return apology("There is no component",9999)
    else:
        db.execute("DELETE from employees where sap_id = ?",SAPID)
        conn.commit()
    conn.close()
    return apology("Sucess",200)

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run()
