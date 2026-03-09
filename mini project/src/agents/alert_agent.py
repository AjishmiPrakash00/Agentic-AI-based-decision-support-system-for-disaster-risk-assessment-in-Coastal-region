import os
from datetime import datetime

def create_alert_message(month, rainfall, risk):
    message = f"""
==============================
🚨 FLOOD ALERT 🚨
==============================

Month: {month}
Predicted Rainfall: {rainfall} mm
Flood Risk Level: {risk}

Recommended Action:
Prepare flood control and emergency response systems.
"""
    return message

def log_alert(message):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, "..", "..", "data", "alert_log.txt")
    
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        file.write(message)

def send_alert(month, rainfall, risk):
    message = create_alert_message(month, rainfall, risk)

    # Print alert
    print(message)

    # Save alert to log file
    log_alert(message)
