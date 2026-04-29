# samanvaya_honeypot
## Smart Honeypot + Live Attacker Intelligence Dashboard
## 📌 Overview

This project is a Smart Honeypot System that simulates a fake login portal to capture attacker behavior, analyze risk, and visualize insights through a dashboard.

Instead of authenticating users, the system:

Logs login attempts
Classifies risk levels
Detects suspicious IP activity
Displays attack analytics and geolocation
🎯 Objective

To understand attacker behavior and build a system that:

Tracks login attempts
Identifies suspicious activity
Visualizes attack patterns
Provides real-time alerts
🚀 Features
🔐 Honeypot Login System
Fake login page captures credentials
No real authentication (acts as trap)
Stores:
Username
Password
IP address
Timestamp
Risk level
## 🧠 Risk Analysis Engine

Classifies attacks into:

Level	Condition
High	Common usernames (admin, root) OR weak passwords
Medium	Password length < 6
Low	All other cases
## 🚨 Suspicious IP Detection
Tracks attempts per IP
If attempts ≥ 7 → flagged as suspicious
Displays popup alert in dashboard
## 📊 Dashboard
Total attack count
High-risk attack count
Attack logs table
Visual charts:
Pie chart (risk distribution)
Line chart (attack trends)
## 🌍 Location Tracking
Uses IP Geolocation API
Displays:
City
Country
ISP
Shows location on Google Maps
## ⚠️ Alert System
Popup alert for suspicious IPs
Banner alert for high-risk attacks
## 📥 Export Logs
Download logs as CSV file
## 🏗️ Tech Stack
Backend
Python (Flask)
SQLite3
Frontend
HTML
CSS
JavaScript
Libraries / APIs
Chart.js (visualization)
IP-API (geolocation)
Google Maps (embedded)
## 📁 Project Structure
project/
│
├── app.py
├── attacks.db
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── otp.html (optional)
│   └── riskAlert.html (optional)
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md
## ⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2️⃣ Install Dependencies
pip install flask
3️⃣ Run Application
python app.py
4️⃣ Open in Browser
http://127.0.0.1:5000
## ⚙️ How It Works
A realistic login page is presented to users (attackers/bots).
When credentials are entered, they are not verified but captured and stored.
The system logs:
Username
Password
IP address
Timestamp
Risk level
A risk analysis engine classifies each attempt as Low, Medium, or High based on suspicious patterns.
If a particular IP repeatedly attempts login (e.g., 7+ times):
It is marked as suspicious
An alert is triggered
The attacker’s IP is tracked and its geolocation is displayed on the dashboard.
All activity is visualized in a dashboard with charts, logs, and alerts.
## 🔄 System Flow
Login Page → Capture Data → Risk Analysis → Database →
IP Tracking → Dashboard → Alerts + Charts + Map
📊 Example Output
⚠️ Suspicious IP Detected
🔴 High Risk Attack Banner
📍 Location: Bangalore, India
📈 Charts showing attack trends
⚠️ Security Note
This is a simulation project
Not for production use
Lacks:
Encryption
Secure authentication
Access control
💡 Future Enhancements
Real-time updates (WebSockets)
Email/SMS alerts
AI-based threat detection
Automatic IP blocking
Heatmap visualization
Admin authentication system

## 🛡️ Working of the Project

1. **User accesses the login page**
   A fake admin login interface is displayed. It looks real but is designed as a trap (honeypot).

2. **User enters credentials**
   The user types a username and password and clicks **Login**. No real authentication is performed.

3. **Request is sent to backend (`/login`)**
   The form submits a POST request to the Flask server.

4. **System captures input data**
   Backend collects:

   * Username
   * Password
   * IP address (`request.remote_addr`)
   * Timestamp

5. **Risk analysis is performed**
   The system classifies the attempt:

   * **High** → common usernames (admin/root) or weak passwords
   * **Medium** → short password (<6)
   * **Low** → all others

6. **Data is stored in database**
   All details are saved in SQLite (`attacks.db`) as a log entry.

7. **IP attempt count is calculated**
   System checks how many times the same IP has attempted login.

8. **Suspicious behavior is detected**
   If an IP attempts login multiple times (≥ 7), it is marked as **suspicious**.

9. **Dashboard is loaded (`/dashboard`)**
   Backend sends:

   * Logs
   * Risk statistics
   * Suspicious IP data

10. **Data is visualized**
    Dashboard shows:

* Table of logs
* Pie chart (risk distribution)
* Line chart (attack trends)

11. **Alerts are triggered**

* Popup alert → for suspicious IPs
* Banner alert → for high-risk attacks

12. **Location tracking is displayed**
    When an IP is clicked:

* System fetches location using API
* Shows city, country, ISP
* Displays location on Google Map

## 🎯 Purpose
To understand how attackers behave
To detect brute-force attacks and suspicious patterns
To monitor repeated login attempts from the same IP
To simulate real-world cybersecurity defense systems

## ⭐ Key Takeaway

This project demonstrates:

Full-stack development
Cybersecurity fundamentals
Data analysis and visualization
Real-world attack simulation