import requests
import constants as c
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
from openai import OpenAI
import json
import pandas as pd

load_dotenv()

proxy_cred = os.getenv("HTTP_PROXY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
proxy = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}

def post_task(title, description, price, at_sid):
    
    url = "https://www.airtasker.com/api/client/v1/experiences/post-task/post"
    
    payload = {
        "title": title,
        "description": description,
        "date_type": "flexible",
        "price": price,
        "date": datetime.utcnow().isoformat() + 'Z',
        "location_type": {"type": "remote"},
        "image_urls": [],
        "origin": "header_post_task-v1",
        "key": str(uuid.uuid4()),
        "attribution_data": {},
        "request_quote_form": []
    }
    
    cookies = c.COOKIES
    cookies["at_sid"]= at_sid
    response = requests.post(url, json=payload, headers=c.HEADERS, proxies=proxy, cookies=cookies)
    print(response.status_code, response.reason)
    return response.status_code, response.reason


def change_profile_pic(picture_url: str, at_sid: str):
    url = "https://www.airtasker.com/api/v2/account/avatar?threaded_comments=true"
    img_r = requests.get(picture_url)
    img_path = "imgs/new_img.jpg"
    if img_r.status_code == 200:
        with open(img_path, "wb") as file:
            file.write(img_r.content)
    cookies = c.COOKIES
    cookies["at_sid"] = at_sid
    with open(img_path, "rb") as img:
        files = {'attachments':img}
        
        r = requests.post(url, files=files, headers=c.HEADERS, cookies=cookies)
            
    os.remove(img_path)
    
    return r.status_code


def generate_new_task():
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a usefull assistant that answers in json format. Make sure you only return the dictionary of the json and nothing else. Your answer will have 3 key value pairs. task_name, task_description, task_price. task_name is a string that must be the name of a task and must be at most 10 words long. task_description is a string that represents the description of a task and must be at most 25 words long. task_price is an integer that represents the price of a task. It must be between 80 and 120 depending on the amount of work required"},
            {"role": "user", "content": "Generate a new task that involves creating a bot in python for automating the process of bidding in tasks in airtasker"}
        ]
    )
    task_info_str = response.choices[0].message.content
    task_info_str = task_info_str.replace(r"json\n", "")
    print(task_info_str)
    task_info_json = json.loads(task_info_str)
    return task_info_json


def post_tasks():
    df = pd.read_excel("users.xlsx", index_col=0)

    at_sids = list(df["at_sid"])

    # for at_sid in at_sids:
    at_sid = at_sids[4]
    new_task = generate_new_task()

    response_code, response_reason = post_task (
        title=new_task["task_name"],
        description=new_task["task_description"],
        price=new_task["task_price"],
        at_sid=at_sid
    )
    
    print(response_code, response_reason)
    
post_tasks()