from flask import Flask, render_template, request, redirect, url_for, Response, session
import sqlite3
from datetime import datetime
import random
import csv
import io
import requests   # ✅ FIXED (missing)

app = Flask(__name__)
app.secret_key = "secret123"

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
    
    if username and username.lower() in common_users:
        return "High"
    elif password and password in weak_passwords:
        return "High"
    elif password and len(password) < 6:
        return "Medium"
    return "Low"

# ---------------- RANDOM IP ----------------
def random_ip():
    sample_ips = [
        "8.8.8.8",
        "1.1.1.1",
        "142.250.183.78",
        "185.199.108.153",
        "13.127.0.1"
    ]
    return random.choice(sample_ips)

# ---------------- ALERT FUNCTION ----------------
def send_alert(ip, attempts):
    try:
        res = requests.get(f"https://ip-api.com/json/{ip}").json()

        city = res.get("city", "Unknown")
        country = res.get("country", "Unknown")

        print("\n⚠️ ALERT: Suspicious Activity Detected")
        print(f"IP: {ip}")
        print(f"Location: {city}, {country}")
        print(f"Attempts: {attempts}\n")

    except:
        print("Error fetching location")

# ---------------- ROUTES ----------------

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_attempt():
    username = request.form.get('username')
    password = request.form.get('password')

    # 🔥 Use fixed IP for demo (IMPORTANT)
    ip_addr = request.remote_addr

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    risk = analyze_risk(username, password)

    conn = sqlite3.connect('attacks.db')
    cursor = conn.cursor()

    # Insert log
    cursor.execute('''
        INSERT INTO logs (username, password, ip_address, timestamp, risk_level)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, ip_addr, timestamp, risk))
    conn.commit()

    # 🔥 Count attempts
    cursor.execute('SELECT COUNT(*) FROM logs WHERE ip_address = ?', (ip_addr,))
    attempts = cursor.fetchone()[0]

    # 🔥 Trigger alert
    if attempts >= 7:
        send_alert(ip_addr, attempts)

    conn.close()

    # ---------------- RISK FLOW ----------------
    import time

    if risk == "High":
        time.sleep(2)  # simulate security check
        return render_template(
        "login.html",
        error="Processing request... Please wait.",
        retry="Try again after some time."
    )

    elif risk == "Medium":
        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        return render_template("otp.html", otp=otp)

    else:
        return render_template("welcome.html")

# ---------------- OTP ----------------
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_otp = request.form.get("otp")

    if not session.get("otp"):
        return render_template("login.html", error="Session expired. Try again.")

    if user_otp == session.get("otp"):
        session.pop("otp", None)
        return render_template("welcome.html")
    else:
        return render_template("otp.html", otp=session.get("otp"), error="Invalid OTP")

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('attacks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM logs ORDER BY id DESC')
    logs = cursor.fetchall()

    cursor.execute('SELECT risk_level, COUNT(*) FROM logs GROUP BY risk_level')
    stats = dict(cursor.fetchall())
    # 🔥 NEW: Find suspicious IPs (>= 7 attempts)
    cursor.execute('''
    SELECT ip_address, COUNT(*) as attempts
    FROM logs
    GROUP BY ip_address
    HAVING attempts >= 7
''')

    suspicious_ips = cursor.fetchall()

    conn.close()

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
        high=high,
        suspicious_ips=suspicious_ips   # ✅ IMPORTANT
    )

# ---------------- CSV DOWNLOAD ----------------
@app.route('/download')
def download_csv():
    conn = sqlite3.connect('attacks.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, password, ip_address, timestamp, risk_level 
        FROM logs ORDER BY id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['Username', 'Password', 'IP Address', 'Timestamp', 'Risk Level'])
    writer.writerows(rows)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=honeypot_logs.csv"}
    )

# ---------------- RUN ----------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)