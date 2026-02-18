import subprocess
import csv
import json
import time
from datetime import datetime
from collections import Counter

CALL_LOG_FILE = "call_log.csv"
SMS_LOG_FILE = "sms_log.csv"
FLOOD_THRESHOLD = 3  # adjust as needed
SLEEP_INTERVAL = 10  # seconds between checks

# Logging functions
def log_call(number):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CALL_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([number, now])

def log_sms(number, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SMS_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([number, now, message])

def export_json(log_file, json_file):
    data = []
    with open(log_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                data.append(row)
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

# Flood detection
def detect_flood(log_file, threshold=FLOOD_THRESHOLD):
    numbers = []
    with open(log_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                numbers.append(row[0])
    counter = Counter(numbers)
    return [num for num, count in counter.items() if count >= threshold]

# Real-time monitoring loop
def monitor():
    print("📲 Defensive SMS/Call Logger started (Press Ctrl+C to stop)")
    while True:
        # Fetch incoming calls
        try:
            calls = subprocess.check_output(["termux-telephony-call-log"], text=True)
            for line in calls.splitlines()[1:]:  # skip header
                parts = line.split()
                number = parts[1]  # column with number
                log_call(number)
        except Exception as e:
            pass  # ignore if no calls

        # Fetch incoming SMS
        try:
            sms_list = subprocess.check_output(["termux-sms-list", "-l", "10"], text=True)
            for line in sms_list.splitlines():
                if line.startswith("{") and '"address":' in line:
                    import ast
                    sms_dict = ast.literal_eval(line)
                    number = sms_dict.get("address", "")
                    message = sms_dict.get("body", "")
                    log_sms(number, message)
        except Exception as e:
            pass  # ignore if no SMS

        # Detect flooding numbers
        flood_calls = detect_flood(CALL_LOG_FILE)
        flood_sms = detect_flood(SMS_LOG_FILE)

        for num in flood_calls:
            subprocess.run(["termux-notification", "--title", "High Call Frequency", "--content", f"{num} called {FLOOD_THRESHOLD}+ times"])

        for num in flood_sms:
            subprocess.run(["termux-notification", "--title", "High SMS Frequency", "--content", f"{num} sent {FLOOD_THRESHOLD}+ messages"])

        # Export logs
        export_json(CALL_LOG_FILE, "call_log.json")
        export_json(SMS_LOG_FILE, "sms_log.json")

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    monitor()
