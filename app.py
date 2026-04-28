from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('attacks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            ip_address TEXT,
            timestamp TEXT,
            risk_level TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ---------------- RISK ANALYSIS ----------------
def analyze_risk(username, password):
    common_users = ['admin', 'root', 'administrator', 'superuser']
    weak_passwords = ['123456', 'password', 'admin123', '12345']
    
    if username.lower() in common_users or password in weak_passwords:
        return "High"
    elif len(password) < 6:
        return "Medium"
    return "Low"
# ✅ ADD HERE
def random_ip():
    sample_ips = [
        "8.8.8.8",        # USA
        "1.1.1.1",        # Cloudflare
        "142.250.183.78", # Google
        "185.199.108.153",# GitHub
        "13.127.0.1"      # India (AWS)
    ]
    return random.choice(sample_ips)
# ---------------- ROUTES ----------------
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_attempt():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_addr = random_ip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    risk = analyze_risk(username, password)

    conn = sqlite3.connect('attacks.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (username, password, ip_address, timestamp, risk_level)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, ip_addr, timestamp, risk))
    conn.commit()
    conn.close()

    return render_template('login.html', error="Invalid system credentials. Access Denied.")

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('attacks.db')
    cursor = conn.cursor()

    # Get logs
    cursor.execute('SELECT * FROM logs ORDER BY id DESC')
    logs = cursor.fetchall()

    # Risk counts
    cursor.execute('SELECT risk_level, COUNT(*) FROM logs GROUP BY risk_level')
    stats = dict(cursor.fetchall())

    conn.close()

    # -------- FIXED PART (IMPORTANT) --------
    labels = ["Low", "Medium", "High"]
    values = [
        stats.get("Low", 0),
        stats.get("Medium", 0),
        stats.get("High", 0)
    ]

    total = sum(values)
    high = stats.get("High", 0)

    return render_template(
        'dashboard.html',
        logs=logs,
        labels=labels,
        values=values,
        total=total,
        high=high
    )

# ---------------- RUN ----------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)