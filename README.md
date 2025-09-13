# System Monitor Project

**A real-time system monitoring tool** built for the System Engineer role.  
It collects CPU, memory, and disk usage, logs them to a MySQL database, and provides alerts via email and a live dashboard.

---

## **Features**

- Real-time system metrics collection (CPU, Memory, Disk)
- Metrics logging into MySQL database
- Email alerts when thresholds are crossed
- Streamlit dashboard for visualization
- Easy demo mode with simulated metrics for presentations

---

## **Tools & Libraries**

- Python 3.12
- MySQL
- Streamlit
- Pandas
- psutil
- smtplib
- python-dotenv

---

## **Project Structure**

system-monitor-project #File Name

|- log_system_metrics.py # Main script to collect metrics & send alerts

|- dashboard.py # Streamlit dashboard for visualization

|- .env.example # Template for environment variables

|- requirements.txt # Required Python packages

|- README.md # Project documentation

---        

## **Setup Instructions**

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/system-monitor-project.git
cd system-monitor-project

2. **Create a virtual environment** (recommended)**
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

**3. Install dependencies**
pip install -r requirements.txt

**4.Create .env file based on .env.example with your credentials:**
EMAIL_USER = your_email@gmail.com
EMAIL_PASSWORD = your_app_password
EMAIL_TO = receiver_email@gmail.com
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587

DB_HOST = localhost
DB_USER = sysuser
DB_PASS = mypassword
DB_NAME = system_monitor

**5.Start MySQL and ensure the metrics table exists:**
CREATE TABLE metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    disk_usage FLOAT
);

**How to Run**

**1. Run metrics logging script**
python log_system_metrics.py
Logs metrics to MySQL
Sends email alerts if thresholds are exceeded

**2. Run the Streamlit dashboard**
streamlit run dashboard.py
Open the browser to view live metrics
Stop demo mode using the Stop Demo button

**Notes for Presentation**
Use demo mode to simulate metrics for live demo
Thresholds are configurable in the .env file
No sensitive information (passwords) should be committed to GitHub

                            
