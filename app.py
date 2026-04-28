import random
import time
from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create database
def init_db():
    con = sqlite3.connect("attacks.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attacks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        username TEXT,
        password TEXT,
        time TEXT,
        risk TEXT
    )
    """)
    con.commit()
    con.close()

init_db()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    ip = request.remote_addr
    time = datetime.now()

    # Risk logic
    score = 0

    if username in ["admin", "root"]:
        score += 2

    if password in ["123456", "password"]:
        score += 2

    con = sqlite3.connect("attacks.db")
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM attacks WHERE ip=?", (ip,))
    attempts = cur.fetchone()[0]

    if attempts > 5:
        score += 3

    if score >= 6:
        risk = "HIGH"
    elif score >= 3:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    cur.execute("INSERT INTO attacks(ip,username,password,time,risk) VALUES(?,?,?,?,?)",
                (ip, username, password, str(time), risk))

    con.commit()
    con.close()

    messages = [
    "Invalid Credentials",
    "Incorrect username or password",
    "Login failed. Try again",
    "Too many attempts, try later"
]

    message = random.choice(messages)

    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    con = sqlite3.connect("attacks.db")
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM attacks")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attacks WHERE risk='HIGH'")
    high = cur.fetchone()[0]

    cur.execute("SELECT * FROM attacks ORDER BY id DESC LIMIT 10")
    logs = cur.fetchall()

    con.close()

    return render_template("dashboard.html", total=total, high=high, logs=logs)

app.run(debug=True)