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

load_dotenv()
PROXY_CRED = os.getenv("HTTP_PROXY")
proxy = {
    "http": f"http://{PROXY_CRED}",
    "https": f"http://{PROXY_CRED}",
}

OPENAI_API_KEY = os.getenv('OPEN_AI_API_KEY')


url = "https://www.airtasker.com/api/v2/tasks?limit=8&path=tasks&threaded_comments=true&task_states=posted%2Cassigned%2Ccompleted%2Coverdue%2Cclosed&lat=-33.907256&lon=151.207706&location_name=Zetland%20NSW%2C%20Australia&task_types=both&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&after_time=2024-06-02T21%3A09%3A31%2B10%3A00"


url = "https://www.airtasker.com/api/v2/tasks?limit=50&path=tasks&threaded_comments=true&task_states=posted&after=0&task_types=online&radius=50000&carl_ids=&disable_recommendations=false&badges=&max_price=9999&min_price=5&sort_by=posted_desc&save_filters=true"
base_task_url = "https://www.airtasker.com/api/v2/tasks/"
base_comment_url = "https://www.airtasker.com/api/v2/comments/"

def scrap():
    data = get_response()
    tasks = get_tasks(data)
    store_tasks(tasks)
    classify_tasks()
    
def get_response() -> dict:
    r = requests.get(url, headers=c.HEADERS)
    data = r.json()
    return data

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
            
def apply_to_tasks():
    df = pd.read_excel(c.DDBB_PATH, index_col=0)
    df_cv_unapplied = df[(df["classification"] == "CV") & (df["applied"] == "No")]
    
    if df_cv_unapplied.empty:
        print("No jobs to apply for...")
        return
    for index, row in df_cv_unapplied.iterrows():
        name, description, profile_name = get_task_info(row["slug"])
        text_to_write = get_openai_description(name, description, profile_name)
        price = get_task_price(name, description)
        try: 
            comment_id, response_status = send_offer(int(price), text_to_write, row["slug"], row["price"])
            if response_status == 200:
                send_reply(comment_id, "Previous feedback on similar task!", row["slug"], "imgs\LandedJobChat.png")
        
        except:
            response_status = 404
            pass
        
        df.loc[df["slug"] == row["slug"], "applied"] = "Yes"
        df.to_excel(c.DDBB_PATH)
        if response_status == 200:
            print("Applied correctly...")
            # attach_img_to_comment(comment_id, r"C:\Users\janma\Pictures\Sample_Jobs\SampleResume1.png")
            
        else:
            print(f"Unable to apply to this task: {response_status}")
        time.sleep(10)
        
def get_task_info(task_link):
    task_url = base_task_url + task_link
    r = requests.get(task_url, headers=c.HEADERS, proxies=proxy)
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
            {"role": "system", "content": f"{c.GPT_SYSTEM_PROMPT}"},
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
    proxy_cred = os.getenv("HTTP_PROXY")
    proxy = {
        "http": f"http://{proxy_cred}",
        "https": f"http://{proxy_cred}",
    }
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

    print(c.COOKIES)

    x = requests.post(post_url, json=payload, cookies=c.COOKIES, headers=c.HEADERS, proxies=proxy)
    data = x.json()
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
    
    x = requests.post(post_url, json=payload, cookies=c.COOKIES, headers=c.HEADERS, proxies=proxy)
    data = x.json()
    comment_id = data["comment"]["id"]
    attach_img_to_comment(comment_id, img_name)
    return x.status_code

def attach_img_to_comment(comment_id, img_path):
    request_url = f"https://www.airtasker.com/api/v2/comments/{comment_id}/attachments?threaded_comments=true"

    with open(img_path, "rb") as img:
        files = {'attachments':img}
        
        response = requests.post(request_url, files=files, headers=c.HEADERS, cookies=c.COOKIES, proxies=proxy)
        print(response.status_code)

if __name__ == "__main__":
    while True:
        print("Getting new tasks...")
        scrap()
        apply_to_tasks()
        # attach_img_to_comment("137614921", r"C:\Users\janma\Pictures\reviewsResume.png")
        # exit()
        time.sleep(15)
        print("Checking for messages on new tasks!")
        message_new_tasks()
        time.sleep(15)
    print("Done")