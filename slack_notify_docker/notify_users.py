import sqlite3
import requests
import os
import schedule
import time
from datetime import datetime

DATABASE_FILE = os.getenv('DATABASE_FILE')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

# In-memory set to keep track of notified users
notified_users = set()

def get_non_authorized_users(db_file):
    print(f"{datetime.now()} - Connecting to database: {db_file}")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    print(f"{datetime.now()} - Querying non-authorized users...")
    cursor.execute("SELECT id, username, email FROM users_info WHERE is_authorized = 0;")
    users = cursor.fetchall()

    print(f"{datetime.now()} - Found {len(users)} non-authorized users.")
    conn.close()
    return users

def send_slack_notification(users):
    if not users:
        print(f"{datetime.now()} - No non-authorized users to notify.")
        return

    new_users_to_notify = [user for user in users if user[0] not in notified_users]
    if not new_users_to_notify:
        print(f"{datetime.now()} - All non-authorized users have already been notified.")
        return

    user_list = "\n".join([f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}" for user in new_users_to_notify])
    message = f"Jupyterhub New non-authorized users on https://pslg-nv1.uni-graz.at/hub/authorize :\n{user_list}"

    print(f"{datetime.now()} - Sending Slack notification with message:\n{message}")
    slack_data = {'text': message}
    response = requests.post(
        SLACK_WEBHOOK_URL, json=slack_data,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(f"{datetime.now()} - Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

    # Add newly notified users to the set
    for user in new_users_to_notify:
        notified_users.add(user[0])

    print(f"{datetime.now()} - Slack notification sent successfully.")


def job():
    print(f"{datetime.now()} - Job started")
    users = get_non_authorized_users(DATABASE_FILE)
    send_slack_notification(users)
    print(f"{datetime.now()} - Job finished")

def schedule_jobs():
    # Schedule the job to run every hour between 07:00 and 17:00 from Monday to Friday
    for hour in range(7, 18):  # 7 to 17 inclusive
        schedule.every().monday.at(f"{hour:02d}:00").do(job)
        schedule.every().tuesday.at(f"{hour:02d}:00").do(job)
        schedule.every().wednesday.at(f"{hour:02d}:00").do(job)
        schedule.every().thursday.at(f"{hour:02d}:00").do(job)
        schedule.every().friday.at(f"{hour:02d}:00").do(job)

def run_pending_jobs():
    print(f"{datetime.now()} - Starting Program")
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait for a minute before checking again

if __name__ == "__main__":
    schedule_jobs()
    run_pending_jobs()
