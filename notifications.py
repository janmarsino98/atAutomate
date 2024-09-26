import constants as c
import requests
import os
import pandas as pd
import time
import logging
from users import User

def get_last_notifications(user: User):
    url = "http://www.airtasker.com/api/client/v1/experiences/notification-feed/index?page_token="
    
    all_cookies = {
        "at_sid": user.at_sid
    }
    
    try:
        r = requests.get(url, headers=c.HEADERS, cookies=all_cookies, proxies=c.PROXY)
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al intentar obtener las ultimas notificaciones. ==> Error: {e}")
        return None
    
    if r.status_code != 200:
        logging.error(f"No se ha obtenido un codigo de respuesta de 200 al obtener las ultimas notificaciones. ==> Codigo: {r.status_code} - Reason: {r.reason}")
        return None
    
    else:
        data = r.json()["data"]
        logging.info("Got last notifications correctly!")
        return data["notifications"]

def get_task_slug(task_link_id):
    url = f"https://www.airtasker.com/api/v2/tasks/{task_link_id}/"
    try:
        r = requests.get(url, headers=c.HEADERS, proxies=c.PROXY)
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error intentando obtener la tarea {url}. ==> Error: {e}")
        return None
        
    if r.status_code != 200:
        logging.error(f"Al intentar obtener la tarea {url} no se ha obtenido una respuesta 200. ==> Codigo: {r.status_code} - Reason: {r.reason}")
        return None
        
    data = r.json()
    slug = data["task"]["slug"]
    return slug


def send_message(slug, user: User):
    url = f"https://www.airtasker.com/api/v2/tasks/{slug}/private_messages?threaded_comments=true"
    
    all_cookies = {
        "at_sid": user.at_sid
    }
    
    payload = {"private_message":{"body":user.message}}
    try:
        r = requests.post(url, json=payload,cookies=all_cookies, headers=c.HEADERS, proxies=c.PROXY)
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error intentando enviar mensaje a una notifcacion. ==> Error: {e}")
        return None
    
    if r.status_code != 200:
        logging.error(f"No se ha mandado el mensaje a la notificaion correctamente. ==> Código: {r.status_code} - Reason: {r.reason}")
        return None
    
    logging.info(f"{user.name} ha mandado un mensaje correctamente a {url}")
    return r

def message_new_tasks(user: User):
    notifications = get_last_notifications(user)
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
            response = send_message(task_slug, user)
            
    new_df = pd.DataFrame(previous_notifications, columns=["notifications"])
    new_df.to_excel("notifications.xlsx")
    return "Notifications responded!"

