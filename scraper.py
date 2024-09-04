import requests
import pandas as pd
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
import constants as c
import time
import helper_functions as hf
from notifications import message_new_tasks
import logging

load_dotenv()
proxy_cred = os.getenv("HTTP_PROXY")
proxy = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}

OPENAI_API_KEY = os.getenv('OPEN_AI_API_KEY')

url = "https://www.airtasker.com/api/v2/tasks?limit=50&path=tasks&threaded_comments=true&task_states=posted&after=0&task_types=online&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&save_filters=true"
base_task_url = "https://www.airtasker.com/api/v2/tasks/"
base_comment_url = "https://www.airtasker.com/api/v2/comments/"

def scrap(session):
    data = get_response(session)
    if data:
        tasks = get_tasks(data)
        store_tasks(tasks)
        classify_tasks()

def get_response(session: requests.Session) -> dict:
    try:
        r = session.get(url, headers=c.HEADERS)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al hacer request de nuevas tareas: {e}")
        return None
    if r.status_code == 200:
        data = r.json()
        logging.info("Nuevas tareas obtenidas correctamente.")
        return data
    else:
        logging.error(f"Código de respuesta incorrecta al hacer request de nuevas tareas: {r.status_code} - {r.reason}")
        return None

def get_tasks(data: dict) -> list:
    tasks = []
    for task in data["tasks"]:
        tasks.append({
            "slug": task["slug"], 
            "name": task["name"],
            "price": task["price"],
            "state": task["state"],
            "bid_on": task["bid_on"],
            })
    return tasks

def store_tasks(tasks: list):
    if os.path.isfile(c.DDBB_PATH):
        prev_df = pd.read_excel(c.DDBB_PATH, index_col=0)
    else:
        prev_df = pd.DataFrame()
        
    tasks_to_add = tasks.copy()
    
    for task in tasks:
        if not prev_df.empty and task["slug"] in prev_df["slug"].values:
            prev_df.loc[prev_df["slug"] == task["slug"], ["price", "state", "bid_on"]] = [task["price"], task["state"], task["bid_on"]]
            tasks_to_add.remove(task)
            
    new_tasks_df = pd.DataFrame.from_dict(tasks_to_add)

    if not new_tasks_df.empty:
        new_tasks_df["classification"] = ""
        new_tasks_df["applied"] = "No"

    if not prev_df.empty:
        final_df = pd.concat([prev_df, new_tasks_df], ignore_index=True).drop_duplicates(subset=["slug"], keep="first").reset_index(drop=True)
        
    else:
        final_df = new_tasks_df
        
    final_df.to_excel(c.DDBB_PATH)
        
def classify_tasks():
    df = pd.read_excel(c.DDBB_PATH, index_col=0)
    df["classification"] = df["classification"].astype(str)
    resume_list = ["resume", "reesume", "resumee", " cv ", "cover letter", "cv ", "cv"]
    for index, row in df.iterrows():
        for word in resume_list:
            if word in row["name"].lower():
                df.at[index, "classification"] = "CV"
    pd.DataFrame.to_excel(df, c.DDBB_PATH)

def apply_to_tasks(session):
    df = pd.read_excel(c.DDBB_PATH, index_col=0)
    df_cv_unapplied = df[(df["classification"] == "CV") & (df["applied"] == "No")]
    
    if df_cv_unapplied.empty:
        logging.info("No new jobs to apply for!")
        return
    for index, row in df_cv_unapplied.iterrows():
        try:
            name, description, profile_name = get_task_info(row["slug"], session)
            text_to_write = get_openai_description(name, description, profile_name)
            price = get_task_price(name, description)

            comment_id = send_offer(int(price), text_to_write, row["slug"], row["price"], session)
            if comment_id:
                send_reply(comment_id, "Previous feedback on similar task!", row["slug"], "imgs\LandedJobChat.png", session)
            
            df.loc[df["slug"] == row["slug"], "applied"] = "Yes"
            df.to_excel(c.DDBB_PATH)
        except Exception as e:
            logging.error(f"Error al procesar la tarea {row['slug']} ==> Error: {e}")
        time.sleep(100)
        
def get_openai_description(name, description, profile_name):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {"role": "system", "content": f"{c.GPT_SYSTEM_PROMPT}"},
            {"role": "user", "content": f"The task name is: {name}. The task description is: {description}. Finally the profile name of the person that published the task is: {profile_name}"}
        ]
    )
    return response.choices[0].message.content


