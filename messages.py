import requests
import pandas as pd


messages_url = "https://www.airtasker.com/api/v2/account/tasks?limit=100&after=0&sort_by=last_message_desc&private_messages=true&my_tasks=true"

msg_cookies = {
        "at_sid":"9d725325-fc38-431c-9bcc-8f37bfd66a49"
    }

msg_headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def get_last_messages():
    response = requests.get(messages_url, cookies=msg_cookies, headers=msg_headers)
    data = response.json()
    profiles = data["profiles"]
    last_messages = data["last_messages"]
    tasks = data["tasks"]
    profiles_df = pd.DataFrame(profiles)
    last_messages_df = pd.DataFrame(last_messages)
    tasks_df = pd.DataFrame(tasks)
    profiles_df.to_excel("profiles.xlsx")
    last_messages_df.to_excel("last_messages.xlsx")
    tasks_df.to_excel("Tasks.xlsx")
    
    
def send_message(message_body, task):
    url = f"https://www.airtasker.com/api/v2/tasks/{task}/private_messages?threaded_comments=true"
    payload ={"private_message": {"body": message_body}}
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Origin": "https://www.airtasker.com",
        "Content-Type":"application/json"
    }
    response = requests.post(url, json=payload, cookies=msg_cookies, headers=headers)
    print(response.content)
    
def 

get_last_messages()