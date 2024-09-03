import constants as c
import requests
import os
import pandas as pd
import time

def get_last_notifications():
    url = "https://www.airtasker.com/api/client/v1/experiences/notification-feed/index?page_token="
    r = requests.get(url, headers=c.HEADERS, cookies=c.COOKIES)
    data = r.json()["data"]
    return data["notifications"]

def get_task_slug(task_link_id):
    url = f"https://www.airtasker.com/api/v2/tasks/{task_link_id}/"
    r = requests.get(url, headers=c.HEADERS)
    data = r.json()
    slug = data["task"]["slug"]
    return slug


def send_message(slug, message):
    url = f"https://www.airtasker.com/api/v2/tasks/{slug}/private_messages?threaded_comments=true"
    payload = {"private_message":{"body":message}}
    r = requests.post(url, json=payload,cookies=c.COOKIES, headers=c.HEADERS, proxies=c.PROXY)
    return r

def message_new_tasks():
    notifications = get_last_notifications()
    assigned_tasks = []
    for notification in notifications:
        if "has assigned you" in notification["segments"][1]["text"]:
            task_slug = notification["segments"][2]["route"].replace("https://www.airtasker.com/tasks/", "")
            assigned_tasks.append(task_slug)
            
    previous_notifications = []
    if os.path.exists("notifications.xlsx"):
        df = pd.read_excel("notifications.xlsx", index_col=0)
        previous_notifications = list(df["notifications"])
        
    for assigned_task in assigned_tasks:
        if assigned_task not in previous_notifications:
            previous_notifications.append(assigned_task)
            task_slug = get_task_slug(assigned_task)
            response = send_message(task_slug, "Hello! Thank you very much for assigning me this task!😊 Can you please send me all the info at janmarsinopique98@gmail.com ?")
            
    new_df = pd.DataFrame(previous_notifications, columns=["notifications"])
    new_df.to_excel("notifications.xlsx")
    return "Notifications responded!"