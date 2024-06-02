import requests
import pandas as pd
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
import mysql.connector
import constants as c
import time

load_dotenv()

OPENAI_API_KEY = os.getenv('OPEN_AI_API_KEY')


url = "https://www.airtasker.com/api/v2/tasks?limit=8&path=tasks&threaded_comments=true&task_states=posted%2Cassigned%2Ccompleted%2Coverdue%2Cclosed&lat=-33.907256&lon=151.207706&location_name=Zetland%20NSW%2C%20Australia&task_types=both&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&after_time=2024-06-02T21%3A09%3A31%2B10%3A00"


url = "https://www.airtasker.com/api/v2/tasks?limit=50&path=tasks&threaded_comments=true&task_states=posted&after=0&task_types=online&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&save_filters=true"
base_task_url = "https://www.airtasker.com/api/v2/tasks/"
base_comment_url = "https://www.airtasker.com/api/v2/comments/"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

def scrap():
    data = get_response()
    tasks = get_tasks(data)
    store_tasks(tasks)
    classify_tasks()
    
def get_response() -> dict:
    r = requests.get(url, headers=headers)
    print(r)
    data = r.json()
    print(data.keys())
    return data

def get_tasks(data: dict) -> list:
    tasks = []
    for task in data["tasks"]:
        tasks.append({
            "slug": task["slug"], 
            "name": task["name"],
            "price": task["price"],
            })
    return tasks

def store_tasks(tasks):
    df = pd.DataFrame.from_dict(tasks)
    df["classification"] = ""
    df["applied"] = "No"
    if os.path.isfile(c.DDBB_PATH):
        last_df = pd.read_excel(c.DDBB_PATH, index_col=0)
        df = pd.concat([last_df, df], ignore_index=True).drop_duplicates(subset=["slug"], keep="first").reset_index(drop=True)
    pd.DataFrame.to_excel(df, c.DDBB_PATH)
        
        
def classify_tasks():
    df = pd.read_excel(c.DDBB_PATH, index_col=0)
    resume_list = ["resume", "reesume", "resumee", " cv ", "cover letter", "application"]
    for index, row in df.iterrows():
        for word in resume_list:
            if word in row["name"].lower():
                df.at[index, "classification"] = "CV"
                pd.DataFrame.to_excel(df, c.DDBB_PATH)
                continue
            
def apply_to_tasks():
    df = pd.read_excel(c.DDBB_PATH, index_col=0)
    df_cv_unapplied = df[(df["classification"] == "CV") & (df["applied"] == "No")]
    for index, row in df_cv_unapplied.iterrows():
        print(row["slug"])
        name, description, profile_name = get_task_info(row["slug"])
        text_to_write = get_openai_description(name, description, profile_name)
        price = get_task_price(name, description)
        comment_id, response_status = send_offer(int(price), text_to_write, row["slug"], row["price"])
        # response_status = send_reply(
        #     task_url=row["slug"],
        #     comment_id=comment_id, 
        #     reply_text="This are some reviews on similar task that I got from other taskers recently",
        #     img_name="cvReviews.jpg"
        #     )
        
        if response_status == 200:
            df.loc[df["slug"] == row["slug"], "applied"] = "Yes"
            df.to_excel(c.DDBB_PATH)
            print("Applied correctly...")
        time.sleep(10)
        
def get_task_info(task_link):
    task_url = base_task_url + task_link
    r = requests.get(task_url, headers=headers)
    data = r.json()
    name = data["task"]["name"]
    description = data["task"]["description"]
    profile_name = data["profiles"][0]["first_name"]
    return name, description, profile_name
        
    
def get_openai_description(name, description, profile_name):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {"role": "system", "content": "Imagine that you are an experience freelancer who has successfully completed several jobs in webpage. You are now trying to apply for one of this tasks. I will pass you the description of the task, the name of the task and the name of the person who is offering this task. You need to return a concise text to make an offer and maximize the chances of landing that job. Your text should first greet the person who published the task, then you must present yourself as a experienced tasker on the required task and tell that person why you are the best for doing that job. Then you must let the client know that you will start working on the task as soon as you get it assigned. Finally you should invite the client to check your profile for previous reviews on similar tasks. Please remember that you have to ONLY respond with the text you would send to the user, do not add any more information or extra clarifications. Make sure not to add any placeholders either, as I previously mentioned my name is Jan so if you need to include my name you can do it. The text should have around 50 words"},
            {"role": "user", "content": f"The task name is: {name}. The task description is: {description}. Finally the profile name of the person that published the task is: {profile_name}"}
        ]
    )
    print(response.choices[0].message.content)
    
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
    print(response.choices[0].message.content)
    
    return response.choices[0].message.content

def send_offer(price, text_to_send, task_url, task_price):
    post_url = base_task_url + task_url + "/bids?threaded_comments=true"
    
    if price < task_price:
        price = task_price
    
    post_cookies = {
        "at_sid":"c5a260d8-b5a9-4a9d-90c6-df5f786fdb53"
    }
    payload = {
        "bid": {
            "price": price
        },
        "afterpay_enabled": False,
        "comment": {
            "body": text_to_send
        }
    }


    x = requests.post(post_url, json=payload, cookies=post_cookies, headers=headers)
    data = x.json()
    print(data)
    comment_id = data["bid"]["comment_id"]
    print(x.status_code)
    return comment_id, x.status_code
    
    
def send_reply(comment_id, reply_text, task_url, img_name):
    
    post_url = base_task_url + task_url + "/comments?threaded_comments=true"
    
    payload = {
        "comment":{
            "body":reply_text,
            "parent_comment_id":comment_id
            },
        "warning_displayed":False
        }
    post_cookies = {
        "at_sid":"c5a260d8-b5a9-4a9d-90c6-df5f786fdb53"
    }

    x = requests.post(post_url, json=payload, cookies=post_cookies, headers=headers)
    data = x.json()
    comment_id = data["comment"]["id"]  
    return x.status_code
    with open(img_name, 'rb') as f:
        img_post_url = base_comment_url + str(comment_id) + "/attachments?threaded_comments=true"
        binary_img = f.read()
        fields={'attachments': ('cvReviews.jpg', binary_img, 'image/jpeg')}
    
        img_post_headers = {
            'Content-Type': 'multipart/form-data',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            }
        
        try:
            y = requests.post(
                url = img_post_url,
                data=fields,
                headers=img_post_headers,
                cookies=post_cookies
            )
            print(y.status_code)
            print(y.reason)
            print(y.text)
        
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

if __name__ == "__main__":
    while True:
        scrap()
        apply_to_tasks()
        time.sleep(30)
    print("Done")
