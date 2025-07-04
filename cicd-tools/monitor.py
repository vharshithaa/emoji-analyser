import os
import sys
import json
import csv
from datetime import datetime
import subprocess
import requests
import joblib

MODEL_PATH = "cicd_model.pkl"
LOG_PATH = "logs/build_logs.csv"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def get_git_files_changed():
    try:
        output = subprocess.check_output(["git", "diff", "--name-only", "HEAD~1", "HEAD"])
        return len(output.decode("utf-8").splitlines())
    except Exception:
        return -1

def get_dev_name():
    return os.getenv("GITHUB_ACTOR", "unknown-dev")

def get_time_of_day():
    now = datetime.now()
    return now.strftime("%H:%M")

def run_prediction(files_changed):
    if not os.path.exists(MODEL_PATH):
        return "Unknown"
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([[files_changed]])[0]
    return "Failure" if prediction == 1 else "Success"

def log_data(dev, time, files_changed, test_status, predicted):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["developer", "time", "files_changed", "test_status", "predicted"])
        writer.writerow([dev, time, files_changed, test_status, predicted])

def send_slack_notification(dev, files_changed, test_status, prediction):
    emoji = "✅" if prediction == "Success" else "⚠️"
    suggestion = ""
    if prediction == "Failure":
        if files_changed > 15:
            suggestion = "• Split your PR into smaller parts.\n"
        if test_status == "Failure":
            suggestion += "• Review failed test cases before re-pushing.\n"

    msg = {
        "text": f"""*CI/CD Build Notification* {emoji}
*Developer:* `{dev}`
*Files Changed:* `{files_changed}`
*Prediction:* `{prediction}`
*Test Result:* `{test_status}`
{suggestion}"""
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(msg), headers=headers)
    if response.status_code != 200:
        print("Slack Notification Failed:", response.text)

def main():
    dev = get_dev_name()
    files_changed = get_git_files_changed()
    time_of_day = get_time_of_day()
    test_status = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    prediction = run_prediction(files_changed)
    log_data(dev, time_of_day, files_changed, test_status, prediction)
    send_slack_notification(dev, files_changed, test_status, prediction)

if __name__ == "__main__":
    main()