def get_task_price(name, description):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Act as a freelancer. I will provide you my price list, a task description and a task name. According to theese parameters you need to return me a price for the task. If you consider the task can't be related to any element in the price list just answer with the sentence 'Task could not be classified'. Else you need to answer with ONLY the price that you would assign. It is important that you don't add any other word neither the currency in your resposne, just the number"},
            {"role": "user", "content": f"The task name is: {name}. The task description is {description} and my pricing list is {c.TARIFAS}"}
        ]
    )
    
    return response.choices[0].message.content
        

def get_task_info(task_link, session: requests.Session):
    task_url = base_task_url + task_link
    try:
        r = session.get(task_url, headers=c.HEADERS)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al intentar extraer información de la tarea {task_url}: {e}")
        return None
    
    if r.status_code != 200:
        logging.error(f"El codigo de respuesta al intentar extraer info de la tareal {task_url} no es 200 ==> Codigo: {r.status_code} - Razon: {r.reason}")
        return None
    data = r.json()
    name = data["task"]["name"]
    description = data["task"]["description"]
    profile_name = data["profiles"][0]["first_name"]
    return name, description, profile_name

def send_offer(price, text_to_send, task_url, task_price, session: requests.Session):
    post_url = base_task_url + task_url + "/bids?threaded_comments=true"
    
    if price < task_price * 0.8:
        price = int(task_price * 0.8)
    
    payload = {
        "bid": {
            "price": price
        },
        "afterpay_enabled": False,
        "comment": {
            "body": text_to_send
        }
    }

    try:
        r = session.post(post_url, json=payload, cookies=c.COOKIES, headers=c.HEADERS)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error trying to send an offer to task: {post_url}. ==> Error: {e}")
        return None
    
    if r.status_code != 200:
        logging.error(f"The code returned when trying to send the offer to task {post_url} was not 200. ==> Code: {r.status_code} - Reason: {r.reason}")
        return None
    
    data = r.json()
    comment_id = data["bid"]["comment_id"]
    logging.info(f"La oferta a la tarea {post_url} se ha publicado correctamente!")
    return comment_id

def send_reply(comment_id, reply_text, task_url, img_name, session: requests.Session):
    post_url = base_task_url + task_url + "/comments?threaded_comments=true"
    
    payload = { 
        "comment":{
            "body":reply_text,
            "parent_comment_id":comment_id
            },
        "warning_displayed":False
        }
    try:
        r = session.post(post_url, json=payload, cookies=c.COOKIES, headers=c.HEADERS)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error trying to send a reply to the task: {post_url}. Error: {e}")
        return None
    
    if r.status_code != 200:
        logging.error(f"The response status when trying to reply to task {post_url} was not 200. ==> Code: {r.status_code} - Reason: {r.reason}")
        return None
    
    data = r.json()
    comment_id = data["comment"]["id"]
    attach_img_to_comment(comment_id, img_name, session)
    return r.status_code

def attach_img_to_comment(comment_id, img_path, session: requests.Session):
    request_url = f"https://www.airtasker.com/api/v2/comments/{comment_id}/attachments?threaded_comments=true"
    try:
        with open(img_path, "rb") as img:
            files = {'attachments':img}
            r = session.post(request_url, files=files, headers=c.HEADERS, cookies=c.COOKIES)
            r.raise_for_status()
            
            logging.info(f"Se ha adjuntado correctamente la imagen al comentario {request_url}")
            return r.status_code
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error al intentar adjuntar imagen al comentario {request_url} ==> error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error trying to add an image to comment {request_url}. ==> error: {e}")
        return None
    except Exception as e:
        logging.error(f"Error inesperado al intentar adjuntar imagen al comentario {request_url} ==> Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        with requests.Session() as session:
            session.proxies.update(proxy)
            logging.info("Starting a new iteration to get tasks and apply to them.")
            try:
                scrap(session)
            except Exception as e:
                logging.error(f"Error al scrapear nuevas tareas. ==> Error: {e}")
                time.sleep(300)
                continue
            try:
                apply_to_tasks(session)
            except Exception as e:
                logging.error(f"Error al intentar aplicar a tareas. ==> Error {e}")
            time.sleep(100)
            logging.info("Checking for messages on new tasks.")
            try:
                message_new_tasks()
            except Exception as e:
                logging.error(f"Error al intentar enviar mensaje a nuevas tareas. ==> Error: {e}")
            logging.info("Iteration completed, waiting before next cycle. You can quit now!")
            time.sleep(100)
