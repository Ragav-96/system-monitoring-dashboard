import psutil
import mysql.connector
from datetime import datetime
import streamlit as st
import pandas as pd
from win10toast_click import ToastNotifier
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
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")      
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# MySQL connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Notifications
toaster = ToastNotifier()

# Streamlit setup
st.set_page_config(page_title="System Monitor Demo", layout="wide")
st.title("System Monitor Demo Dashboard")

# Initialize dataframe
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['timestamp', 'cpu_usage', 'memory_usage', 'disk_usage'])
if 'stop_demo' not in st.session_state:
    st.session_state.stop_demo = False

# Stop button
if st.button("Stop Demo"):
    st.session_state.stop_demo = True
    st.success("Demo stopped. You can close the browser or exit the script.")
    cursor.close()
    conn.close()

# Email alert function
def send_alert(subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER   
        msg["To"] = EMAIL_TO       
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)  # <- updated
            server.send_message(msg)
        toaster.show_toast(subject, message, duration=5, threaded=True)
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Streamlit placeholders
st.subheader("Metrics Table")
table = st.empty()
st.subheader("Metrics Chart")
chart = st.empty()

# Main loop
while not st.session_state.stop_demo:
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

    # Update Streamlit dataframe
    new_row = pd.DataFrame([[timestamp, cpu, memory, disk]],
                           columns=['timestamp', 'cpu_usage', 'memory_usage', 'disk_usage'])
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

    # Update dashboard
    table.dataframe(st.session_state.df)
    chart.line_chart(st.session_state.df.set_index('timestamp'))

    # Alerts
    if cpu > THRESHOLDS["cpu"]:
        send_alert("High CPU Usage", f"CPU: {cpu}% at {timestamp}")
    if memory > THRESHOLDS["memory"]:
        send_alert("High Memory Usage", f"Memory: {memory}% at {timestamp}")
    if disk > THRESHOLDS["disk"]:
        send_alert("High Disk Usage", f"Disk: {disk}% at {timestamp}")

    time.sleep(2)  # faster updates for demo

