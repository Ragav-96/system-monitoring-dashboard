import warnings
warnings.filterwarnings("ignore")  # suppress unnecessary warnings

import psutil
import mysql.connector
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import random
import time
from dotenv import load_dotenv
import os

# ---------------- CONFIG ----------------
THRESHOLDS = {"cpu": 10, "memory": 10, "disk": 10}  # low thresholds for demo

# Load credentials from .env file
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# MySQL connection
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)
cursor = conn.cursor()

# Email alert function
def send_alert(subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Alert sent: {subject}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Main loop
try:
    while True:
        # Simulate metrics with random spikes
        cpu = random.randint(5, 100)
        memory = random.randint(5, 100)
        disk = random.randint(5, 100)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert into MySQL
        cursor.execute(
            "INSERT INTO metrics (timestamp, cpu_usage, memory_usage, disk_usage) VALUES (%s,%s,%s,%s)",
            (timestamp, cpu, memory, disk)
        )
        conn.commit()

        # Print metrics to console (optional)
        print(f"{timestamp} | CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%")

        # Alerts
        if cpu > THRESHOLDS["cpu"]:
            send_alert("High CPU Usage", f"CPU: {cpu}% at {timestamp}")
        if memory > THRESHOLDS["memory"]:
            send_alert("High Memory Usage", f"Memory: {memory}% at {timestamp}")
        if disk > THRESHOLDS["disk"]:
            send_alert("High Disk Usage", f"Disk: {disk}% at {timestamp}")

        time.sleep(2)  # faster updates for demo

except KeyboardInterrupt:
    print("Monitoring stopped by user.")
finally:
    cursor.close()
    conn.close()



