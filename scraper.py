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
from users import users, User
import logging
from pymongo import MongoClient

load_dotenv()
proxy_cred = os.getenv("HTTP_PROXY")
proxy = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}

OPENAI_API_KEY = os.getenv('OPEN_AI_API_KEY')
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.get_default_database()
users_collection = db['users']
tasks_collection = db['tasks']
sent_messages_collection = db['sentMessages']

url = "https://www.airtasker.com/api/v2/tasks?limit=50&path=tasks&threaded_comments=true&task_states=posted&after=0&task_types=online&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&save_filters=true"
base_task_url = "https://www.airtasker.com/api/v2/tasks/"
base_comment_url = "https://www.airtasker.com/api/v2/comments/"

class Task:
    def __init__(self, slug: str, name: str, price: int, state: str, bid_on: str):
        self.slug = slug
        self.name = name
        self.price = price
        self.state = state
        self.bid_on = bid_on
        self.classification = None
        
        self.created_at = None
        self.sender_id = None
        self.sender_last_activity = None
        self.description = None
        self.profile_name = None
        
    def set_classification(self):
        resume_list = ["resume", "reesume", "resumee", " cv ", "cover letter", "cv ", "cv"]
        for word in resume_list:
            if word in self.name.lower():
                self.classification = "CV"
                break

def scrap(session):
    data = get_response(session)
    if data:
        tasks = get_tasks(data)
        store_tasks(tasks)
        
def get_response(session: requests.Session) -> dict:
    try:
        r = session.get(url, headers=c.HEADERS)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al hacer request de nuevas tareas: {e}")
        time.sleep(300)
        return None
    if r.status_code == 200:
        data = r.json()
        logging.info("Nuevas tareas obtenidas correctamente.")
        return data
    else:
        logging.error(f"Código de respuesta incorrecta al hacer request de nuevas tareas: {r.status_code} - {r.reason}")
        return None

def get_tasks(data: dict) -> list[Task]:
    tasks = []
    for task_data in data["tasks"]:
        publisher_last_activity_at = None
        for profile in data["profiles"]:
            if profile["id"] == task_data["sender_id"]:
                publisher_last_activity_at = profile.get("last_activity_at")
                break

        task = Task(
            slug=task_data["slug"],
            name=task_data["name"],
            price=task_data["price"],
            state=task_data["state"],
            bid_on=task_data["bid_on"]
        )
        # Add additional attributes to the Task instance
        task.created_at = task_data["created_at"]
        task.sender_id = task_data["sender_id"]
        task.sender_last_activity = publisher_last_activity_at
        tasks.append(task)
    return tasks

def store_tasks(tasks: list[Task]):
    users = list(users_collection.find())
    for task in tasks:
        existing_task = tasks_collection.find_one({"slug": task.slug})
        if not existing_task:
            task.set_classification()
            task_data = task.__dict__
            
            for user in users:
                user_name = user["name"]
                task_data[f"applied_{user_name}"] = "No"
            result = tasks_collection.insert_one(task_data)
    logging.info("New tasks have been stored!")

def apply_to_tasks(session, user: User):
    
    query = {
        "classification": "CV",
        f"applied_{user.name}": "No"
    }
    
    unapplied_tasks_cursor = tasks_collection.find(query)
    
    if tasks_collection.count_documents(query) == 0:
        logging.info("No new jobs to apply for!")
        return
        
    
    for task_data in unapplied_tasks_cursor:
        # Create Task instance
        task = Task(
            slug=task_data["slug"],
            name=task_data["name"],
            price=task_data["price"],
            state=task_data["state"],
            bid_on=task_data["bid_on"]
        )
        
        try:
            name, description, profile_name = get_task_info(task.slug, session)
            text_to_write = get_openai_description(name, description, profile_name, user)
            price = get_task_price(name, description, user)
            comment_id = send_offer(
                int(price),
                text_to_write,
                task.slug,
                task.price,
                session,
                user.at_sid
            )
        except Exception as e:
            logging.error(f"Error processing task {task.slug} ==> Error: {e}")
        
        # Update the task to mark it as applied
        tasks_collection.update_one(
            {"slug": task.slug},
            {"$set": {f"applied_{user.name}": "Yes"}}
        )
        
def get_openai_description(name, description, profile_name, user: User):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": f"{user.prompt}"},
            {"role": "user", "content": f"The task name is: {name}. The task description is: {description}. Finally the profile name of the person that published the task is: {profile_name}"}
        ]
    )
    return response.choices[0].message.content


def get_task_price(name, description, user:User):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Act as a freelancer. I will provide you my price list, a task description and a task name. According to theese parameters you need to return me a price for the task. If you consider the task can't be related to any element in the price list just answer with the sentence 'Task could not be classified'. Else you need to answer with ONLY the price that you would assign. It is important that you don't add any other word neither the currency in your resposne, just the number as an integer"},
            {"role": "user", "content": f"The task name is: {name}. The task description is {description} and my pricing list is {user.tarifas}"}
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
        logging.error(f"El codigo de respuesta al intentar extraer info de la tarea {task_url} no es 200 ==> Codigo: {r.status_code} - Razon: {r.reason}")
        return None
    data = r.json()
    name = data["task"]["name"]
    description = data["task"]["description"]
    profile_name = data["profiles"][0]["first_name"]
    return name, description, profile_name

def send_offer(price, text_to_send, task_url, task_price, session: requests.Session, at_sid:str):
    post_url = base_task_url + task_url + "/bids?threaded_comments=true"
    
    all_cookies = {
        "at_sid": at_sid
    }
    
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
        r = session.post(post_url, json=payload, cookies=all_cookies, headers=c.HEADERS)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error trying to send an offer to task: {post_url}. ==> Error: {e}")
        return None
    
    if r.status_code != 200:
        logging.error(f"{user.name}: The code returned when trying to send the offer to task {post_url} was not 200. ==> Code: {r.status_code} - Reason: {r.reason}")
        return None
    
    data = r.json()
    comment_id = data["bid"]["comment_id"]
    logging.info(f"La oferta a la tarea {post_url} se ha publicado correctamente!")
    return comment_id

def send_reply(comment_id, reply_text, task_url, img_name, session: requests.Session, at_sid:str):
    post_url = base_task_url + task_url + "/comments?threaded_comments=true"
    
    all_cookies = {
        "at_sid": at_sid
    }
    
    payload = { 
        "comment":{
            "body":reply_text,
            "parent_comment_id":comment_id
            },
        "warning_displayed":False
        }
    try:
        r = session.post(post_url, json=payload, cookies=all_cookies, headers=c.HEADERS)
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
    
def main_function():
    while True:
        for user in users:
            if user.name in ["Ava", "Rachel"]:
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
                        apply_to_tasks(session, user)
                    except Exception as e:
                        logging.error(f"Error al intentar aplicar a tareas. ==> Error {e}")
                    time.sleep(100)
                    logging.info("Checking for messages on new tasks.")
                    try:
                        message_new_tasks(user)
                    except Exception as e:
                        logging.error(f"Error al intentar enviar mensaje a nuevas tareas. ==> Error: {e}")
                        
                    logging.info(f"User {user.name} completed!")
                    time.sleep(150)
        logging.info("Iteration completed, waiting before next cycle. You can quit now!")

def new_main():
    with requests.Session() as session:
        scrap(session)

if __name__ == "__main__":
    with requests.Session() as session:
        from users import user_ava
        apply_to_tasks(session, user_ava)