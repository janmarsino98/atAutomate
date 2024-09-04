import constants as c
import requests
import os
import pandas as pd
import time
import logging

def get_last_notifications():
    url = "http://www.airtasker.com/api/client/v1/experiences/notification-feed/index?page_token="
    try:
        r = requests.get(url, headers=c.HEADERS, cookies=c.COOKIES, proxies=c.PROXY)
    
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


def send_message(slug, message):
    print("Intentando mandar mensaje a nuevas notificaciones...")
    print(c.PROXY)
    url = f"https://www.airtasker.com/api/v2/tasks/{slug}/private_messages?threaded_comments=true"
    payload = {"private_message":{"body":message}}
    try:
        r = requests.post(url, json=payload,cookies=c.COOKIES, headers=c.HEADERS, proxies=c.PROXY)
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error intentando enviar mensaje a una notifcacion. ==> Error: {e}")
        return None
    
    if r.status_code != 200:
        logging.error(f"No se ha mandado el mensaje a la notificaion correctamente. ==> Código: {r.status_code} - Reason: {r.reason}")
        return None
    
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

