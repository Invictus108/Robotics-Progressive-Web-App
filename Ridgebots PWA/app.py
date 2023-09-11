import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

#dict maker
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
db1 = sqlite3.connect("finance.db", check_same_thread=False)
db1.row_factory = dict_factory
db = db1.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # render template with needed info
    return render_template("index.html") 


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        rows = db.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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

def get(method, page, date):
    if method == "POST":
        id = request.form.get("item_id")

        db.execute("SELECT admin FROM users WHERE id = ?", [str(session["user_id"])])
        admin = db.fetchone()['admin']

        if admin is None:
            admin = 0

        if admin:
            db.execute(f"DELETE FROM {page} WHERE id = ?", [id])
            db1.commit()

            if date:
                sql = f"SELECT * FROM {page} ORDER BY date DESC"
            else:
                sql = f"SELECT * FROM {page}"

            db.execute(sql)
            info = db.fetchall()

            return render_template(f"{page}.html", info=info)
    
        else:
            return apology("You are not a admin")
    

    else:
        if date:
            sql = f"SELECT * FROM {page} ORDER BY date DESC"
        else:
            sql = f"SELECT * FROM {page}"

        db.execute(sql)
        info = db.fetchall()
        return render_template(f"{page}.html", info=info)

def add(method, page, first, second, third, fourth, date):
    if method == "POST":
        one = request.form.get(first)
        two = request.form.get(second)
        three = request.form.get(third)
        four = request.form.get(fourth)

        if four is None:
            four = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        db.execute("SELECT admin FROM users WHERE id = ?", [str(session["user_id"])])
        admin = db.fetchone()['admin']

        if admin is None:
            admin = 0

        sql = f"INSERT INTO {page} ({first}, {second}, {third}, {fourth}) VALUES (?,?,?,?)"

        if admin:
            db.execute(sql, [one, two, three, four])
            db1.commit()

            if date:
                sql = f"SELECT * FROM {page} ORDER BY date DESC"
            else:
                sql = f"SELECT * FROM {page}"

            db.execute(sql)
            info = db.fetchall()

            return render_template(f"{page}.html", info=info)
            

        else:
            db.execute("INSERT INTO admin (page, command, data_one, data_two, data_three, data_four) VALUES (?,?,?,?,?,?)", [page, sql, one, two, three, four])
            db1.commit()
            return render_template("request.html")
            
        

    else:
        return render_template(f"{page}_add.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # get data from form
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # make sure all fields exist
        if not username or not password or not confirm_password:
            return apology("Please fill in all fields")

        # check if confirmation matches password
        if confirm_password != password:
            return apology("Make sure both passwords are identical")

        # check if useranme taken
        db.execute("SELECT * FROM users WHERE username=?", [username])
        if db.fetchone() != None:
            return apology("Username already taken")

        # genrate password hash
        password = generate_password_hash(password)

        # insert username and password into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", [username, password])
        db1.commit()

        # log user in
        db.execute("SELECT * FROM users WHERE username = ?", [username])
        rows = db.fetchone()
        session["user_id"] = rows

        return redirect("/")

    else:
        return render_template("register.html")
    
@app.route("/score")
@login_required
def score():
    return render_template("score.html")

@app.route("/records", methods=["GET", "POST"])
@login_required
def records():
    return get(request.method, "records", True)

@app.route("/records_add", methods=["GET", "POST"])
@login_required
def records_add():
    return add(request.method, "records", "blue", "red", "score", "date", True)

@app.route("/team_todo", methods=["GET", "POST"])
@login_required
def team_todo():
    return get(request.method, "team_todo", True)

@app.route("/team_todo_add", methods=["GET", "POST"])
@login_required
def team_todo_add():
    return add(request.method, "team_todo", "task", "description", "date", "person", True)

@app.route("/personal_todo", methods=["GET", "POST"])
@login_required
def personal_todo():
    if request.method == "POST":
        id = request.form.get("item_id")

        db.execute("DELETE FROM personal_todo WHERE id = ?", [id])
        db1.commit()

        db.execute("SELECT * FROM personal_todo WHERE username = ? ORDER BY date DESC", [str(session["user_id"])])
        info = db.fetchall()

        return render_template("personal_todo.html", info=info)
    

    else:
        db.execute("SELECT * FROM personal_todo WHERE username = ?", [str(session["user_id"])])
        info = db.fetchall()
        return render_template("personal_todo.html", info=info)
    
@app.route("/personal_todo_add", methods=["GET", "POST"])
@login_required
def personal_todo_add():
    if request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        goal = request.form.get("goal")

        sql = "INSERT INTO personal_todo (username, task, description, goal) VALUES (?,?,?,?)"
   
        db.execute(sql, [str(session["user_id"]), task, description, goal])
        db1.commit()

        db.execute("SELECT * FROM personal_todo WHERE username = ? ORDER BY date DESC", [str(session["user_id"])])
        info = db.fetchall()

        return render_template("personal_todo.html", info=info)  

    else:
        return render_template("personal_todo_add.html")


@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    return get(request.method, "calendar", True)
    
@app.route("/calendar_add", methods=["GET", "POST"])
@login_required
def calendar_add():
    return add(request.method, "calendar", "event", "address", "date", "time", True)

@app.route("/roster", methods=["GET", "POST"])
@login_required
def roster():
    return get(request.method, "roster", False)

@app.route("/roster_add", methods=["GET", "POST"])
@login_required
def roster_add():
   return add(request.method, "roster", "name", "grade", "email", "position", False)
    
@app.route("/parts", methods=["GET", "POST"])
@login_required
def parts():
    return get(request.method, "parts", False)
    
@app.route("/parts_add", methods=["GET", "POST"])
@login_required
def parts_add():
    return add(request.method, "parts", "part", "link", "amount", "price", False)

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":
        add_id = request.form.get("add_item_id")
        remove_id = request.form.get("remove_item_id")

        if remove_id:
            db.execute("DELETE FROM admin WHERE id = ?", [remove_id])
            db1.commit()

            db.execute("SELECT * FROM admin")
            info = db.fetchall()

            return render_template("admin.html", info=info)
        
        if add_id:
            db.execute("SELECT * FROM admin WHERE id = ?", [add_id])
            row = db.fetchone()

            if row is not None:
                command = row["command"]
                data_one = row["data_one"]
                data_two = row["data_two"]
                data_three = row["data_three"]
                data_four = row["data_four"]

            db.execute(command, [data_one, data_two, data_three, data_four])

            db.execute("DELETE FROM admin WHERE id = ?", [add_id])
            db1.commit()

            db.execute("SELECT * FROM admin")
            info = db.fetchall()

            return render_template("admin.html", info=info)
            
            

    else:
        db.execute("SELECT admin FROM users WHERE id = ?", [str(session["user_id"])])
        admin = db.fetchone()['admin']

        if admin:
            db.execute("SELECT * FROM admin")
            info = db.fetchall()
            
            return render_template("admin.html", info=info)
        
        else:
            return apology("You are not a admin")

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":

        # get data from form
        password = request.form.get("password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirmation")

        # get password from data base
        db.execute("SELECT hash FROM users WHERE id = ?", [str(session["user_id"])])
        data = db.fetchone()

        # check if password is correct
        if not check_password_hash(data["hash"], password):
            return apology("Incorrect password")

        # check if new password equals confirmation
        if new_password != confirm_password:
            return apology("Confirmation needs the match new password")

        # generate password hash
        password_hash = generate_password_hash(new_password)

        # update password
        db.execute("UPDATE users SET hash=? WHERE id=?", [password_hash, str(session["user_id"])])
        db1.commit()

        return redirect("/")

    else:
        return render_template("password.html")







   