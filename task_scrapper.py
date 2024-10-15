import requests
import constants as c
import logging
import time
from dotenv import load_dotenv
import os
from pymongo import MongoClient



url = "https://www.airtasker.com/api/v2/tasks?limit=50&path=tasks&threaded_comments=true&task_states=posted&after=0&task_types=online&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&save_filters=true"

load_dotenv()

proxy_cred = os.getenv("HTTP_SCRAPPING_PROXY")
proxy = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.get_default_database()
users_collection = db['users']
tasks_collection = db['tasks']

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
            
    def to_dict(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'price': self.price,
            'state': self.state,
            'bid_on': self.bid_on,
            'classification': self.classification,
            'created_at': self.created_at,
            'sender_id': self.sender_id,
            'sender_last_activity': self.sender_last_activity,
            'description': self.description,
            'profile_name': self.profile_name,
        }

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
    tasks_to_insert = []
    for task in tasks:
        existing_task = tasks_collection.find_one({"slug": task.slug})
        if not existing_task:
            task.set_classification()
            task_data = task.to_dict()
            
            for user in users:
                user_name = user["name"]
                task_data[f"applied_{user_name}"] = "No"
                
            tasks_to_insert.append(task)
    if tasks_to_insert:
        tasks_collection.insert_many(tasks_to_insert)
        
    logging.info("New tasks have been stored!")


if __name__ == "__main__":
    while True:
        with requests.Session() as session:
            session.proxies.update(proxy)
            scrap(session)
            time.sleep(100)